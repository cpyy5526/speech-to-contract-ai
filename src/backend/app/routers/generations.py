from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.generations import GenerationStatusResponse
from app.services import generations as generation_service
from app.core.dependencies import get_session

router = APIRouter(prefix="/contracts/generate", tags=["Generations"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def generate_contract(session: AsyncSession = Depends(get_session)):
    """
    변환된 텍스트를 바탕으로 계약서 생성 시작
    """
    try:
        return await generation_service.generate_contract(session)
    except generation_service.TranscriptionNotReady:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Transcription not ready")
    except generation_service.NoAudioData:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No audio data for this user")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.get("/status", response_model=GenerationStatusResponse)
async def get_generation_status(session: AsyncSession = Depends(get_session)):
    """
    현재 사용자의 계약서 생성 진행상황 조회
    """
    try:
        return await generation_service.get_generation_status(session)
    except generation_service.NoGenerationInProgress:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No contract generation in progress")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_generation(session: AsyncSession = Depends(get_session)):
    """
    계약서 생성 프로세스 중단
    """
    try:
        await generation_service.cancel_generation(session)
    except generation_service.NoGenerationInProgress:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No contract generation in progress")
    except generation_service.CannotCancelGeneration:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Cannot cancel generation at this stage")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")
