"""
애플리케이션 전역 설정 모듈
==========================
- .env 파일을 우선적으로 로드하여 환경변수를 읽어옵니다.
- Pydantic BaseSettings(미사용): 순수 파이썬 클래스로 선언합니다.
- settings = Settings()  단일 인스턴스를 내보내 FastAPI, Celery 등에서 import하여 사용합니다.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


class Settings:
    """
    프로젝트 전역 설정 모음.

    Notes
    -----
    - `.env` 파일이 존재하지 않을 경우에도 `os.environ`에 이미
      설정된 값이 있으면 그대로 사용합니다.
    - 정수형‧불리언형 환경변수는 `int()`, `.lower()` 등을 통해
      형 변환/정규화를 수행했습니다.
    """

    def __init__(self) -> None:
        # ------------------------------------------------------------------ #
        # .env 로드
        # ------------------------------------------------------------------ #
        # backend/ 최상위 경로(= 현재 파일에서 두 단계 상위)를 기본 위치로 가정
        base_dir = Path(__file__).resolve().parent.parent.parent
        env_path = base_dir / ".env"
        load_dotenv(dotenv_path=env_path, override=False)

        # ------------------------------------------------------------------ #
        # 애플리케이션
        # ------------------------------------------------------------------ #
        self.APP_NAME: str = os.getenv("APP_NAME", "speech-to-contract")
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"}

        # ------------------------------------------------------------------ #
        # Database (PostgreSQL‧SQLModel)
        # ------------------------------------------------------------------ #
        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://user:password@localhost:5432/contract_db",
        )

        # ------------------------------------------------------------------ #
        # JWT / 보안
        # ------------------------------------------------------------------ #
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
        )
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = int(
            os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
        )

        # ------------------------------------------------------------------ #
        # Celery (비동기 작업 큐)
        # ------------------------------------------------------------------ #
        self.CELERY_BROKER_URL: str = os.getenv(
            "CELERY_BROKER_URL", "redis://localhost:6379/0"
        )
        self.CELERY_RESULT_BACKEND: str = os.getenv(
            "CELERY_RESULT_BACKEND", self.CELERY_BROKER_URL
        )
        # 태스크 타임아웃 등 옵션이 필요하면 추가 선언

        # ------------------------------------------------------------------ #
        # Redis (캐시‧세션 등)
        # ------------------------------------------------------------------ #
        self.REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/1")

        # ------------------------------------------------------------------ #
        # OpenAI / Whisper
        # ------------------------------------------------------------------ #
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_API_BASE: str = os.getenv(
            "OPENAI_API_BASE", "https://api.openai.com/v1"
        )
        self.OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # ------------------------------------------------------------------ #
        # 파일 업로드 경로
        # ------------------------------------------------------------------ #
        self.AUDIO_UPLOAD_DIR: str = os.getenv("AUDIO_UPLOAD_DIR", "uploads/audio")
        self.TEXT_UPLOAD_DIR: str = os.getenv("TEXT_UPLOAD_DIR", "uploads/text")

        # 디렉터리 자동 생성(없으면)
        Path(self.AUDIO_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.TEXT_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

        # ------------------------------------------------------------------ #
        # 음성파일 형식 및 크기 제한
        # ------------------------------------------------------------------ #
        exts = os.getenv("ALLOWED_AUDIO_EXTENSIONS", ".mp3,.wav")
        self.ALLOWED_AUDIO_EXTENSIONS: set[str] = {
            ext.strip().lower() for ext in exts.split(",") if ext.strip()
        }
        self.MAX_UPLOAD_SIZE_BYTES: int = int(
            os.getenv("MAX_UPLOAD_SIZE_BYTES", 40 * 1024 * 1024)  # 기본 40MiB
        )


# 단일 인스턴스
settings = Settings()
