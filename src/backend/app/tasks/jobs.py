from __future__ import annotations

import asyncio
import logging
import os
import uuid

from celery import Celery
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.celery_app import celery_app  # Celery 인스턴스
from app.core.config import settings
from app.core.stt import STTCallError, transcribe_audio
from app.db.session import async_session
from app.models.transcription import Transcription
from app.services.generations import generate_contract

logger = logging.getLogger(__name__)

# 업로드 디렉터리가 없으면 생성
TEXT_UPLOAD_DIR = getattr(settings, "TEXT_UPLOAD_DIR", "uploads/text")
os.makedirs(TEXT_UPLOAD_DIR, exist_ok=True)


def _write_text_to_file(text: str) -> str:
    """텍스트를 파일로 저장하고 파일 경로를 반환합니다."""
    filename = f"{uuid.uuid4()}.txt"
    file_path = os.path.join(TEXT_UPLOAD_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as fp:
        fp.write(text)
    return file_path


@celery_app.task(name="tasks.jobs.start_whisper_transcription", bind=True)
def start_whisper_transcription(self, transcription_id: str) -> None:  # noqa: ANN001
    """지정된 Transcription 레코드에 대해 Whisper STT를 실행합니다."""

    async def _run() -> None:  # noqa: D401
        async with async_session() as session:
            try:
                result = await session.execute(
                    select(Transcription).where(Transcription.id == transcription_id)
                )
                transcription: Transcription | None = result.scalar_one_or_none()
                if transcription is None:
                    logger.error("Transcription %s not found", transcription_id)
                    return

                try:
                    logger.info("[Whisper] 시작: %s", transcription.audio_file)
                    text = await transcribe_audio(transcription.audio_file)
                    text_path = _write_text_to_file(text)

                    transcription.text_file = text_path
                    transcription.status = "done"
                    logger.info("[Whisper] 완료: %s → %s", transcription.audio_file, text_path)
                except STTCallError as exc:
                    transcription.status = "transcription_failed"
                    logger.exception("Whisper STT 실패: %s", exc)
                except Exception as exc:  # noqa: BLE001
                    transcription.status = "transcription_failed"
                    logger.exception("예상치 못한 오류: %s", exc)

                await session.commit()
            except SQLAlchemyError:
                logger.exception("DB 작업 중 오류 발생")
                raise

    asyncio.run(_run())


@celery_app.task(name="tasks.start_contract_generation", bind=True)
def start_contract_generation(self) -> None:  # noqa: ANN001
    """완료된 Transcription을 기반으로 계약서 생성을 시작합니다."""

    async def _run() -> None:  # noqa: D401
        async with async_session() as session:
            try:
                logger.info("[Contract] 생성 파이프라인 시작")
                await generate_contract(session)
                logger.info("[Contract] 생성 파이프라인 완료")
            except Exception as exc:  # noqa: BLE001
                logger.exception("계약서 생성 파이프라인 실패: %s", exc)

    asyncio.run(_run())
