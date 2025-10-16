"""
FastAPI 메인 애플리케이션
외계행성 탐지 API 서버
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from ..infrastructure.database import init_db
from .api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 라이프사이클 관리
    시작 시 데이터베이스 초기화
    """
    # 시작 시 실행
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")

    yield

    # 종료 시 실행
    print("Shutting down...")


# FastAPI 앱 생성
app = FastAPI(
    title="Exoplanet Detection API",
    description="NASA Space Apps Challenge - 외계행성 탐지 ML 모델 API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS 설정
# 환경변수에서 허용된 도메인 목록을 가져옴 (콤마로 구분)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:19006,http://localhost:8081").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # 환경변수에서 설정된 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")

# Prometheus Metrics 설정
Instrumentator().instrument(app).expose(app)


# Root 엔드포인트
@app.get("/", tags=["root"])
async def root():
    """
    루트 엔드포인트

    API 기본 정보 제공
    """
    return {
        "message": "Welcome to Exoplanet Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1",
        "metrics": "/metrics"
    }


if __name__ == "__main__":
    import uvicorn

    # 환경변수에서 호스트와 포트 가져오기
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
