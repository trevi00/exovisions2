"""
예측 요청 DTO
외부에서 들어오는 데이터를 검증하고 변환
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PredictionRequest:
    """
    예측 요청 DTO

    Attributes:
        light_curve_data: 광도 곡선 데이터 (시간, 밝기)
        features: 추출된 특징값 (선택)
    """

    light_curve_data: Optional[dict] = None
    features: Optional[dict] = None

    def __post_init__(self):
        """DTO 검증"""
        if not self.light_curve_data and not self.features:
            raise ValueError("광도 곡선 데이터 또는 특징값 중 하나는 필수입니다")

    def has_light_curve(self) -> bool:
        """광도 곡선 데이터 존재 여부"""
        if self.light_curve_data is None:
            return False
        # 빈 딕셔너리 또는 time/flux 키가 없으면 False
        if not self.light_curve_data:
            return False
        return 'time' in self.light_curve_data and 'flux' in self.light_curve_data

    def has_features(self) -> bool:
        """특징값 존재 여부"""
        if self.features is None:
            return False
        # 빈 딕셔너리면 False
        return bool(self.features)
