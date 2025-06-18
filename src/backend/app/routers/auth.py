from app.core.logger import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services import auth as auth_service
from app.core.dependencies import get_session, get_current_user
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


router = APIRouter(prefix="/auth", tags=["Auth"])

# /user/me 하나만 정의되어 있음, 별도 파일로 분리하지 않고 현재 코드에 포함. 따로 구분
user_router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    """사용자 회원가입 처리"""
    try:
        await auth_service.register(payload, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/register: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """사용자 로그인을 처리하고 JWT 토큰 반환"""
    try:
        return await auth_service.login(payload, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/login: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/verify-social", response_model=TokenResponse)
async def verify_social(
    payload: SocialLoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """소셜 로그인 토큰을 검증하고 JWT 토큰 반환"""
    try:
        return await auth_service.verify_social(payload, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/verify-social: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/token/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    payload: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session)
):
    """Refresh Token을 사용해 새로운 Access Token 발급"""
    try:
        return await auth_service.refresh_token(payload, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/token/refresh: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@user_router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    현재 로그인한 사용자 정보를 반환
    """
    try:
        return await auth_service.get_me(current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /user/me: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/password/forgot", status_code=status.HTTP_204_NO_CONTENT)
async def forgot_password(
    payload: PasswordResetRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    비밀번호 찾기 요청 처리하고 이메일로 링크 전송
    """
    try:
        await auth_service.forgot_password(payload, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/password/forgot: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/password/reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    payload: ResetPasswordRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    비밀번호 재설정 링크를 통한 새 비밀번호를 설정
    """
    try:
        await auth_service.reset_password(payload, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/password/reset: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/password/change", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """로그인한 사용자의 비밀번호 변경"""
    try:
        await auth_service.change_password(payload, current_user, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/password/change: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    로그인된 사용자의 모든 토큰을 무효화하고 세션 종료
    """
    try:
        await auth_service.logout(current_user, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/logout: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )


@router.delete("/delete-account", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    로그인한 사용자의 계정 삭제
    """
    try:
        await auth_service.delete_account(current_user, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Unexpected error in /auth/delete-account: %s", e, exc_info=True)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
