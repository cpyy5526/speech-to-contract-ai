from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 프로젝트 공통 설정값 로드 (env -> settings)
from app.core.config import settings  # noqa: F401  # (미사용 경고 방지)

# 비동기 DB 초기화 함수
from app.db.init_db import init_db

# 각 라우터 모듈
from app.routers import transcriptions, generations, contracts
from app.routers.auth import router as auth_router, user_router


# FastAPI 애플리케이션 인스턴스 -------------------------------------------------
app = FastAPI(
    title=getattr(settings, "PROJECT_NAME", "AI Contract Generation API"),
    description="음성 기반 계약서 자동 생성 웹서비스 백엔드",
    version=getattr(settings, "VERSION", "0.1.0"),
)


# CORS 설정 ---------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 Origin 허용 (개발 편의)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록 --------------------------------------------------------------------
app.include_router(auth_router)          # /auth
app.include_router(user_router)          # /auth/user (prefix="/user")
app.include_router(transcriptions.router)
app.include_router(generations.router)
app.include_router(contracts.router)


# 애플리케이션 라이프사이클 -------------------------------------------------------
@app.on_event("startup")
async def _startup() -> None:
    """애플리케이션 기동 시 1회 실행: 데이터베이스 초기화"""
    await init_db()


# 로컬 실행 ---------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=getattr(settings, "DEBUG", False),
    )
