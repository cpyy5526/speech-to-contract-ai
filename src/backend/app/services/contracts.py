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

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract
from app.models.suggestion import GptSuggestion
from app.schemas.contract import (
    ContractResponse,
    ContractUpdateRequest,
    GPTSuggestionResponse,
)

# ⇢ Prompt‑team utilities – imported, *not* implemented here
from app.prompts.contract_validation import validate_contract_fields  # type: ignore

__all__ = [
    "get_contracts",
    "get_contract",
    "update_contract",
    "delete_contract",
    "get_suggestions",
    "restore_contract",
    # Exceptions
    "ContractNotFound",
    "InvalidContractFields",
    "InitialContentsMissing",
    "DatabaseError",
]


# ============================================================
# Exceptions
# ============================================================


class ContractNotFound(Exception):
    """Raised when the requested contract does not exist."""


class InvalidContractFields(Exception):
    """Raised when a contract JSON is missing required fields."""


class InitialContentsMissing(Exception):
    """Raised when ``initial_contents`` is absent (should never happen)."""


class DatabaseError(Exception):
    """Raised when lower‑level DB errors bubble up."""


# ============================================================
# Internal helpers
# ============================================================


def _contract_to_response(model: Contract) -> ContractResponse:  # noqa: D401
    """Map a :class:`~app.models.contract.Contract` ORM instance → schema."""

    # Enum ➜ str for the Pydantic response model
    status_str = (
        model.generation_status.value  # type: ignore[attr-defined]
        if hasattr(model.generation_status, "value")
        else str(model.generation_status)
    )

    return ContractResponse(
        id=str(model.id),
        contract_type=model.contract_type,
        generation_status=status_str,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _suggestion_to_response(model: GptSuggestion) -> GPTSuggestionResponse:  # noqa: D401
    """Map a :class:`~app.models.suggestion.GptSuggestion` ORM instance → schema."""

    return GPTSuggestionResponse(
        field_path=model.field_path,
        suggestion_text=model.suggestion_text,
    )


# ============================================================
# Public service API – called by the *routers*
# ============================================================


async def get_contracts(session: AsyncSession) -> List[ContractResponse]:
    """Return *all* contracts (caller is expected to handle authorisation)."""
    try:
        stmt = select(Contract).order_by(Contract.created_at.desc())
        result = await session.execute(stmt)
        contracts = result.scalars().all()
        return [_contract_to_response(c) for c in contracts]
    except SQLAlchemyError as exc:  # pragma: no cover – DB layer shield
        raise DatabaseError from exc


async def get_contract(contract_id: str, session: AsyncSession) -> ContractResponse:
    """Return a single contract by *primary‑key* UUID."""
    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise ContractNotFound
        return _contract_to_response(contract)
    except SQLAlchemyError as exc:
        raise DatabaseError from exc


async def update_contract(
    contract_id: str,
    payload: ContractUpdateRequest,
    session: AsyncSession,
) -> None:
    """Persist user edits to an existing contract.

    Steps
    -----
    1. Fetch → 404 if missing
    2. Validate required fields (prompt‑team helper)
    3. Update JSON + timestamp → commit
    """

    try:
        contract = await session.get(Contract, UUID(contract_id))
        if contract is None:
            raise ContractNotFound

        # JSON schema lite‑check (delegated)
        if not validate_contract_fields(contract.contract_type, payload.contents):
            raise InvalidContractFields

        contract.contents = payload.contents  # type: ignore[assignment]
        contract.updated_at = datetime.utcnow()

        session.add(contract)
        await session.commit()
        await session.refresh(contract)
    except (InvalidContractFields, ContractNotFound):
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc


async def delete_contract(contract_id: str, session: AsyncSession) -> None:
    """Hard‑delete a contract record (cascades to suggestions)."""
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
