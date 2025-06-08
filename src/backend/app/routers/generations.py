from app.core.logger import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_session, get_current_user
from app.schemas.generation import GenerationStatusResponse
from app.services import generations as generation_service

router = APIRouter(prefix="/contracts/generate", tags=["Generations"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def generate_contract(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        await generation_service.create_generation(current_user.id, session)
        logger.info("계약서 생성 요청 완료: user_id=%s", current_user.id)
        return
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

@router.get("/status", response_model=GenerationStatusResponse)
async def get_generation_status(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        result = await generation_service.get_generation_status(current_user.id, session)
        logger.info("계약서 생성 상태 조회 성공: user_id=%s, status=%s", current_user.id, result.status)
        return result
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_generation(
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        await generation_service.cancel_generation(current_user.id, session)
        logger.info("계약서 생성 취소 요청 완료: user_id=%s", current_user.id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )