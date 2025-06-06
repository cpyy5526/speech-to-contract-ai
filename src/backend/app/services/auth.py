from __future__ import annotations

import re, requests
from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose.exceptions import ExpiredSignatureError, JWTError

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    decode_token,
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
    TokenRefreshResponse,
    UserResponse,
)


# --------------------------------------------------------------------------- #
# 내부 헬퍼
# --------------------------------------------------------------------------- #

def is_strong_password(password: str) -> bool:
    return bool(
        re.fullmatch(
            r"(?=.*[a-zA-Z])"
            r"(?=.*\d)"
            r"(?=.*[!@#$%^&*()_\-+=])"
            r"[A-Za-z\d!@#$%^&*()_\-+=]{8,20}",
            password
        )
    )

def is_valid_email(email: str) -> bool:
    return bool(
        re.fullmatch(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            email)
    )

async def _stage_token(
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
    access_exp = (
        datetime.now(timezone.utc) 
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_exp = (
        datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    access_token = create_access_token(str(user.id), access_exp)
    refresh_token = create_refresh_token(str(user.id), refresh_exp)

    try:
        await _stage_token(
            user.id,
            access_token,
            TokenType.access,
            access_exp,
            session,
        )
        await _stage_token(
            user.id,
            refresh_token,
            TokenType.refresh,
            refresh_exp,
            session,
        )
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

# --------------------------------------------------------------------------- #
# 공개 서비스 함수
# --------------------------------------------------------------------------- #

async def register(payload: RegisterRequest, session: AsyncSession) -> None:
    """자체 회원가입"""
    # 필드 누락 확인
    if not payload.email or not payload.username or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or invalid fields"
        )

    # 이메일 주소 형식 검사
    if not is_valid_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or invalid fields"
        )
    
    # username 형식 검사
    if not re.fullmatch(r"^[a-zA-Z0-9_]{4,20}$", payload.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or invalid fields"
        )

    # 비밀번호 형식 검사
    if not is_strong_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not meet security requirements"
        )
    
    hashed_pw = get_password_hash(payload.password)
    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hashed_pw,
    )

    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        email_exists = await session.scalar(
            select(User).where(User.email == payload.email)
        )
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        username_exists = await session.scalar(
            select(User).where(User.username == payload.username)
        )
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


async def login(payload: LoginRequest, session: AsyncSession) -> TokenResponse:
    """ID/PW 로그인."""
    if not payload.username or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing username or password"
        )

    try:
        user = await session.scalar(
            select(User).where(User.username == payload.username)
        )
        if not user or not verify_password(
            payload.password,
            user.hashed_password or ""
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        return await _create_and_store_jwts(user, session)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    


async def verify_social(
    payload: SocialLoginRequest, session: AsyncSession
) -> TokenResponse:
    """소셜 로그인(placeholder 검증)."""
    provider = payload.provider.lower()
    if provider not in settings.SUPPORTED_SOCIAL_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported provider",
        )
    
    if not payload.social_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing social token",
        )

    # Google 토큰 검증
    url = (
        f"{settings.GOOGLE_TOKENINFO_ENDPOINT}"
        f"?id_token={payload.social_token}"
    )
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid social token",
            )
        data = response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Social server error",
        )

    google_user_id = data.get("sub")
    if not google_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid social token",
        )

    # 사용자 조회
    try:
        user = await session.scalar(
            select(User).where(
                (User.provider == provider)
                & (User.provider_user_id == google_user_id)
            )
        )

        # 최초 로그인 시 사용자 등록
        if user is None:
            email = data.get("email")    # "abc@gmail.com"
            if not email:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid social token"
                )
            user = User(
                email=email,
                username=email,
                provider=provider,
                provider_user_id=google_user_id,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return await _create_and_store_jwts(user, session)
    
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )


async def refresh_token(
    payload: RefreshTokenRequest, session: AsyncSession
) -> TokenRefreshResponse:
    """Refresh 토큰으로 Access 재발급."""
    # 1. Refresh 토큰 디코드 및 기본 검증
    try:
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        user_id_str: str | None = token_data.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # 2. DB에서 토큰 조회 및 상태 확인
    try:
        token_in_db = await session.scalar(
            select(UserToken)
            .where(UserToken.token == payload.refresh_token)
        )
        if not token_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        if token_in_db.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Revoked token"
            )
        if token_in_db.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token"
            )

        user = await session.get(User, UUID(user_id_str))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        # 3. 새 Access 토큰 발급
        access_exp = (
            datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_access_token = create_access_token(str(user.id), access_exp)

        await _stage_token(
            user.id,
            new_access_token,
            TokenType.access,
            access_exp,
            session,
        )
        await session.commit()

        return TokenRefreshResponse(
            access_token=new_access_token
        )

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


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
        token_data = decode_token(payload.token, token_type="access")
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
