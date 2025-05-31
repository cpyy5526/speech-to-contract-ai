import os
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.transcription import Transcription, TranscriptionStatus
from app.models.generation import Generation
from app.schemas.transcription import UploadInitResponse, UploadStatusResponse
from app.tasks.transcriptions import process_uploaded_audio


async def register_upload(
    filename: str, user_id: UUID, session: AsyncSession
) -> UploadInitResponse:
    """업로드 세션을 등록하고 클라이언트에 업로드 URL을 제공합니다."""
    ext = _validate_ext(filename)

    transcription = Transcription(
        user_id=user_id,
        status=TranscriptionStatus.uploading,
    )

    try:
        session.add(transcription)
        await session.commit()
        await session.refresh(transcription)
        transcription.audio_file = f"{transcription.id}{ext}"
        await session.commit()

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
    upload_url = f"{settings.UPLOAD_BASE_URL}/upload/audio/{transcription.id}"
    return UploadInitResponse(upload_url=upload_url)


async def trigger_transcription(transcription_id: UUID, session: AsyncSession) -> None:
    """업로드 완료 후 변환 태스크를 실행합니다."""
    transcription = await session.get(Transcription, transcription_id)
    
    # API 설계상 클라이언트 요청만으로는 논리적으로 발생할 수 없지만 방어적으로 처리
    if not transcription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    # 서버 내부 실행 환경이나 DB의 예기치 못한 문제. 로그만 남김 (클라이언트에서는 계속 uploading으로 표시됨)
    try:
        transcription.status = TranscriptionStatus.uploaded
        await session.commit()
    except SQLAlchemyError as exc:
        await session.rollback()
        # logger.exception("DB commit 실패: transcription_id=%s", transcription_id)
        raise HTTPException(status_code=500, detail="Unexpected server error")

    # Celery 태스크 큐에 등록
    process_uploaded_audio.delay(str(transcription_id))


async def get_audio_status(user_id: UUID, session: AsyncSession) -> UploadStatusResponse:
    transcription = await _get_latest(user_id, session)

    # 만약 done 상태라면, 이미 generation에 연결됐는지 추가로 검사
    if transcription.status == TranscriptionStatus.done:
        result = await session.exec(
            select(Generation).where(Generation.transcription_id == transcription.id)
        )
        generation = result.first()
        if generation:
            # 이미 계약서 생성에 사용된 transcription -> 추적 대상 아님 (요청 로직 오류 방지)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No audio data for this user"
            )
    
    return UploadStatusResponse(status=transcription.status.value)


async def cancel_transcription(user_id: UUID, session: AsyncSession) -> None:
    transcription = await _get_latest(user_id, session)

    if transcription.status not in {
        TranscriptionStatus.uploading,
        TranscriptionStatus.uploaded,
        TranscriptionStatus.transcribing,
        TranscriptionStatus.transcription_failed,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot cancel at this stage"
        )

    transcription.status = TranscriptionStatus.cancelled
    await session.commit()


async def retry_transcription(user_id: UUID, session: AsyncSession) -> None:
    transcription = await _get_latest(user_id, session)
    if transcription.status != TranscriptionStatus.transcription_failed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot retry at this stage")
    transcription.status = TranscriptionStatus.uploaded  # 상태를 uploaded로 되돌리고 재시작
    await session.commit()
    process_uploaded_audio.delay(str(transcription.id))


def _validate_ext(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    if not ext or ext.lower() not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported audio format",
        )
    return ext.lower()


async def _get_latest(user_id: UUID, session: AsyncSession) -> Transcription:
    try:
        result = await session.exec(
            select(Transcription)
            .where(Transcription.user_id == user_id)
            .order_by(Transcription.created_at.desc())
            .limit(1)
        )
        transcription = result.first()
        if not transcription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No audio data for this user"
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    return transcription
