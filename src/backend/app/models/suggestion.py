from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class GptSuggestion(SQLModel, table=True):
    __tablename__ = "gpt_suggestions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    contract_id: UUID = Field(foreign_key="contracts_contents.id", nullable=False, index=True)

    field_path: str = Field(nullable=False)
    suggestion_text: str = Field(nullable=False)

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
    )
