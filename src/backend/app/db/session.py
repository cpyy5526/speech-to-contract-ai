from typing import AsyncGenerator

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

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

# Session for Celery
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session