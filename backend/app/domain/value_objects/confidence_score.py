"""
신뢰도 점수 Value Object
불변 객체로서 예측의 신뢰도를 나타냄
"""

from dataclasses import dataclass
from typing import Literal


ConfidenceLevel = Literal["VERY_HIGH", "HIGH", "MEDIUM", "LOW", "VERY_LOW"]


@dataclass(frozen=True)
class ConfidenceScore:
    """
    신뢰도 점수 Value Object

    Attributes:
        score: 0.0 ~ 1.0 사이의 신뢰도 점수
    """

    score: float

    def __post_init__(self):
        """Value Object 검증"""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"신뢰도 점수는 0.0과 1.0 사이여야 합니다: {self.score}")

    def get_level(self) -> ConfidenceLevel:
        """신뢰도 레벨 반환"""
        if self.score >= 0.9:
            return "VERY_HIGH"
        elif self.score >= 0.8:
            return "HIGH"
        elif self.score >= 0.6:
            return "MEDIUM"
        elif self.score >= 0.4:
            return "LOW"
        else:
            return "VERY_LOW"

    def is_reliable(self, threshold: float = 0.7) -> bool:
        """신뢰할 수 있는 수준인지 판단"""
        return self.score >= threshold

    def __str__(self) -> str:
        return f"{self.score:.2%} ({self.get_level()})"
