from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Dict

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class GenerationStatus(str, Enum):
    generating = "generating"
    done = "done"
    failed = "failed"
    cancelled = "cancelled"


class Contract(SQLModel, table=True):
    __tablename__ = "contracts_contents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False, index=True)

    contract_type: str = Field(nullable=False, index=True)
    contents: Dict = Field(sa_column=Column(JSONB), nullable=False)
    initial_contents: Dict = Field(sa_column=Column(JSONB), nullable=False)

    generation_status: GenerationStatus = Field(nullable=False, index=True)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
