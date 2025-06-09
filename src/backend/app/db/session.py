from typing import AsyncGenerator

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings

# Async SQLAlchemy engine (PostgreSQL)
engine = create_async_engine(
    settings.DATABASE_URL,  # e.g. "postgresql+asyncpg://user:pass@host:port/db"
    echo=False,
    future=True,
    pool_pre_ping=True,
)

# AsyncSession factory
async_session_factory: sessionmaker[AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# FastAPI dependency
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


# --- Sync SQLAlchemy 세션 설정 (Celery 등 외부 프로세스 환경) ---

sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,  # e.g. "postgresql://user:pass@host:port/db"
    echo=False,
    future=True,
    pool_pre_ping=True,
)

sync_session_factory = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autoflush=False,
)

def get_sync_session() -> Session:
    return sync_session_factory()