from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.transcription import UploadStatusResponse
from app.services import transcriptions as transcription_service

from app.core.dependencies import get_session, get_current_user
from app.models.user import User

router = APIRouter(prefix="/contracts/audio", tags=["Transcriptions"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def upload_audio(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    사용자의 녹음 파일 업로드
    """
    try:
        return await transcription_service.upload_audio(file, session, user.id)
    except transcription_service.MissingFile:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing or invalid audio file")
    except transcription_service.UnsupportedAudioFormat:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported audio format")
    except transcription_service.FileTooLarge:
        raise HTTPException(status.HTTP_413_PAYLOAD_TOO_LARGE, detail="Audio file is too large")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.get("/status", response_model=UploadStatusResponse)
async def get_audio_status(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    사용자의 음성 파일 업로드 및 텍스트 변환 진행상황 조회
    """
    try:
        return await transcription_service.get_audio_status(session, user.id)
    except transcription_service.NoAudioData:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No audio data for this user")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_audio(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    """
    음성 파일 업로드 또는 텍스트 변환 중단
    """
    try:
        await transcription_service.cancel_audio(session, user.id)
    except transcription_service.InvalidStatusForCancel:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Cannot cancel at this stage")
    except transcription_service.NoAudioData:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No audio data for this user")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")
