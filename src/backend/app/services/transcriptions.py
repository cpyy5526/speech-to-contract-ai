import os
from uuid import uuid4, UUID

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.transcription import Transcription, TranscriptionStatus
from app.schemas.transcription import UploadInitResponse, UploadStatusResponse
from app.tasks.transcriptions import process_uploaded_audio

ALLOWED_EXTENSIONS = set(settings.ALLOWED_EXTENSIONS)


def _validate_filename(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    if not ext or ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported audio format",
        )
    return ext.lower()


async def register_upload(
    filename: str, user_id: UUID, session: AsyncSession
) -> UploadInitResponse:
    """업로드 세션을 등록하고 클라이언트에 업로드 URL을 제공합니다."""
    ext = _validate_filename(filename)
    transcription_id = uuid4()
    audio_filename = f"{transcription_id}{ext}"

    transcription = Transcription(
        id=transcription_id,
        user_id=user_id,
        audio_file=audio_filename,
        status=TranscriptionStatus.uploading,
    )
    session.add(transcription)
    await session.commit()

    upload_url = f"{settings.UPLOAD_BASE_URL}/upload/audio/{transcription_id}"
    return UploadInitResponse(upload_url=upload_url)


async def trigger_transcription(transcription_id: UUID, session: AsyncSession) -> None:
    """업로드 완료 후 변환 태스크를 실행합니다."""
    transcription = await session.get(Transcription, transcription_id)
    if not transcription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    transcription.status = TranscriptionStatus.uploaded
    await session.commit()

    # Celery 태스크 큐에 등록
    process_uploaded_audio.delay(str(transcription_id))


async def get_audio_status(user_id: UUID, session: AsyncSession) -> UploadStatusResponse:
    result = await session.exec(
        select(Transcription)
        .where(Transcription.user_id == user_id)
        .order_by(Transcription.created_at.desc())
        .limit(1)
    )
    transcription = result.first()
    if not transcription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audio data for this user")
    return UploadStatusResponse(status=transcription.status.value)


async def cancel_transcription(user_id: UUID, session: AsyncSession) -> None:
    transcription = await _get_latest(user_id, session)
    if transcription.status not in {
        TranscriptionStatus.uploading,
        TranscriptionStatus.uploaded,
        TranscriptionStatus.transcribing,
        TranscriptionStatus.transcription_failed,
    }:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot cancel at this stage")
    transcription.status = TranscriptionStatus.cancelled
    await session.commit()


async def retry_transcription(user_id: UUID, session: AsyncSession) -> None:
    transcription = await _get_latest(user_id, session)
    if transcription.status != TranscriptionStatus.transcription_failed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot retry at this stage")
    transcription.status = TranscriptionStatus.uploaded  # 상태를 uploaded로 되돌리고 재시작
    await session.commit()
    process_uploaded_audio.delay(str(transcription.id))


async def _get_latest(user_id: UUID, session: AsyncSession) -> Transcription:
    result = await session.exec(
        select(Transcription)
        .where(Transcription.user_id == user_id)
        .order_by(Transcription.created_at.desc())
        .limit(1)
    )
    transcription = result.first()
    if not transcription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No audio data for this user")
    return transcription
