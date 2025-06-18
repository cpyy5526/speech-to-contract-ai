"""app/core/dependencies.py
====================================

FastAPI 의존성 주입 모듈
-----------------------
* get_session: 공통 DB 세션 주입
* get_current_user: JWT 검증 후 활성 사용자 주입

다른 라우터/서비스 모듈에서는 다음과 같이 사용합니다.

from fastapi import Depends
from app.core.dependencies import get_session, get_current_user

@router.get("/protected")
async def protected_route(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    ...
"""

from __future__ import annotations
from app.core.logger import logging
logger = logging.getLogger(__name__)

from uuid import UUID
from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import async_session
from app.core.security import decode_token
from app.models.user import User
from app.models.token import UserToken


# ---------------------------------------------------------------------------
# Database Session Dependency
# ---------------------------------------------------------------------------

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a single **AsyncSession**.

    내부에서 ``app.db.session.async_session`` (이미 AsyncGenerator) 을 재사용하여
    세션 객체를 생성합니다. FastAPI 의존성 시스템은 *context-manager* 스타일의
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
    """
    Authorization 헤더의 Bearer Access Token을 검증하고
    유효한 사용자 객체(User)를 반환합니다.
    """

    # 1. 헤더 존재 여부 확인
    if not authorization:
        logger.warning("인증 헤더 누락")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


    # 2. JWT 디코딩 & 검증
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except ExpiredSignatureError:
        logger.warning("JWT 만료")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
        )
    except JWTError:
        logger.warning("JWT 디코딩 실패")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # 3. 사용자 조회
    try:
        user = await session.get(User, UUID(user_id_str))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    # 4. 폐기된 토큰 검사
    try:
        token_record = await session.execute(
            select(UserToken).where(
                UserToken.token == token,
                UserToken.token_type == "access"
            )
        )
        token_obj = token_record.scalars().first()

        if not token_obj or token_obj.is_revoked:
            logger.warning("폐기된 토큰 사용 시도")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception:
        logger.warning("토큰 유효성 검사 중 DB 오류")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return user
