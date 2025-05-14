"""
app/core/security.py
--------------------

• JWT 생성‧검증 유틸리티
• 비밀번호 해시‧검증 유틸리티

`app/services/auth.py` 등 서비스 계층에서 import 하여 사용합니다.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# ────────────────────────────────────────────────────────────────────────────
# 사설(내부) 상수
# ────────────────────────────────────────────────────────────────────────────
_SECRET_KEY: str = settings.SECRET_KEY
_ALGORITHM: str = settings.ALGORITHM or "HS256"

# 기본 만료(환경 변수가 없을 때 fallback)
_ACCESS_EXPIRE_MINUTES: int = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 15)
_REFRESH_EXPIRE_DAYS: int = getattr(settings, "REFRESH_TOKEN_EXPIRE_DAYS", 7)


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
    평문 ↔️ 해시 일치 여부를 True / False 로 반환합니다.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ────────────────────────────────────────────────────────────────────────────
# JWT 생성
# ────────────────────────────────────────────────────────────────────────────
def _create_token(
    data: Dict[str, Any],
    expires_delta: timedelta,
    token_type: str,
) -> str:
    """
    내부 헬퍼: 공통 JWT 생성.

    Parameters
    ----------
    data
        ``sub`` 등을 포함한 클레임 사전.
    expires_delta
        만료까지의 시간 차이.
    token_type
        "access" / "refresh" 등.
    """
    to_encode: Dict[str, Any] = data.copy()
    to_encode["type"] = token_type
    expire: datetime = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire

    encoded_jwt: str = jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)
    return encoded_jwt


def create_access_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Access Token(JWT) 발급.

    기본 만료는 환경 변수 `ACCESS_TOKEN_EXPIRE_MINUTES` (기본 15분).
    """
    delta = expires_delta or timedelta(minutes=_ACCESS_EXPIRE_MINUTES)
    return _create_token(data, delta, token_type="access")


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Refresh Token(JWT) 발급.

    기본 만료는 환경 변수 `REFRESH_TOKEN_EXPIRE_DAYS` (기본 7일).
    """
    delta = expires_delta or timedelta(days=_REFRESH_EXPIRE_DAYS)
    return _create_token(data, delta, token_type="refresh")


# ────────────────────────────────────────────────────────────────────────────
# JWT 검증
# ────────────────────────────────────────────────────────────────────────────
def verify_token(token: str, token_type: str | None = None) -> Dict[str, Any]:
    """
    JWT 를 디코드하여 payload(dict)를 반환합니다.

    Parameters
    ----------
    token
        검사할 JWT 문자열.
    token_type
        "access" / "refresh" 등 타입을 강제하고 싶을 때 지정.
        지정했는데 일치하지 않으면 `JWTError` 를 발생시킵니다.

    Raises
    ------
    jose.JWTError
        ▸ 서명 불일치  
        ▸ 만료(exp)  
        ▸ 타입 불일치 등
    """
    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            _SECRET_KEY,
            algorithms=[_ALGORITHM],
        )
    except JWTError as exc:
        # 서명 오류, 만료(exp) 등 모든 JWT 예외 재전달
        raise exc

    # 토큰 타입 확인(옵션)
    if token_type and payload.get("type") != token_type:
        raise JWTError("Invalid token type")

    return payload
