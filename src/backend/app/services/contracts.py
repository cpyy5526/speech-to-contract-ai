from __future__ import annotations

"""Contracts service layer
===========================
Business‑logic helpers that sit between the FastAPI routers and the database layer.
This module *must* remain side‑effect free (no network/GPT calls). GPT‑related
logic lives in the `app.prompts.*` namespace and is *only* invoked here through
placeholder helpers supplied by the prompt‑engineering team.

Every public coroutine either returns a serialisable Pydantic schema instance
(or list thereof) **or** ``None``.  All database mutations follow the canonical
``add → commit → refresh`` sequence and *never* leak SQLAlchemy exceptions –
callers need only catch the custom exceptions exposed in ``__all__``.
"""

from datetime import datetime
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
from app.prompts.keyword_schema import keyword_schema

# ⇢ Prompt‑team utilities – imported, *not* implemented here
from app.prompts.contract_validation import validate_contract_fields  # type: ignore


# ============================================================
# Internal helpers
# ============================================================

# 평탄화된 중첩 dict의 key set 리턴
def flatten_keys(d: dict, prefix: str = "") -> set[str]:
    keys = set()
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.update(flatten_keys(v, full_key))
        else:
            keys.add(full_key)
    return keys

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

        schema = keyword_schema.get(contract.contract_type)
        if schema is None:    # 요청 데이터에 해당하는 계약 유형 정의되지 않음
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unsupported contract type"
            )

        schema_keys = flatten_keys(schema)
        payload_keys = flatten_keys(payload.contents)
        if schema_keys != payload_keys:   # JSON 필드 검사: 모든 key 일치 확인
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing or invalid contract fields"
            )

        contract.contents = payload.contents  # type: ignore[assignment]
        contract.updated_at = datetime.utcnow()

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
            raise ContractNotFound
        await session.delete(contract)
        await session.commit()
    except ContractNotFound:
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc


async def get_suggestions(
    contract_id: str, session: AsyncSession
) -> List[GPTSuggestionResponse]:
    """Return GPT suggestions attached to *contract_id*."""
    try:
        # Existence check (cheaper than a join for clarity here)
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise ContractNotFound

        stmt = select(GptSuggestion).where(GptSuggestion.contract_id == contract.id)
        result = await session.execute(stmt)
        suggestions = result.scalars().all()
        return [_suggestion_to_response(s) for s in suggestions]
    except ContractNotFound:
        raise
    except SQLAlchemyError as exc:
        raise DatabaseError from exc


async def restore_contract(contract_id: str, session: AsyncSession) -> None:
    """Revert ``contents`` to the immutable ``initial_contents`` snapshot."""
    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise ContractNotFound

        if contract.initial_contents is None:
            raise InitialContentsMissing

        contract.contents = contract.initial_contents  # type: ignore[assignment]
        contract.updated_at = datetime.utcnow()

        session.add(contract)
        await session.commit()
        await session.refresh(contract)
    except (ContractNotFound, InitialContentsMissing):
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc
