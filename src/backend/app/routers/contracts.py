from app.core.logger import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session, get_current_user
from app.models.user import User
from app.schemas.contract import (
    ContractResponse,
    ContractDetailsResponse,
    ContractUpdateRequest,
    GPTSuggestionResponse,
)
from app.services import contracts as contracts_service

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.get("", response_model=list[ContractResponse])
async def get_contracts_list(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """사용자가 생성한 계약서 목록 조회"""
    try:
        result = await contracts_service.get_contracts_list(
            current_user.id,
            session
        )
        logger.info("계약서 목록 조회 성공: user_id=%s", current_user.id)
        return result
    except HTTPException as e:
        raise e
    except Exception:
        logger.error("계약서 목록 조회 실패: user_id=%s", current_user.id, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.get("/{contract_id}", response_model=ContractDetailsResponse)
async def get_contract(
    contract_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """특정 계약서의 내용 조회"""
    try:
        result = await contracts_service.get_contract(contract_id, session)
        logger.info("계약서 조회 성공: contract_id=%s", contract_id)
        return result
    except HTTPException as e:
        raise e
    except Exception:
        logger.error("계약서 조회 실패: contract_id=%s", contract_id, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.put("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_contract(
    contract_id: str,
    payload: ContractUpdateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """특정 계약서 수정 및 저장"""
    try:
        await contracts_service.update_contract(contract_id, payload, session)
        logger.info("계약서 수정 성공: contract_id=%s", contract_id)
    except HTTPException as e:
        raise e
    except Exception:
        logger.error("계약서 수정 실패: contract_id=%s", contract_id, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.get(
    "/{contract_id}/suggestions",
    response_model=list[GPTSuggestionResponse]
)
async def get_suggestions(
    contract_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """계약서의 빈 필드에 대한 GPT 제안 텍스트 조회"""
    try:
        result = await contracts_service.get_suggestions(contract_id, session)
        logger.info("GPT 제안 조회 성공: contract_id=%s", contract_id)
        return result
    except HTTPException as e:
        raise e
    except Exception:
        logger.error("GPT 제안 조회 실패: contract_id=%s", contract_id, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/{contract_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_contract(
    contract_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """최초 생성된 버전으로 계약서 복원"""
    try:
        await contracts_service.restore_contract(contract_id, session)
        logger.info("계약서 복원 성공: contract_id=%s", contract_id)
    except HTTPException as e:
        raise e
    except Exception:
        logger.error("계약서 복원 실패: contract_id=%s", contract_id, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(
    contract_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """특정 계약서 삭제"""
    try:
        await contracts_service.delete_contract(contract_id, session)
        logger.info("계약서 삭제 성공: contract_id=%s", contract_id)
    except HTTPException as e:
        raise e
    except Exception:
        logger.error("계약서 삭제 실패: contract_id=%s", contract_id, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
