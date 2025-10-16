"""
Pydantic 스키마
API 요청/응답 검증 및 직렬화
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class PredictionRequestSchema(BaseModel):
    """
    예측 요청 스키마

    광도 곡선 데이터 또는 특징값 중 하나는 필수
    """
    light_curve_data: Optional[Dict] = Field(
        None,
        description="광도 곡선 데이터 (time, flux, flux_err)",
        example={
            "time": [0.0, 0.1, 0.2, 0.3],
            "flux": [1.0, 0.95, 0.98, 1.0],
            "flux_err": [0.01, 0.01, 0.01, 0.01]
        }
    )
    features: Optional[Dict[str, float]] = Field(
        None,
        description="추출된 특징값",
        example={
            "mean_flux": 0.98,
            "std_flux": 0.02,
            "transit_depth": 0.05
        }
    )
    save_result: bool = Field(
        True,
        description="예측 결과를 데이터베이스에 저장할지 여부"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "light_curve_data": {
                    "time": [0.0, 0.1, 0.2, 0.3, 0.4],
                    "flux": [1.0, 0.95, 0.98, 1.0, 0.99]
                },
                "save_result": True
            }
        }


class PredictionResponseSchema(BaseModel):
    """예측 응답 스키마"""
    id: str = Field(..., description="예측 ID")
    is_exoplanet: bool = Field(..., description="외계행성 여부")
    classification: str = Field(
        ...,
        description="분류 (CONFIRMED, LIKELY_CONFIRMED, CANDIDATE, FALSE_POSITIVE)"
    )
    planet_probability: float = Field(..., description="행성 확률", ge=0.0, le=1.0)
    candidate_probability: float = Field(..., description="후보 확률", ge=0.0, le=1.0)
    confidence_score: float = Field(..., description="신뢰도 점수", ge=0.0, le=1.0)
    confidence_level: str = Field(
        ...,
        description="신뢰도 레벨 (VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW)"
    )
    created_at: datetime = Field(..., description="생성 시간")
    light_curve_data: Optional[Dict] = Field(None, description="광도 곡선 데이터")
    input_features: Optional[Dict[str, float]] = Field(None, description="입력 특징값")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "is_exoplanet": True,
                "classification": "CONFIRMED",
                "planet_probability": 0.92,
                "candidate_probability": 0.85,
                "confidence_score": 0.92,
                "confidence_level": "VERY_HIGH",
                "created_at": "2025-01-14T10:30:00",
                "light_curve_data": None
            }
        }


class PredictionsListResponseSchema(BaseModel):
    """예측 목록 응답 스키마"""
    predictions: List[PredictionResponseSchema] = Field(..., description="예측 목록")
    total: int = Field(..., description="전체 예측 개수")
    skip: int = Field(..., description="건너뛴 개수")
    limit: int = Field(..., description="조회 개수")

    class Config:
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "is_exoplanet": True,
                        "classification": "CONFIRMED",
                        "planet_probability": 0.92,
                        "candidate_probability": 0.85,
                        "confidence_score": 0.92,
                        "confidence_level": "VERY_HIGH",
                        "created_at": "2025-01-14T10:30:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100
            }
        }


class DeleteResponseSchema(BaseModel):
    """삭제 응답 스키마"""
    message: str = Field(..., description="응답 메시지")
    deleted_count: int = Field(..., description="삭제된 개수")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Successfully deleted 5 predictions",
                "deleted_count": 5
            }
        }
