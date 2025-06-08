from __future__ import annotations
import logging
logger = logging.getLogger(__name__)

import re, requests
from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jose.exceptions import ExpiredSignatureError, JWTError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
    logger.debug("JWT 발급: access_exp=%s, refresh_exp=%s", access_exp, refresh_exp)

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
        logger.info("JWT 저장 성공: user_id=%s", user.id)

    except SQLAlchemyError:
        logger.error("JWT 저장 실패: user_id=%s", user.id, exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def _send_reset_email(to_email: str, reset_token: str) -> None:
    reset_link = f"{settings.PASSWORD_RESET_URL_BASE}?token={reset_token}"
    message = Mail(
        from_email=settings.EMAIL_FROM_ADDRESS,
        to_emails=to_email,
        subject="[Speech-to-Contract] 비밀번호 재설정",
        html_content=f"""
        <p>아래 링크를 통해 비밀번호를 새로 설정하세요.</p>
        <a href="{reset_link}">{reset_link}</a>
        <p>이 링크는 곧 만료됩니다.</p>
        """,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
    

# --------------------------------------------------------------------------- #
# 공개 서비스 함수
# --------------------------------------------------------------------------- #

async def register(payload: RegisterRequest, session: AsyncSession) -> None:
    """자체 회원가입"""
    logger.info("회원가입 시도: email=%s, username=%s", payload.email, payload.username)

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
        logger.info("회원가입 성공: user_id=%s", user.id)
    except IntegrityError:
        logger.warning("회원가입 실패: 중복된 email 또는 username")
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
    except SQLAlchemyError as e:
        logger.error("DB 오류: %s", e, exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


async def login(
    payload: LoginRequest,
    session: AsyncSession,
) -> TokenResponse:
    """ID/PW 로그인."""
    logger.info("로그인 시도: username=%s", payload.username)
    
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
            logger.warning("로그인 실패: 인증 실패 username=%s", payload.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        result = await _create_and_store_jwts(user, session)
        logger.info("로그인 성공: user_id=%s", user.id)
        return result

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
            logger.warning(
                "소셜 토큰 검증 실패: status_code=%s, response=%s",
                response.status_code, response.text
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid social token",
            )
        data = response.json()
    except requests.RequestException:
        logger.error("소셜 서버 오류: provider=%s", provider, exc_info=True)
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

        result = await _create_and_store_jwts(user, session)
        logger.info("소셜 로그인 성공: provider=%s, user_id=%s", provider, user.id)
        return result
    
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

        logger.info("Access 토큰 재발급 완료: user_id=%s", user.id)
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
    logger.info("비밀번호 재설정 요청 수신: email=%s", payload.email)
    
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing email"
        )
    if not is_valid_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    try:
        user = await session.scalar(
            select(User).where(User.email == payload.email)
        )
        if not user:
            logger.warning(
                "비밀번호 재설정 요청 실패 - 존재하지 않는 이메일: email=%s", payload.email
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        reset_exp = datetime.now(timezone.utc) + timedelta(hours=1)
        reset_token = create_access_token(
            str(user.id), reset_exp, token_type="password_reset"
        )

        await _send_reset_email(user.email, reset_token)
        logger.info("비밀번호 재설정 링크 발송 완료: user_id=%s", user.id)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


async def reset_password(
    payload: ResetPasswordRequest, session: AsyncSession
) -> None:
    """재설정 토큰으로 비밀번호 변경."""
    if not payload.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing token"
        )
    if not payload.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing new password"
        )
    if not is_strong_password(payload.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not meet security requirements"
        )
    try:
        token_data = decode_token(payload.token)
        if token_data.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        user_id_str = token_data.get("sub")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        user = await session.get(User, UUID(user_id_str))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        user.hashed_password = get_password_hash(payload.new_password)
        user.updated_at = datetime.now(timezone.utc)
        logger.info("비밀번호 재설정 성공: user_id=%s", user.id)

        await session.execute(
            update(UserToken)
            .where(UserToken.user_id == user.id)
            .values(is_revoked=True)
        )
        session.add(user)
        await session.commit()

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


async def change_password(
    payload: PasswordChangeRequest,
    current_user: User,
    session: AsyncSession,
) -> None:
    """로그인 사용자 비밀번호 변경."""
    if not payload.old_password or not payload.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing password fields",
        )

    if not is_strong_password(payload.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password does not meet security requirements",
        )

    if not current_user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if not verify_password(
        payload.old_password,
        current_user.hashed_password
    ):
        logger.warning(
            "비밀번호 변경 실패 - 기존 비밀번호 불일치: user_id=%s", current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid current password",
        )

    try:
        current_user.hashed_password = (
            get_password_hash(payload.new_password)
        )
        current_user.updated_at = datetime.now(timezone.utc)
        session.add(current_user)
        await session.commit()
        logger.info("비밀번호 변경 완료: user_id=%s", current_user.id)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )


async def delete_account(
    current_user: User,
    session: AsyncSession,
) -> None:
    """사용자 탈퇴 (계정 + 토큰 전부 삭제)."""
    try:
        await session.execute(
            delete(UserToken).where(UserToken.user_id == current_user.id)
        )
        await session.delete(current_user)
        await session.commit()
        logger.info("계정 삭제 완료: user_id=%s", current_user.id)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )


async def get_me(current_user: User) -> UserResponse:
    """현재 로그인한 사용자 정보."""
    return UserResponse(
        email=current_user.email,
        username=current_user.username
    )


async def logout(current_user: User, session: AsyncSession) -> None:
    """현재 사용자 로그아웃: 모든 토큰 폐기"""
    try:
        await session.execute(
            update(UserToken)
            .where(UserToken.user_id == current_user.id)
            .values(is_revoked=True)
        )
        await session.commit()
        logger.info("로그아웃 완료: user_id=%s", current_user.id)

    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unexpected server error"
        )
