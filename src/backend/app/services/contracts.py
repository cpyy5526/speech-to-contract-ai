from __future__ import annotations

"""Contracts service layer:
Business-logic helpers that sit between the FastAPI routers and the database layer.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.suggestion import GptSuggestion
from app.schemas.contract import (
    ContractResponse,
    ContractDetailsResponse,
    ContractUpdateRequest,
    GPTSuggestionResponse,
)
from app.prompts.keyword_schema import matches_schema


# ============================================================
# Internal helpers
# ============================================================

def _contract_to_response(model: Contract) -> ContractResponse:  # noqa: D401
    """Map a :class:`~app.models.contract.Contract` ORM instance -> schema."""

    return ContractResponse(
        id=str(model.id),
        contract_type=model.contract_type,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )

def _contract_details_to_response(model: Contract) -> ContractDetailsResponse:
    return ContractDetailsResponse(
        contract_type=model.contract_type,
        contents=model.contents,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )

def _suggestion_to_response(model: GptSuggestion) -> GPTSuggestionResponse:  # noqa: D401
    """Map a :class:`~app.models.suggestion.GptSuggestion` ORM instance -> schema."""

    return GPTSuggestionResponse(
        field_path=model.field_path,
        suggestion_text=model.suggestion_text,
    )


# ============================================================
# Public service API – called by the *routers*
# ============================================================

async def get_contracts_list(
        user_id: UUID,
        session: AsyncSession
) -> List[ContractResponse]:
    """Return *all* contracts (caller is expected to handle authorisation)."""
    try:
        stmt = (
            select(Contract)
            .where(Contract.user_id == user_id)
            .order_by(Contract.created_at.desc())
        )
        result = await session.execute(stmt)
        contracts = result.scalars().all()
        return [_contract_to_response(c) for c in contracts]
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database query failed"
        )


async def get_contract(
    contract_id: str,
    session: AsyncSession
) -> ContractDetailsResponse:
    """Return a single contract by *primary-key* UUID."""
    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        return _contract_details_to_response(contract)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database query failed"
        )


async def update_contract(
    contract_id: str,
    payload: ContractUpdateRequest,
    session: AsyncSession,
) -> None:
    """Persist user edits to an existing contract."""

    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:   # 대상 계약서 없음
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )

        # JSON 필드 검사: 요청 데이터의 모든 key 일치 확인
        if not matches_schema(contract.contract_type, payload.contents):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing or invalid contract fields"
            )

        contract.contents = payload.contents  # type: ignore[assignment]
        contract.updated_at = datetime.now(timezone.utc)

        session.add(contract)
        await session.commit()
        await session.refresh(contract)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database update failed"
        )


async def delete_contract(contract_id: str, session: AsyncSession) -> None:
    """Hard-delete a contract record (cascades to suggestions)."""
    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        await session.delete(contract)
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database update failed"
        )


async def get_suggestions(
    contract_id: str, session: AsyncSession
) -> List[GPTSuggestionResponse]:
    """Return GPT suggestions attached to *contract_id*."""
    try:
        # Existence check (cheaper than a join for clarity here)
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )

        stmt = select(GptSuggestion).where(GptSuggestion.contract_id == contract.id)
        result = await session.execute(stmt)
        suggestions = result.scalars().all()
        return [_suggestion_to_response(s) for s in suggestions]
    
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database query failed"
        )


async def restore_contract(contract_id: str, session: AsyncSession) -> None:
    """Revert ``contents`` to the immutable ``initial_contents`` snapshot."""
    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
        if contract.initial_contents is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Initial contents missing"
            )

        contract.contents = contract.initial_contents  # type: ignore[assignment]
        contract.updated_at = datetime.now(timezone.utc)

        session.add(contract)
        await session.commit()
        await session.refresh(contract)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database update failed"
        )
