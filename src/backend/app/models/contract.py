from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB

class GenerationStatus(str, Enum):
    generating = "generating"
    done = "done"
    failed = "failed"
    cancelled = "cancelled"

class Contract(SQLModel, table=True):
    __tablename__ = "contracts_contents"
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False)
    contract_type: str
    contents: dict = Field(sa_column=Column(JSONB))
    initial_contents: dict = Field(sa_column=Column(JSONB))
    generation_status: GenerationStatus = Field(
        sa_column=Column(Enum(GenerationStatus, name="gen_status_enum")),
        default=GenerationStatus.generating
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)