from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


class GptSuggestion(SQLModel, table=True):
    __tablename__ = "gpt_suggestions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    contract_id: UUID = Field(foreign_key="contracts_contents.id", nullable=False, index=True)

    field_path: str = Field(nullable=False)
    suggestion_text: str = Field(nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
