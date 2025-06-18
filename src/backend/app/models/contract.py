from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Dict, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class Contract(SQLModel, table=True):
    __tablename__ = "contracts_contents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False, index=True)
    generation_id: Optional[UUID] = Field(
        foreign_key="contracts_generations.id", nullable=True, index=True
    )

    contract_type: str = Field(nullable=False, index=True)
    contents: Dict = Field(sa_column=Column(JSONB, nullable=False))
    initial_contents: Dict = Field(sa_column=Column(JSONB, nullable=False))

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )
