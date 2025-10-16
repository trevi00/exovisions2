"""
특징 추출기
광도 곡선 데이터로부터 머신러닝에 사용할 특징 추출
"""

import numpy as np
from typing import Dict, List
from scipy.stats import skew, kurtosis
from ...domain.entities.light_curve import LightCurve


class FeatureExtractor:
    """
    광도 곡선 특징 추출기

    시계열 데이터로부터 통계적 특징을 추출하여
    머신러닝 모델의 입력으로 사용
    """

    def extract_features(self, light_curve: LightCurve) -> Dict[str, float]:
        """
        광도 곡선으로부터 특징 추출

        Parameters:
            light_curve: 광도 곡선 엔티티

        Returns:
            추출된 특징값 딕셔너리
        """
        flux = np.array(light_curve.flux)
        time = np.array(light_curve.time)

        features = {}

        # 기본 통계량
        features['mean_flux'] = np.mean(flux)
        features['median_flux'] = np.median(flux)
        features['std_flux'] = np.std(flux)
        features['var_flux'] = np.var(flux)
        features['min_flux'] = np.min(flux)
        features['max_flux'] = np.max(flux)

        # 범위 및 변동성
        features['flux_range'] = features['max_flux'] - features['min_flux']
        features['flux_ratio'] = features['max_flux'] / features['min_flux'] if features['min_flux'] != 0 else 0

        # 고차 모멘트
        features['skewness'] = skew(flux)
        features['kurtosis'] = kurtosis(flux)

        # 백분위수
        features['flux_25percentile'] = np.percentile(flux, 25)
        features['flux_75percentile'] = np.percentile(flux, 75)
        features['flux_90percentile'] = np.percentile(flux, 90)

        # 변동 계수
        features['coefficient_of_variation'] = (
            features['std_flux'] / features['mean_flux']
            if features['mean_flux'] != 0 else 0
        )

        # Transit 특징
        features['transit_depth'] = self._calculate_transit_depth(flux)
        features['transit_duration'] = self._estimate_transit_duration(flux, time)

        # 에러 관련 (있는 경우)
        if light_curve.flux_err is not None:
            flux_err = np.array(light_curve.flux_err)
            features['mean_flux_err'] = np.mean(flux_err)
            features['max_flux_err'] = np.max(flux_err)

        return features

    def _calculate_transit_depth(self, flux: np.ndarray) -> float:
        """
        Transit depth 계산

        Parameters:
            flux: 플럭스 배열

        Returns:
            Transit depth (정규화된 밝기 감소)
        """
        median_flux = np.median(flux)
        min_flux = np.min(flux)

        if median_flux == 0:
            return 0.0

        depth = (median_flux - min_flux) / median_flux
        return depth

    def _estimate_transit_duration(
        self,
        flux: np.ndarray,
        time: np.ndarray
    ) -> float:
        """
        Transit duration 추정

        Parameters:
            flux: 플럭스 배열
            time: 시간 배열

        Returns:
            Transit 지속 시간
        """
        # Transit threshold (median보다 1% 이상 어두운 지점)
        median_flux = np.median(flux)
        threshold = median_flux * 0.99

        # Threshold 이하인 지점 찾기
        in_transit = flux < threshold

        if not np.any(in_transit):
            return 0.0

        # Transit 구간의 시간 범위
        transit_times = time[in_transit]

        if len(transit_times) == 0:
            return 0.0

        duration = np.max(transit_times) - np.min(transit_times)
        return duration

    def extract_from_dict(self, light_curve_data: dict) -> Dict[str, float]:
        """
        딕셔너리 데이터로부터 특징 추출

        Parameters:
            light_curve_data: 광도 곡선 데이터 딕셔너리

        Returns:
            추출된 특징값 딕셔너리
        """
        light_curve = LightCurve(
            time=light_curve_data.get('time', []),
            flux=light_curve_data.get('flux', []),
            flux_err=light_curve_data.get('flux_err')
        )

        return self.extract_features(light_curve)
