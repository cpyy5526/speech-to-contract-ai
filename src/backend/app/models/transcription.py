from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class TranscriptionStatus(str, Enum):
    uploading = "uploading"
    uploaded = "uploaded"
    transcribing = "transcribing"
    done = "done"
    upload_failed = "upload_failed"
    transcription_failed = "transcription_failed"
    cancelled = "cancelled"


class Transcription(SQLModel, table=True):
    __tablename__ = "contracts_transcriptions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False, index=True)

    status: TranscriptionStatus = Field(nullable=False, index=True)
    upload_url: Optional[str] = Field(default=None)
    audio_file: Optional[str] = Field(nullable=True)
    script_file: Optional[str] = Field(nullable=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
