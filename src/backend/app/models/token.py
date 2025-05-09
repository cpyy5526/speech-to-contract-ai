from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import Optional


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class UserToken(SQLModel, table=True):
    __tablename__ = "auth_user_tokens"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="auth_users.id", nullable=False, index=True)

    token_type: TokenType = Field(nullable=False, index=True)
    token: str = Field(nullable=False)
    is_revoked: bool = Field(default=False, nullable=False)
    expires_at: datetime = Field(nullable=False)

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
