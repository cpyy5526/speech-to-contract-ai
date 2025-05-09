from sqlmodel import SQLModel

# Import models so their metadata is registered
from app.models import (  # noqa: F401
    user,          # noqa
    token,         # noqa
    contract,      # noqa
    transcription, # noqa
    suggestion,    # noqa
)

from app.db.session import engine


async def init_db() -> None:
    """애플리케이션 시작 시 호출하여 테이블을 생성합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
