"""app/core/dependencies.py
====================================

FastAPI 의존성 주입 모듈
-----------------------
* **get_session**  ― 공통 DB 세션 주입
* **get_current_user** ― JWT 검증 후 활성 사용자 주입

다른 라우터/서비스 모듈에서는 다음과 같이 사용합니다.

```python
from fastapi import Depends
from app.core.dependencies import get_session, get_current_user

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ...
```
"""

from __future__ import annotations

import uuid
from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.core.security import verify_token
from app.models.user import User

__all__ = [
    "get_session",
    "get_current_user",
]

# ---------------------------------------------------------------------------
# Database Session Dependency
# ---------------------------------------------------------------------------

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a single **AsyncSession**.

    내부에서 ``app.db.session.async_session`` (이미 AsyncGenerator) 을 재사용하여
    세션 객체를 생성합니다. FastAPI 의존성 시스템은 *context‑manager* 스타일의
    ``async for`` 루프를 자동으로 처리하므로, 다음과 같이 래핑하여 사용합니다.
    """

    async for session in async_session():
        yield session

# ---------------------------------------------------------------------------
# Current User Dependency
# ---------------------------------------------------------------------------

async def get_current_user(
    authorization: str | None = Header(None, alias="Authorization"),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Extract and validate the *Bearer* token, returning the active :class:`User`.

    Flow
    ----
    1. ``Authorization: Bearer <JWT>`` 헤더 파싱
    2. :func:`app.core.security.verify_token` 으로 디코딩 (access token 강제)
    3. ``sub``(사용자 ID) 기반으로 DB 조회 → 비활성화 사용자 차단
    4. 세션 컨텍스트에 ``current_user_id`` 저장 (서비스 계층에서 활용)

    Raises
    ------
    fastapi.HTTPException
        * 401 – 토큰 누락 / 형식 오류 / 만료 · 위조 등
    """

    # 1) 헤더 존재 여부 확인
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2) JWT 디코딩 & 검증
    try:
        payload = verify_token(token, token_type="access")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str: str | None = payload.get("sub")  # type: ignore[index]
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3) 사용자 조회
    try:
        user: User | None = await session.get(User, uuid.UUID(user_id_str))
    except ValueError:  # 잘못된 UUID 형식
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4) 서비스 계층 편의를 위해 세션 컨텍스트에 저장
    session.info["current_user_id"] = user.id  # type: ignore[index]

    return user
