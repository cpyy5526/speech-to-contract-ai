from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class UserToken(SQLModel, table=True):
    __tablename__ = "auth_user_tokens"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False, index=True)

    token_type: TokenType = Field(nullable=False, index=True)
    token: str = Field(nullable=False, unique=True)
    is_revoked: bool = Field(default=False, nullable=False)
    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
    )
