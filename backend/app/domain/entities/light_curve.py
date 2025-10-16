"""
광도 곡선 엔티티 (Light Curve Entity)
별의 밝기 변화 데이터를 나타내는 도메인 엔티티
"""

from dataclasses import dataclass
from typing import List, Optional
import numpy as np


@dataclass
class LightCurve:
    """
    광도 곡선 엔티티

    Attributes:
        time: 시간 배열
        flux: 밝기(flux) 배열
        flux_err: 밝기 오차 배열 (선택)
        metadata: 추가 메타데이터
    """

    time: List[float]
    flux: List[float]
    flux_err: Optional[List[float]] = None
    metadata: Optional[dict] = None

    def __post_init__(self):
        """엔티티 검증"""
        self._validate()

    def _validate(self):
        """도메인 규칙 검증"""
        if len(self.time) != len(self.flux):
            raise ValueError("시간과 밝기 배열의 길이가 같아야 합니다")

        if len(self.time) == 0:
            raise ValueError("광도 곡선 데이터가 비어있을 수 없습니다")

        if self.flux_err and len(self.flux_err) != len(self.flux):
            raise ValueError("밝기 오차 배열의 길이가 밝기 배열과 같아야 합니다")

    def get_length(self) -> int:
        """데이터 포인트 개수"""
        return len(self.time)

    def get_time_span(self) -> float:
        """관측 기간 (일)"""
        if len(self.time) < 2:
            return 0.0
        return max(self.time) - min(self.time)

    def get_flux_range(self) -> tuple[float, float]:
        """밝기 범위 (최소, 최대)"""
        return (min(self.flux), max(self.flux))

    def has_transit_signal(self, threshold: float = 0.01) -> bool:
        """
        트랜짓 신호 존재 여부 (간단한 휴리스틱)

        Parameters:
            threshold: 밝기 감소 임계값 (기본 1%)
        """
        flux_array = np.array(self.flux)
        median_flux = np.median(flux_array)
        min_flux = np.min(flux_array)

        # 중간값 대비 최소값의 감소량
        drop = (median_flux - min_flux) / median_flux

        return drop > threshold

    def normalize(self) -> 'LightCurve':
        """정규화된 광도 곡선 반환"""
        flux_array = np.array(self.flux)
        median_flux = np.median(flux_array)

        normalized_flux = (flux_array / median_flux).tolist()

        return LightCurve(
            time=self.time.copy(),
            flux=normalized_flux,
            flux_err=self.flux_err.copy() if self.flux_err else None,
            metadata=self.metadata
        )

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            'time': self.time,
            'flux': self.flux,
            'flux_err': self.flux_err,
            'metadata': self.metadata,
            'length': self.get_length(),
            'time_span': self.get_time_span(),
            'flux_range': self.get_flux_range()
        }
