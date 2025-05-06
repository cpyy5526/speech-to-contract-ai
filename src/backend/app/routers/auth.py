from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest, PasswordResetRequest, PasswordChangeRequest
from app.services import auth as auth_service
from app.core.dependencies import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

# /user/me 하나만 정의되어 있음, 별도 파일로 분리하지 않고 현재 코드에 포함. 따로 구분
user_router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_session)):
    """
    사용자 회원가입 처리
    """
    try:
        await auth_service.register(payload, session)
    except auth_service.EmailAlreadyRegistered:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already registered")
    except auth_service.UsernameAlreadyTaken:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Username already taken")
    except auth_service.InvalidFields:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing or invalid fields")
    except auth_service.InvalidPassword:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Password does not meet security requirements")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    사용자 로그인을 처리하고 JWT 토큰 반환
    """
    try:
        return await auth_service.login(payload, session)
    except auth_service.InvalidCredentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/verify-social", response_model=TokenResponse)
async def verify_social(payload: SocialLoginRequest, session: AsyncSession = Depends(get_session)):
    """
    소셜 로그인 토큰을 검증하고 JWT 토큰 반환
    """
    try:
        return await auth_service.verify_social(payload, session)
    except auth_service.UnsupportedProvider:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Unsupported provider")
    except auth_service.MissingSocialToken:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing social token")
    except auth_service.InvalidSocialToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid social token")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/token/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshTokenRequest, session: AsyncSession = Depends(get_session)):
    """
    Refresh Token을 사용해 새로운 Access Token 발급
    """
    try:
        return await auth_service.refresh_token(payload, session)
    except auth_service.InvalidToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except auth_service.ExpiredToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@user_router.get("/me", response_model=UserResponse)
async def get_me(session: AsyncSession = Depends(get_session)):
    """
    현재 로그인한 사용자 정보를 반환
    """
    try:
        return await auth_service.get_me(session)
    except auth_service.MissingToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    except auth_service.InvalidToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except auth_service.ExpiredToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/password/forgot", status_code=status.HTTP_204_NO_CONTENT)
async def forgot_password(payload: PasswordResetRequest, session: AsyncSession = Depends(get_session)):
    """
    비밀번호 찾기 요청 처리하고 이메일로 링크 전송
    """
    try:
        await auth_service.forgot_password(payload, session)
    except auth_service.InvalidEmailFormat:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid email format")
    except auth_service.MissingEmail:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing email")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/password/reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(payload: ResetPasswordRequest, session: AsyncSession = Depends(get_session)):
    """
    비밀번호 재설정 링크를 통한 새 비밀번호를 설정
    """
    try:
        await auth_service.reset_password(payload, session)
    except auth_service.InvalidToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    except auth_service.MissingPassword:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Missing new password")
    except auth_service.InvalidPassword:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Password does not meet security requirements")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.post("/password/change", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(payload: PasswordChangeRequest, session: AsyncSession = Depends(get_session)):
    """
    로그인한 사용자의 비밀번호 변경
    """
    try:
        await auth_service.change_password(payload, session)
    except auth_service.InvalidToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except auth_service.ExpiredToken:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except auth_service.InvalidPassword:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Password does not meet security requirements")
    except auth_service.InvalidCurrentPassword:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid current password")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")


@router.delete("/delete-account", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(session: AsyncSession = Depends(get_session)):
    """
    로그인한 사용자의 계정 삭제
    """
    try:
        await auth_service.delete_account(session)
    except auth_service.UserNotFound:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not found")
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")
