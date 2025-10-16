"""API v1"""
from fastapi import APIRouter
from .endpoints import predictions, health, statistics

# v1 라우터 생성
api_router = APIRouter()

# 엔드포인트 등록
api_router.include_router(health.router)
api_router.include_router(predictions.router)
api_router.include_router(statistics.router)

__all__ = ['api_router']
