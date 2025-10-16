"""
데이터 전처리기
특징값을 모델 입력에 맞게 변환
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union


class Preprocessor:
    """
    데이터 전처리기

    추출된 특징값을 ML 모델에 입력할 수 있도록
    스케일링 및 변환 수행
    """

    def __init__(self, scaler=None):
        """
        Parameters:
            scaler: sklearn 스케일러 (StandardScaler, MinMaxScaler 등)
        """
        self.scaler = scaler
        self.feature_names = None

    def set_scaler(self, scaler):
        """스케일러 설정"""
        self.scaler = scaler

    def preprocess_features(
        self,
        features: Dict[str, float]
    ) -> np.ndarray:
        """
        특징값 전처리 (Feature Engineering 포함)

        Parameters:
            features: 특징값 딕셔너리

        Returns:
            전처리된 특징값 배열
        """
        # 딕셔너리를 DataFrame으로 변환
        df = pd.DataFrame([features])

        # Feature Engineering: 5개의 추가 특징 생성
        # (train_multiclass_model.py의 engineer_features()와 동일)

        # 1. depth_per_radius_sq: 깊이 / 반지름^2
        if 'transit_depth' in df.columns and 'planet_radius' in df.columns:
            df['depth_per_radius_sq'] = df['transit_depth'] / (df['planet_radius'] ** 2 + 1e-6)

        # 2. orbit_transit_product: 궤도주기 × 통과시간
        if 'orbital_period' in df.columns and 'transit_duration' in df.columns:
            df['orbit_transit_product'] = df['orbital_period'] * df['transit_duration']

        # 3. signal_strength: 신호강도 / 깊이
        if 'signal_to_noise' in df.columns and 'transit_depth' in df.columns:
            df['signal_strength'] = df['signal_to_noise'] / (df['transit_depth'] + 1e-6)

        # 4. temp_ratio: 행성온도 / 별온도
        if 'equilibrium_temp' in df.columns and 'stellar_temp' in df.columns:
            df['temp_ratio'] = df['equilibrium_temp'] / (df['stellar_temp'] + 1e-6)

        # 5. planet_star_radius_ratio: 행성반지름 / 별반지름
        if 'planet_radius' in df.columns and 'stellar_radius' in df.columns:
            df['planet_star_radius_ratio'] = df['planet_radius'] / (df['stellar_radius'] + 1e-6)

        # 스케일러가 있으면 훈련 시 사용된 feature 순서대로 재정렬
        if self.scaler is not None and hasattr(self.scaler, 'feature_names_in_'):
            expected_features = self.scaler.feature_names_in_.tolist()

            # 누락된 특징은 0으로 채우고, 순서대로 재정렬
            for feature_name in expected_features:
                if feature_name not in df.columns:
                    df[feature_name] = 0.0

            # 훈련 시와 동일한 순서로 컬럼 재정렬
            df = df[expected_features]

        # 특징 이름 저장 (첫 번째 호출 시)
        if self.feature_names is None:
            self.feature_names = df.columns.tolist()

        # 결측치 처리
        df = df.fillna(0)

        # 무한값 처리
        df = df.replace([np.inf, -np.inf], 0)

        # 스케일링
        if self.scaler is not None:
            scaled_features = self.scaler.transform(df)
        else:
            scaled_features = df.values

        return scaled_features

    def preprocess_batch(
        self,
        features_list: List[Dict[str, float]]
    ) -> np.ndarray:
        """
        배치 전처리

        Parameters:
            features_list: 특징값 딕셔너리 리스트

        Returns:
            전처리된 특징값 배열
        """
        # DataFrame으로 변환
        df = pd.DataFrame(features_list)

        # 특징 이름 저장
        if self.feature_names is None:
            self.feature_names = df.columns.tolist()

        # 결측치 처리
        df = df.fillna(0)

        # 무한값 처리
        df = df.replace([np.inf, -np.inf], 0)

        # 스케일링
        if self.scaler is not None:
            scaled_features = self.scaler.transform(df)
        else:
            scaled_features = df.values

        return scaled_features

    def validate_features(self, features: Dict[str, float]) -> bool:
        """
        특징값 검증

        Parameters:
            features: 특징값 딕셔너리

        Returns:
            유효성 여부
        """
        # 빈 딕셔너리 체크
        if not features:
            return False

        # 모든 값이 숫자인지 확인
        for key, value in features.items():
            if not isinstance(value, (int, float)):
                return False

            # NaN, Inf 체크
            if np.isnan(value) or np.isinf(value):
                return False

        return True

    def get_feature_names(self) -> List[str]:
        """특징 이름 목록 반환"""
        return self.feature_names if self.feature_names else []

    def align_features(
        self,
        features: Dict[str, float],
        expected_features: List[str]
    ) -> Dict[str, float]:
        """
        특징값을 예상 특징 목록에 맞게 정렬

        Parameters:
            features: 특징값 딕셔너리
            expected_features: 예상 특징 이름 리스트

        Returns:
            정렬된 특징값 딕셔너리
        """
        aligned = {}

        for feature_name in expected_features:
            if feature_name in features:
                aligned[feature_name] = features[feature_name]
            else:
                # 없는 특징은 0으로 채움
                aligned[feature_name] = 0.0

        return aligned
