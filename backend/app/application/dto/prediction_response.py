"""
예측 응답 DTO
API 응답으로 반환되는 데이터 구조
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class PredictionResponse:
    """
    예측 응답 DTO

    Attributes:
        id: 예측 ID
        is_exoplanet: 외계행성 여부
        classification: 분류 결과 (CONFIRMED, LIKELY_CONFIRMED, CANDIDATE, FALSE_POSITIVE)
        planet_probability: 행성 확률
        candidate_probability: 후보 확률
        confidence_score: 신뢰도 점수
        confidence_level: 신뢰도 레벨 (VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW)
        created_at: 생성 시간
        light_curve_data: 광도 곡선 데이터 (선택)
        input_features: 입력 특징값 (선택)
    """

    id: str
    is_exoplanet: bool
    classification: str
    planet_probability: float
    candidate_probability: float
    confidence_score: float
    confidence_level: str
    created_at: datetime
    light_curve_data: Optional[dict] = None
    input_features: Optional[Dict[str, float]] = None

    @classmethod
    def from_domain(cls, prediction, classification: str, confidence_level: str):
        """도메인 엔티티로부터 DTO 생성"""
        return cls(
            id=prediction.id,
            is_exoplanet=prediction.is_exoplanet,
            classification=classification,
            planet_probability=prediction.planet_probability,
            candidate_probability=prediction.candidate_probability,
            confidence_score=prediction.confidence_score,
            confidence_level=confidence_level,
            created_at=prediction.created_at,
            light_curve_data=prediction.light_curve_data,
            input_features=prediction.input_features
        )
