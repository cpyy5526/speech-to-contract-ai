from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

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

@router.get("/", response_model=list[ContractResponse])
async def get_contracts_list(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    사용자가 생성한 계약서 목록 조회
    """
    try:
        return await contracts_service.get_contracts_list(current_user.id, session)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.get("/{contract_id}", response_model=ContractDetailsResponse)
async def get_contract(contract_id: str, session: AsyncSession = Depends(get_session)):
    """
    특정 계약서의 내용 조회
    """
    try:
        return await contracts_service.get_contract(contract_id, session)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.put("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_contract(contract_id: str, payload: ContractUpdateRequest, session: AsyncSession = Depends(get_session)):
    """
    특정 계약서 수정 및 저장
    """
    try:
        await contracts_service.update_contract(contract_id, payload, session)
    except contracts_service.ContractNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Contract not found")
    except contracts_service.InvalidContractFields:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing or invalid contract fields")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.get("/{contract_id}/suggestions")
async def get_suggestions(contract_id: str, session: AsyncSession = Depends(get_session)):
    """
    계약서의 빈 필드에 대한 GPT 제안 텍스트 조회
    """
    try:
        return await contracts_service.get_suggestions(contract_id, session)
    except contracts_service.ContractNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Contract not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/{contract_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_contract(contract_id: str, session: AsyncSession = Depends(get_session)):
    """
    최초 생성된 버전으로 계약서 복원
    """
    try:
        await contracts_service.restore_contract(contract_id, session)
    except contracts_service.ContractNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Contract not found")
    except contracts_service.InitialContentsMissing:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Initial contents missing")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(contract_id: str, session: AsyncSession = Depends(get_session)):
    """
    특정 계약서 삭제
    """
    try:
        await contracts_service.delete_contract(contract_id, session)
    except contracts_service.ContractNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Contract not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")
