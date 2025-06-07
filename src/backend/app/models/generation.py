from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class GenerationStatus(str, Enum):
    generating = "generating"
    done = "done"
    failed = "failed"
    cancelled = "cancelled"
    archived = "archived"    # 내부에서만 사용되는 상태


class Generation(SQLModel, table=True):
    __tablename__ = "contracts_generations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False, index=True)
    transcription_id: Optional[UUID] = Field(
        foreign_key="contracts_transcriptions.id", nullable=True, index=True
    )

    status: GenerationStatus = Field(nullable=False, index=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )