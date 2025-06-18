from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

import bcrypt
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from app.core.config import settings
from app.core.logger import logging
logger = logging.getLogger(__name__)


# ────────────────────────────────────────────────────────────────────────────
# 비밀번호 해시 / 검증
# ────────────────────────────────────────────────────────────────────────────
def get_password_hash(password: str) -> str:
    """
    주어진 평문 비밀번호를 bcrypt salt 로 해시하여 반환합니다.
    """
    hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문-해시 일치 여부를 True / False 로 반환합니다.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ────────────────────────────────────────────────────────────────────────────
# JWT 생성
# ────────────────────────────────────────────────────────────────────────────
def _create_token(
    subject: str,
    expires_at: datetime,
    token_type: str,
) -> str:
    """
    subject: 토큰 소유자 ID (user_id 등)
    token_type: "access" | "refresh"
    """
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": expires_at,
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_access_token(subject: str, expires_at: datetime) -> str:
    return _create_token(subject, expires_at, token_type="access")


def create_refresh_token(subject: str, expires_at: datetime) -> str:
    return _create_token(subject, expires_at, token_type="refresh")


# ────────────────────────────────────────────────────────────────────────────
# JWT 검증
# ────────────────────────────────────────────────────────────────────────────
def decode_token(token: str) -> Dict[str, Any]:
    """
    JWT 를 디코드하여 payload(dict)를 반환합니다.
    """
    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        logger.info("토큰 디코딩 성공: sub=%s, exp=%s", payload.get("sub"), payload.get("exp"))
        return payload
    except ExpiredSignatureError:
        logger.warning("토큰 만료됨: %s", token, exc_info=True)
        raise
    except JWTError:
        logger.warning("토큰 디코딩 실패: %s", token, exc_info=True)
        raise
