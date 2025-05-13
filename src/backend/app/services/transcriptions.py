from __future__ import annotations

"""
음성 업로드·변환(Polling) 비즈니스 로직
=====================================

* 업로드 → Whisper 변환(Celery)까지의 상태 흐름 관리
* DB에는 **메타데이터**만 저장, 실제 파일은 `uploads/audio/`, `uploads/text/`
* GPT 호출·Whisper 변환 자체는 **여기서 수행하지 않음** (Celery 태스크 발행만)

상태 흐름
---------
uploading → uploaded → transcribing → done
                   ↘︎                     ↘︎
              upload_failed      transcription_failed
                   ↘︎                     ↘︎
                        cancelled  (사용자 취소)
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Final, Iterable

import aiofiles        # 비동기 파일 I/O
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transcription import Transcription, TranscriptionStatus
from app.schemas.transcriptions import UploadStatusResponse

# Celery 태스크 – **구현은 별도 모듈** (`app.tasks.transcription`)
from app.tasks.transcription import start_whisper_transcription  # type: ignore

# --------------------------------------------------------------------------- #
# 설정 상수
# --------------------------------------------------------------------------- #
ALLOWED_EXT: Final[set[str]] = {".mp3", ".wav"}
MAX_FILE_BYTES: Final[int] = 40 * 1024 * 1024  # 40 MiB

AUDIO_DIR = Path("uploads/audio")
TEXT_DIR = Path("uploads/text")

# 보장: 런타임 최초 호출 시 한 번만 디렉터리 생성
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)

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
async def _latest_transcription(session: AsyncSession) -> Transcription | None:
    stmt = select(Transcription).order_by(Transcription.created_at.desc()).limit(1)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def _save_upload(file: UploadFile) -> tuple[str, int]:
    """
    업로드 파일을 `uploads/audio/` 하위에 저장하고
    (절대경로, 최종 바이트크기)를 반환합니다.
    """
    ext = Path(file.filename or "").suffix.lower()
    uid = f"{uuid.uuid4()}{ext}"
    out_path = AUDIO_DIR / uid

    size = 0
    async with aiofiles.open(out_path, "wb") as out_stream:
        while chunk := await file.read(1024 * 1024):  # 1 MiB씩
            size += len(chunk)
            if size > MAX_FILE_BYTES:
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
    file: UploadFile, session: AsyncSession
) -> UploadStatusResponse:
    """
    1. 포맷·크기 검증 → `uploading` 레코드 생성
    2. 파일 저장 완료 → `uploaded`로 업데이트
    3. Celery 태스크 호출
    """
    if not file or not file.filename:
        raise MissingFile

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise UnsupportedAudioFormat

    # ――― DB: uploading ----------------------------------------------------- #
    transcription = Transcription(
        user_id=None,  # 🔖 실제 서비스에서는 토큰 → user_id 주입
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


async def get_audio_status(session: AsyncSession) -> UploadStatusResponse:
    """가장 최근 Transcription 상태만 반환합니다."""
    try:
        transcription = await _latest_transcription(session)
        if transcription is None:
            raise NoAudioData
        return _status_response(transcription)
    except SQLAlchemyError as exc:
        raise DatabaseError from exc


async def cancel_audio(session: AsyncSession) -> None:
    """
    uploading / uploaded / transcribing 단계에서만 취소 가능.

    * 상태 cancelled 로 변경
    * 저장된 파일(음성·텍스트) 삭제
    """
    try:
        transcription = await _latest_transcription(session)
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
