from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_session, get_current_user
from app.schemas.transcription import (
    UploadInitRequest,
    UploadInitResponse,
    UploadStatusResponse,
)
from app.services import transcriptions as svc

router = APIRouter(prefix="/transcription", tags=["Transcription"])


@router.post(
    "/initiate",
    response_model=UploadInitResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def initiate_upload(
    data: UploadInitRequest,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """음성 업로드 세션을 초기화하고 업로드 URL을 반환합니다."""
    return await svc.register_upload(data.filename, current_user.id, session)


@router.get("/status", response_model=UploadStatusResponse)
async def check_status(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return await svc.get_audio_status(current_user.id, session)


@router.get(
    "/retry",
    status_code=status.HTTP_202_ACCEPTED,
)
async def retry_transcription(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await svc.retry_transcription(current_user.id, session)
    return {"detail": "Retry started"}


@router.post(
    "/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_transcription(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await svc.cancel_transcription(current_user.id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/uploaded-notify/{transcription_id}",
    status_code=status.HTTP_202_ACCEPTED,
    include_in_schema=False,  # 내부 호출용
)
async def uploaded_notify(
    transcription_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """nginx 업로드 완료 Callback"""
    await svc.trigger_transcription(transcription_id, session)
    return {"detail": "Accepted"}
    