"""
헬스 체크 및 모델 정보 API
"""

from fastapi import APIRouter, Depends
from ...dependencies import get_exoplanet_detector
from .....infrastructure.ml import ExoplanetDetectorImpl


router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="헬스 체크",
    description="서버 상태를 확인합니다."
)
async def health_check():
    """
    헬스 체크 API

    **Returns:**
    - 서버 상태 정보
    """
    return {
        "status": "healthy",
        "service": "Exoplanet Detection API",
        "version": "1.0.0"
    }


@router.get(
    "/model/info",
    summary="모델 정보 조회",
    description="현재 로드된 ML 모델의 정보를 조회합니다."
)
async def get_model_info(
    detector: ExoplanetDetectorImpl = Depends(get_exoplanet_detector)
):
    """
    모델 정보 조회 API

    **Returns:**
    - 모델 메타데이터 (이름, 타입, 특징 개수 등)
    """
    try:
        model_info = detector.get_model_info()
        return {
            "status": "success",
            "model_info": model_info
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
