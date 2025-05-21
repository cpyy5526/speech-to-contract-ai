from __future__ import annotations

"""
음성 업로드·변환(Polling) 비즈니스 로직
=====================================

* 업로드 → Whisper 변환(Celery)까지의 상태 흐름 관리
* DB에는 **메타데이터**만 저장, 실제 파일은 `uploads/audio/`, `uploads/text/`
* GPT 호출·Whisper 변환 자체는 **여기서 수행하지 않음** (Celery 태스크 발행만)

상태 흐름
---------
     ------ cancelled -------
     |           |          |
uploading -> uploaded -> transcribing -> done
                 |               |    
            upload_failed   transcription_failed
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Final, Iterable
from uuid import UUID

import aiofiles        # 비동기 파일 I/O
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.transcription import Transcription, TranscriptionStatus
from app.schemas.transcription import UploadStatusResponse

# Celery 태스크 – **구현은 별도 모듈** (`app.tasks.transcription`)
from app.tasks.transcription import start_whisper_transcription  # type: ignore


# --------------------------------------------------------------------------- #
# 공개 API
# --------------------------------------------------------------------------- #
__all__: Iterable[str] = (
    # service 함수
    "upload_audio",
    "get_audio_status",
    "cancel_audio",
    # 예외
    "MissingFile",
    "UnsupportedAudioFormat",
    "FileTooLarge",
    "NoAudioData",
    "InvalidStatusForCancel",
    "DatabaseError",
)


# --------------------------------------------------------------------------- #
# 예외 정의
# --------------------------------------------------------------------------- #
class MissingFile(Exception):
    """업로드 파일이 제공되지 않았거나 비어 있을 때."""


class UnsupportedAudioFormat(Exception):
    """허용되지 않은 확장자(.mp3, .wav 아님)."""


class FileTooLarge(Exception):
    """파일 크기가 `MAX_FILE_BYTES`를 초과할 때."""


class NoAudioData(Exception):
    """사용자에게 Transcription 레코드가 아예 없을 때."""


class InvalidStatusForCancel(Exception):
    """취소 불가 단계(이미 done/failed/cancelled 등)."""


class DatabaseError(Exception):
    """SQLAlchemy 예외 래퍼."""


# --------------------------------------------------------------------------- #
# 내부 헬퍼
# --------------------------------------------------------------------------- #
async def _latest_transcription(
        session: AsyncSession, user_id: UUID
) -> Transcription | None:
    stmt = (
        select(Transcription)
        .where(Transcription.user_id == user_id)
        .order_by(Transcription.created_at.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def _save_upload(file: UploadFile) -> tuple[str, int]:
    """
    업로드 파일을 `uploads/audio/` 하위에 저장하고
    (절대경로, 최종 바이트크기)를 반환합니다.
    """
    ext = Path(file.filename or "").suffix.lower()
    uid = f"{uuid.uuid4()}{ext}"
    out_path = Path(settings.AUDIO_UPLOAD_DIR) / uid

    # chunk 단위로 복사하며 파일 용량 제한을 체크하는 방식이 다소 비효율적일 수 있으나,
    # 파일 용량을 먼저 체크하는 방식은 비동기 환경에서 안정성과 이식성 이슈가 있으므로 일단 현재 방식 사용
    size = 0
    async with aiofiles.open(out_path, "wb") as out_stream:
        while chunk := await file.read(1024 * 1024):  # 1 MiB씩
            size += len(chunk)
            if size > settings.MAX_UPLOAD_SIZE_BYTES:
                # 부분 저장된 파일 정리
                await out_stream.close()
                out_path.unlink(missing_ok=True)
                raise FileTooLarge
            await out_stream.write(chunk)

    return str(out_path), size


def _status_response(model: Transcription) -> UploadStatusResponse:
    status_str = (
        model.status.value if hasattr(model.status, "value") else str(model.status)
    )
    return UploadStatusResponse(status=status_str)


# --------------------------------------------------------------------------- #
# 비즈니스 로직 (라우터에서 호출)
# --------------------------------------------------------------------------- #
async def upload_audio(
    file: UploadFile, session: AsyncSession, user_id: UUID
) -> UploadStatusResponse:
    """
    1. 포맷·크기 검증 → `uploading` 레코드 생성
    2. 파일 저장 완료 → `uploaded`로 업데이트
    3. Celery 태스크 호출
    """
    if not file or not file.filename:
        raise MissingFile

    ext = Path(file.filename).suffix.lower()
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise UnsupportedAudioFormat

    # ――― DB: uploading ----------------------------------------------------- #
    transcription = Transcription(
        user_id=user_id,
        status=TranscriptionStatus.uploading,
    )

    try:
        session.add(transcription)
        await session.commit()
        await session.refresh(transcription)
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc

    # ――― 파일 저장 --------------------------------------------------------- #
    try:
        audio_path, _size = await _save_upload(file)
    except FileTooLarge:
        # 상태 upload_failed 로 기록
        transcription.status = TranscriptionStatus.upload_failed
        transcription.updated_at = datetime.utcnow()
        await session.commit()
        raise
    finally:
        await file.close()

    # ――― DB: uploaded ------------------------------------------------------ #
    transcription.audio_file = audio_path
    transcription.status = TranscriptionStatus.uploaded
    transcription.updated_at = datetime.utcnow()

    try:
        session.add(transcription)
        await session.commit()
        await session.refresh(transcription)
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc

    # ――― Celery 변환 시작 --------------------------------------------------- #
    # 변환 시작 후 Celery 워커가 상태를 transcribing → done/failed 로 변경
    start_whisper_transcription.delay(str(transcription.id))

    return _status_response(transcription)


async def get_audio_status(
    session: AsyncSession, user_id: UUID
) -> UploadStatusResponse:
    """가장 최근 Transcription 상태만 반환합니다."""
    try:
        transcription = await _latest_transcription(session, user_id)
        if transcription is None:
            raise NoAudioData
        return _status_response(transcription)
    except SQLAlchemyError as exc:
        raise DatabaseError from exc


async def cancel_audio(session: AsyncSession, user_id: UUID) -> None:
    """
    uploading / uploaded / transcribing 단계에서만 취소 가능.

    * 상태 cancelled 로 변경
    * 저장된 파일(음성·텍스트) 삭제
    """
    try:
        transcription = await _latest_transcription(session, user_id)
        if transcription is None:
            raise NoAudioData

        if transcription.status not in {
            TranscriptionStatus.uploading,
            TranscriptionStatus.uploaded,
            TranscriptionStatus.transcribing,
        }:
            raise InvalidStatusForCancel

        # 파일 정리
        for path_str in (transcription.audio_file, transcription.script_file):
            if path_str:
                Path(path_str).unlink(missing_ok=True)

        # 상태 갱신
        transcription.status = TranscriptionStatus.cancelled
        transcription.updated_at = datetime.utcnow()
        session.add(transcription)
        await session.commit()

    except (NoAudioData, InvalidStatusForCancel):
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc
