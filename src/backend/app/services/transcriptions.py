from app.core.logger import logging
logger = logging.getLogger(__name__)

import os
from uuid import UUID
from pathlib import Path
from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
        logger.info(
            "업로드 세션 등록 완료: user_id=%s, transcription_id=%s",
            user_id, transcription.id
        )

    except SQLAlchemyError:
        await session.rollback()
        logger.error("업로드 세션 등록 중 DB 오류: user_id=%s", user_id, exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
    upload_url = f"{settings.UPLOAD_BASE_URL}/upload/audio/{transcription.audio_file}"
    return UploadInitResponse(upload_url=upload_url)


async def trigger_transcription(transcription_id: UUID, session: AsyncSession) -> None:
    """업로드 완료 후 변환 태스크를 실행합니다."""
    transcription = await session.get(Transcription, transcription_id)
    
    # API 설계상 클라이언트 요청만으로는 논리적으로 발생할 수 없지만 방어적으로 처리
    if not transcription:
        logger.warning("transcription_id 존재하지 않음: %s", transcription_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    audio_path = Path(settings.AUDIO_UPLOAD_DIR) / transcription.audio_file
    if not audio_path.is_file():
        transcription.status = TranscriptionStatus.upload_failed
        await session.commit()
        logger.warning(
            "파일 없음, 상태 'upload_failed'로 반영: transcription_id=%s, path=%s",
            transcription_id, audio_path
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio file not found. Upload may have failed."
        )

    # 서버 내부 실행 환경이나 DB의 예기치 못한 문제. 로그만 남김 (클라이언트에서는 계속 uploading으로 표시됨)
    try:
        transcription.status = TranscriptionStatus.uploaded
        await session.commit()
        logger.info("transcription 상태 'uploaded'로 변경 완료: transcription_id=%s", transcription_id)
    except SQLAlchemyError as exc:
        await session.rollback()
        logger.error("DB commit 실패: transcription_id=%s", transcription_id, exc_info=True)
        raise HTTPException(status_code=500, detail="Unexpected server error")

    # Celery task queue에 텍스트 변환 파이프라인 등록
    try:
        process_uploaded_audio.delay(str(transcription_id))
        logger.info("STT 변환 태스크 Celery 등록 완료: transcription_id=%s", transcription_id)
    except Exception:
        logger.error("Celery 등록 실패: transcription_id=%s", transcription_id, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )


async def get_audio_status(user_id: UUID, session: AsyncSession) -> UploadStatusResponse:
    transcription = await _get_latest(user_id, session)

    # 만약 done 상태라면, 이미 generation에 연결됐는지 추가로 검사
    if transcription.status == TranscriptionStatus.done:
        result = await session.execute(
            select(Generation).where(Generation.transcription_id == transcription.id)
        )
        generation = result.scalars().first()
        if generation:
            # 이미 계약서 생성에 사용된 transcription -> 추적 대상 아님 (요청 로직 오류 방지)
            logger.warning(
                "이미 generation에 사용된 transcription 요청 차단: transcription_id=%s",
                transcription.id
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No audio data for this user"
            )
    
    logger.info(
        "transcription 상태 조회 성공: user_id=%s, status=%s",
        user_id, transcription.status
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
        logger.warning(
            "취소 불가한 transcription 상태: user_id=%s, status=%s",
            user_id, transcription.status
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot cancel at this stage"
        )

    transcription.status = TranscriptionStatus.cancelled
    await session.commit()
    logger.info("transcription 취소 완료: transcription_id=%s", transcription.id)


async def retry_transcription(user_id: UUID, session: AsyncSession) -> None:
    transcription = await _get_latest(user_id, session)
    if transcription.status != TranscriptionStatus.transcription_failed:
        logger.warning(
            "재시도 불가 상태: transcription_id=%s, status=%s",
            transcription.id, transcription.status
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot retry at this stage"
        )
    transcription.status = TranscriptionStatus.uploaded  # 상태를 uploaded로 되돌리고 재시작
    await session.commit()
    logger.info("transcription 재시도 준비 완료: transcription_id=%s", transcription.id)

    try:
        process_uploaded_audio.delay(str(transcription.id))
        logger.info("재시도 STT 태스크 Celery 등록 완료: transcription_id=%s", transcription.id)
    except Exception:
        logger.error(
            "Celery 등록 실패 (재시도): transcription_id=%s",
            transcription.id, exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )


def _validate_ext(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    if not ext or ext.lower() not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported audio format",
        )
    return ext.lower()


async def _get_latest(user_id: UUID, session: AsyncSession) -> Transcription:
    logger.info("최신 transcription 조회 시작: user_id=%s", user_id)
    try:
        result = await session.execute(
            select(Transcription)
            .where(Transcription.user_id == user_id)
            .order_by(Transcription.created_at.desc())
            .limit(1)
        )
        transcription = result.scalars().first()
        logger.info("최신 transcription 조회 결과: %s", transcription)
    except Exception as e:
        logger.exception("Transcription 조회 중 예기치 못한 예외 발생: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    
    if not transcription:
        logger.warning("해당 user의 transcription 없음: user_id=%s", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No audio data for this user"
        )
    
    return transcription
