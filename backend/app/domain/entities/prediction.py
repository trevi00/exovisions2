"""
예측 엔티티 (Prediction Entity)
외계행성 탐지 예측 결과를 나타내는 도메인 엔티티
"""

from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Prediction:
    """
    외계행성 예측 엔티티

    Attributes:
        id: 고유 식별자
        light_curve_data: 광도 곡선 데이터 (JSON)
        is_exoplanet: 외계행성 여부
        confidence_score: 신뢰도 점수 (0.0 ~ 1.0)
        planet_probability: 행성 확률
        candidate_probability: 후보 확률
        created_at: 생성 시간
        input_features: 입력된 특징값들
    """

    # 필수 속성
    is_exoplanet: bool
    confidence_score: float
    planet_probability: float
    candidate_probability: float

    # 선택 속성 (광도 곡선 또는 특징값 중 하나만 사용 가능)
    light_curve_data: Optional[dict] = None

    # 선택 속성
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    input_features: Optional[dict] = None

    def __post_init__(self):
        """엔티티 검증"""
        self._validate()

    def _validate(self):
        """도메인 규칙 검증"""
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("신뢰도 점수는 0.0과 1.0 사이여야 합니다")

        if not 0.0 <= self.planet_probability <= 1.0:
            raise ValueError("행성 확률은 0.0과 1.0 사이여야 합니다")

        if not 0.0 <= self.candidate_probability <= 1.0:
            raise ValueError("후보 확률은 0.0과 1.0 사이여야 합니다")

        # light_curve_data는 선택 사항 (특징값만 사용할 수도 있음)

    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """높은 신뢰도 여부"""
        return self.confidence_score >= threshold

    def get_classification(self) -> str:
        """분류 결과 반환"""
        if self.is_exoplanet:
            return "CONFIRMED" if self.is_high_confidence() else "LIKELY_CONFIRMED"
        else:
            return "CANDIDATE" if self.is_high_confidence(0.5) else "FALSE_POSITIVE"

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            'id': self.id,
            'light_curve_data': self.light_curve_data,
            'is_exoplanet': self.is_exoplanet,
            'confidence_score': self.confidence_score,
            'planet_probability': self.planet_probability,
            'candidate_probability': self.candidate_probability,
            'classification': self.get_classification(),
            'created_at': self.created_at.isoformat(),
            'input_features': self.input_features
        }
