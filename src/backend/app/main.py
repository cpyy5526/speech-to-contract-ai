from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logging
setup_logging()
import logging
logger = logging.getLogger(__name__)

# 프로젝트 공통 설정값 로드 (env -> settings)
from app.core.config import settings  # noqa: F401  # (미사용 경고 방지)

# 비동기 DB 초기화 함수
from app.db.init_db import init_db

# 각 라우터 모듈
from app.routers import auth, contracts, generations, transcriptions

# Lifespan 이벤트 핸들러 정의 ----------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI lifespan 시작 - DB 초기화 진행")
    await init_db()
    logger.info("FastAPI lifespan - DB 초기화 성공")
    yield
    logger.info("FastAPI lifespan 종료")


# FastAPI 앱 인스턴스 생성 (lifespan 포함)
app = FastAPI(
    title=getattr(settings, "PROJECT_NAME", "speech-to-contract-ai"),
    description="구두계약 음성 기반 계약서 생성 서비스 백엔드",
    version=getattr(settings, "VERSION", "0.1.0"),
    lifespan=lifespan,
)


'''
# CORS 설정 ---------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin 허용 (개발 편의)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''


# 라우터 등록 --------------------------------------------------------------------
app.include_router(auth.router)            # /auth
app.include_router(auth.user_router)       # /user
app.include_router(transcriptions.router)
app.include_router(generations.router)
app.include_router(contracts.router)


'''
# 로컬 실행 ---------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=getattr(settings, "DEBUG", False),
    )
'''