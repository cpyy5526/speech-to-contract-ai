from pydantic import BaseModel, EmailStr
from typing import Optional

# Request Models

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "user123",
                "password": "your_password"
            }
        }

class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "user123",
                "password": "your_password"
            }
        }

class SocialLoginRequest(BaseModel):
    provider: str
    social_token: str

    class Config:
        schema_extra = {
            "example": {
                "provider": "google",
                "social_token": "social_login_token_here"
            }
        }

class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "refresh_token_here"
            }
        }

class PasswordResetRequest(BaseModel):
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    class Config:
        schema_extra = {
            "example": {
                "token": "reset_token_here",
                "new_password": "new_password"
            }
        }

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

    class Config:
        schema_extra = {
            "example": {
                "old_password": "current_password",
                "new_password": "new_password"
            }
        }


# Response Models

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        schema_extra = {
            "example": {
                "access_token": "jwt_access_token_here",
                "refresh_token": "jwt_refresh_token_here",
                "token_type": "bearer"
            }
        }

class UserResponse(BaseModel):
    email: EmailStr
    username: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "user123"
            }
        }
