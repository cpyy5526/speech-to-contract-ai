"""
app/services/auth.py
====================

인증(회원, 토큰) 비즈니스-로직 계층.

* 자체 회원가입 / 로그인
* 소셜 로그인(placeholder)
* JWT Access / Refresh 발급·저장·검증
* 비밀번호 재설정(placeholder), 변경, 탈퇴
* 현재 로그인 사용자 조회

외부 부수 효과가 필요한 부분(e-mail 발송, 소셜 토큰 검증 등)은
모두 TODO / placeholder 로 남겨두었으며, 본 모듈은 DB 트랜잭션과
JWT 처리, 비밀번호 해시 등 **서비스 계층** 책임에 집중합니다.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from app.models.token import TokenType, UserToken
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    PasswordChangeRequest,
    PasswordResetRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    SocialLoginRequest,
    TokenResponse,
    UserResponse,
)

# --------------------------------------------------------------------------- #
# 설정 상수
# --------------------------------------------------------------------------- #

ACCESS_TOKEN_EXPIRE_MIN: int = 15  # 15분
REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7일

SUPPORTED_SOCIAL_PROVIDERS: set[str] = {"google", "kakao", "naver"}

# --------------------------------------------------------------------------- #
# 예외 정의 (__all__ 에 노출)
# --------------------------------------------------------------------------- #

class EmailAlreadyRegistered(Exception):
    """이미 가입된 이메일."""

class UsernameAlreadyTaken(Exception):
    """사용 중인 사용자명."""

class InvalidCredentials(Exception):
    """아이디/비밀번호 불일치."""

class InvalidPassword(Exception):
    """비밀번호 규칙 위반 또는 불일치."""

class UserNotFound(Exception):
    """사용자 레코드 없음."""

class InvalidToken(Exception):
    """JWT 형식 오류 등 무효 토큰."""

class ExpiredToken(Exception):
    """만료된 토큰."""

class RevokedToken(Exception):
    """취소(폐기)된 토큰."""

class MissingEmail(Exception):
    """이메일 누락."""

class InvalidEmailFormat(Exception):
    """올바르지 않은 이메일 형식."""

class MissingSocialToken(Exception):
    """소셜 토큰 누락."""

class UnsupportedProvider(Exception):
    """지원하지 않는 소셜 로그인 공급자."""

class InvalidCurrentPassword(Exception):
    """현재 비밀번호 불일치."""

class MissingToken(Exception):
    """Authorization 토큰 누락."""

# 라우터에서 참조하는 추가 예외 -----------------------------
class InvalidFields(Exception):
    """필수 필드 누락."""

class InvalidSocialToken(Exception):
    """소셜 토큰 검증 실패."""

class MissingPassword(Exception):
    """새 비밀번호 누락."""
# ----------------------------------------------------------

__all__: List[str] = [
    # 공개 서비스 함수
    "register",
    "login",
    "verify_social",
    "refresh_token",
    "forgot_password",
    "reset_password",
    "change_password",
    "delete_account",
    "get_me",
    # 예외
    "EmailAlreadyRegistered",
    "UsernameAlreadyTaken",
    "InvalidCredentials",
    "InvalidPassword",
    "UserNotFound",
    "InvalidToken",
    "ExpiredToken",
    "RevokedToken",
    "MissingEmail",
    "InvalidEmailFormat",
    "MissingSocialToken",
    "UnsupportedProvider",
    "InvalidCurrentPassword",
    "MissingToken",
    # 라우터 dependency용 추가 예외
    "InvalidFields",
    "InvalidSocialToken",
    "MissingPassword",
]

# --------------------------------------------------------------------------- #
# 내부 헬퍼
# --------------------------------------------------------------------------- #

def _expires(delta: timedelta) -> datetime:
    return datetime.utcnow() + delta


async def _store_token(
    user_id: UUID,
    token_str: str,
    token_type: TokenType,
    expires_at: datetime,
    session: AsyncSession,
) -> None:
    session.add(
        UserToken(
            user_id=user_id,
            token_type=token_type,
            token=token_str,
            expires_at=expires_at,
        )
    )


async def _create_and_store_jwts(
    user: User,
    session: AsyncSession,
) -> TokenResponse:
    access_payload = {"sub": str(user.id), "type": "access"}
    refresh_payload = {"sub": str(user.id), "type": "refresh"}

    access_token: str = create_access_token(access_payload)
    refresh_token: str = create_refresh_token(refresh_payload)

    try:
        await _store_token(
            user.id,
            access_token,
            TokenType.access,
            _expires(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)),
            session,
        )
        await _store_token(
            user.id,
            refresh_token,
            TokenType.refresh,
            _expires(timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)),
            session,
        )
        await session.commit()
    except SQLAlchemyError as exc:
        await session.rollback()
        raise

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

# --------------------------------------------------------------------------- #
# 공개 서비스 함수
# --------------------------------------------------------------------------- #

async def register(payload: RegisterRequest, session: AsyncSession) -> None:
    """자체 회원가입."""
    try:
        # 이메일‧사용자명 중복 검사
        dup_email = await session.scalar(
            select(User).where(User.email == payload.email)
        )
        if dup_email:
            raise EmailAlreadyRegistered

        dup_username = await session.scalar(
            select(User).where(User.username == payload.username)
        )
        if dup_username:
            raise UsernameAlreadyTaken

        # TODO: 비밀번호 강도 검사 → InvalidPassword raise
        hashed_pw = get_password_hash(payload.password)

        user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=hashed_pw,
        )
        session.add(user)
        await session.commit()

    except (EmailAlreadyRegistered, UsernameAlreadyTaken, InvalidPassword):
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise
    # 반환값 없음 (HTTP 204)


async def login(payload: LoginRequest, session: AsyncSession) -> TokenResponse:
    """ID/PW 로그인."""
    try:
        user: User | None = await session.scalar(
            select(User).where(User.username == payload.username)
        )
        if not user or not user.hashed_password:
            raise InvalidCredentials
        if not verify_password(payload.password, user.hashed_password):
            raise InvalidCredentials

        return await _create_and_store_jwts(user, session)

    except InvalidCredentials:
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def verify_social(
    payload: SocialLoginRequest, session: AsyncSession
) -> TokenResponse:
    """소셜 로그인(placeholder 검증)."""
    provider = payload.provider.lower()
    if provider not in SUPPORTED_SOCIAL_PROVIDERS:
        raise UnsupportedProvider
    if not payload.social_token:
        raise MissingSocialToken

    # TODO: 실제 소셜 토큰 검증 → InvalidSocialToken raise
    # 여기서는 토큰을 단순 해시하여 고유 값 생성
    pseudo_id: str = str(abs(hash(payload.social_token)))

    try:
        user: User | None = await session.scalar(
            select(User).where(
                (User.provider == provider)
                & (User.provider_user_id == pseudo_id)
            )
        )

        if user is None:
            # 신규 사용자 생성
            pseudo_email = EmailStr(f"{provider}_{pseudo_id}@example.com")
            pseudo_username = f"{provider}_user_{pseudo_id[:6]}"
            user = User(
                email=pseudo_email,
                username=pseudo_username,
                provider=provider,
                provider_user_id=pseudo_id,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return await _create_and_store_jwts(user, session)

    except (UnsupportedProvider, MissingSocialToken):
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def refresh_token(
    payload: RefreshTokenRequest, session: AsyncSession
) -> TokenResponse:
    """Refresh 토큰으로 Access 재발급."""
    try:
        token_data = verify_token(payload.refresh_token, token_type="refresh")
        user_id_str: str | None = token_data.get("sub")  # type: ignore[index]
        if not user_id_str:
            raise InvalidToken

        token_in_db: UserToken | None = await session.scalar(
            select(UserToken).where(UserToken.token == payload.refresh_token)
        )
        if not token_in_db:
            raise InvalidToken
        if token_in_db.is_revoked:
            raise RevokedToken
        if token_in_db.expires_at < datetime.utcnow():
            raise ExpiredToken

        user: User | None = await session.get(User, UUID(user_id_str))
        if not user:
            raise UserNotFound

        # 새 Access Token 발급
        new_access_token = create_access_token({"sub": user_id_str, "type": "access"})
        await _store_token(
            user.id,
            new_access_token,
            TokenType.access,
            _expires(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)),
            session,
        )
        await session.commit()

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=payload.refresh_token,
        )

    except (InvalidToken, RevokedToken, ExpiredToken, UserNotFound):
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def forgot_password(
    payload: PasswordResetRequest, session: AsyncSession
) -> None:
    """비밀번호 재설정 링크 이메일 발송."""
    if not payload.email:
        raise MissingEmail
    try:
        user: User | None = await session.scalar(
            select(User).where(User.email == payload.email)
        )
        if not user:
            raise UserNotFound

        reset_token = create_access_token(
            {"sub": str(user.id), "type": "password_reset"},
        )

        # TODO: 실제 이메일 전송 (비동기 큐 또는 외부 서비스)
        # send_reset_email(user.email, reset_token)

    except (MissingEmail, UserNotFound):
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def reset_password(
    payload: ResetPasswordRequest, session: AsyncSession
) -> None:
    """재설정 토큰으로 비밀번호 변경."""
    if not payload.new_password:
        raise MissingPassword
    try:
        token_data = verify_token(payload.token, token_type="access")
        user_id_str: str | None = token_data.get("sub")  # type: ignore[index]
        if not user_id_str:
            raise InvalidToken

        user: User | None = await session.get(User, UUID(user_id_str))
        if not user:
            raise UserNotFound

        user.hashed_password = get_password_hash(payload.new_password)
        user.updated_at = datetime.utcnow()

        # 기존 토큰 모두 폐기
        await session.execute(
            update(UserToken)
            .where(UserToken.user_id == user.id)
            .values(is_revoked=True)
        )
        session.add(user)
        await session.commit()

    except (InvalidToken, MissingPassword, UserNotFound):
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def change_password(
    payload: PasswordChangeRequest, session: AsyncSession
) -> None:
    """로그인 사용자 비밀번호 변경."""
    user_id: UUID | None = session.info.get("current_user_id")  # type: ignore[arg-type]
    if not user_id:
        raise MissingToken

    try:
        user: User | None = await session.get(User, user_id)
        if not user or not user.hashed_password:
            raise UserNotFound

        if not verify_password(payload.old_password, user.hashed_password):
            raise InvalidCurrentPassword

        user.hashed_password = get_password_hash(payload.new_password)
        user.updated_at = datetime.utcnow()
        session.add(user)
        await session.commit()

    except (MissingToken, UserNotFound, InvalidCurrentPassword):
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def delete_account(session: AsyncSession) -> None:
    """사용자 탈퇴 (계정 + 토큰 전부 삭제)."""
    user_id: UUID | None = session.info.get("current_user_id")  # type: ignore[arg-type]
    if not user_id:
        raise MissingToken

    try:
        user: User | None = await session.get(User, user_id)
        if not user:
            raise UserNotFound

        # 토큰 일괄 삭제
        await session.execute(
            delete(UserToken).where(UserToken.user_id == user.id)
        )
        # 사용자 삭제
        await session.delete(user)
        await session.commit()

    except (MissingToken, UserNotFound):
        raise
    except SQLAlchemyError:
        await session.rollback()
        raise


async def get_me(session: AsyncSession) -> UserResponse:
    """현재 로그인한 사용자 정보."""
    user_id: UUID | None = session.info.get("current_user_id")  # type: ignore[arg-type]
    if not user_id:
        raise MissingToken

    try:
        user: User | None = await session.get(User, user_id)
        if not user:
            raise UserNotFound

        return UserResponse(email=user.email, username=user.username)

    except (MissingToken, UserNotFound):
        raise
    except SQLAlchemyError:
        raise
