"""
예측 결과 Value Object
불변 객체로서 예측 결과를 나타냄
"""

from dataclasses import dataclass
from typing import Literal


class PredictionClass:
    """예측 분류 상수"""
    CONFIRMED = "CONFIRMED"
    LIKELY_CONFIRMED = "LIKELY_CONFIRMED"
    CANDIDATE = "CANDIDATE"
    FALSE_POSITIVE = "FALSE_POSITIVE"


# 타입 힌트용
PredictionClassType = Literal["CONFIRMED", "LIKELY_CONFIRMED", "CANDIDATE", "FALSE_POSITIVE"]


@dataclass(frozen=True)
class PredictionResult:
    """
    예측 결과 Value Object

    Attributes:
        is_exoplanet: 외계행성 여부
        classification: 분류 결과
        planet_probability: 행성 확률
        candidate_probability: 후보 확률
    """

    is_exoplanet: bool
    classification: PredictionClassType
    planet_probability: float
    candidate_probability: float

    def __post_init__(self):
        """Value Object 검증"""
        if not 0.0 <= self.planet_probability <= 1.0:
            raise ValueError("행성 확률은 0.0과 1.0 사이여야 합니다")

        if not 0.0 <= self.candidate_probability <= 1.0:
            raise ValueError("후보 확률은 0.0과 1.0 사이여야 합니다")

    def is_confirmed(self) -> bool:
        """확인된 외계행성 여부"""
        return self.classification in ["CONFIRMED", "LIKELY_CONFIRMED"]

    def is_high_confidence(self) -> bool:
        """높은 신뢰도 여부"""
        return self.classification == "CONFIRMED"

    def get_dominant_probability(self) -> float:
        """우세한 확률 반환"""
        return max(self.planet_probability, self.candidate_probability)
