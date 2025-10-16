"""
외계행성 탐지 서비스 구현
도메인 서비스 인터페이스의 실제 구현
"""

import numpy as np
from typing import Dict
from ...domain.entities.light_curve import LightCurve
from ...domain.services.exoplanet_detector import IExoplanetDetector
from ...domain.value_objects.prediction_result import PredictionResult, PredictionClass
from .model_loader import ModelLoader
from .feature_extractor import FeatureExtractor
from .preprocessor import Preprocessor


class ExoplanetDetectorImpl(IExoplanetDetector):
    """
    외계행성 탐지 서비스 구현

    ML 모델을 사용하여 광도 곡선 또는 특징값으로부터
    외계행성을 탐지
    """

    def __init__(
        self,
        model_loader: ModelLoader,
        feature_extractor: FeatureExtractor,
        preprocessor: Preprocessor
    ):
        """
        Parameters:
            model_loader: 모델 로더
            feature_extractor: 특징 추출기
            preprocessor: 전처리기
        """
        self.model_loader = model_loader
        self.feature_extractor = feature_extractor
        self.preprocessor = preprocessor

        # 모델과 스케일러가 로드되지 않았다면 로드
        if not self.model_loader.is_loaded():
            try:
                self.model_loader.load_all()
                self.preprocessor.set_scaler(self.model_loader.get_scaler())
            except Exception as e:
                raise RuntimeError(f"모델 로드 실패: {str(e)}")

    async def detect(self, light_curve: LightCurve) -> PredictionResult:
        """
        광도 곡선으로부터 외계행성 탐지

        Parameters:
            light_curve: 광도 곡선 데이터

        Returns:
            예측 결과
        """
        # 1. 특징 추출
        features = self.feature_extractor.extract_features(light_curve)

        # 2. 특징값으로 예측
        return await self.detect_from_features(features)

    async def detect_from_features(self, features: Dict[str, float]) -> PredictionResult:
        """
        특징값으로부터 외계행성 탐지

        Parameters:
            features: 추출된 특징값 딕셔너리

        Returns:
            예측 결과
        """
        # 1. 특징값 검증
        if not self.preprocessor.validate_features(features):
            raise ValueError("유효하지 않은 특징값입니다")

        # 2. 전처리
        processed_features = self.preprocessor.preprocess_features(features)

        # 3. 모델 예측
        model = self.model_loader.get_model()
        probabilities = model.predict_proba(processed_features)[0]

        # 4. 결과 해석
        # 모델 출력: [false_positive_prob, candidate_prob, confirmed_prob]
        # 또는 [not_exoplanet_prob, exoplanet_prob] (이진 분류인 경우)

        if len(probabilities) == 2:
            # 이진 분류
            not_exoplanet_prob = probabilities[0]
            exoplanet_prob = probabilities[1]
            planet_probability = exoplanet_prob
            candidate_probability = exoplanet_prob
            is_exoplanet = exoplanet_prob > 0.5
        else:
            # 다중 클래스 분류
            false_positive_prob = probabilities[0]
            candidate_prob = probabilities[1] if len(probabilities) > 1 else 0.0
            confirmed_prob = probabilities[2] if len(probabilities) > 2 else 0.0

            planet_probability = confirmed_prob
            candidate_probability = candidate_prob
            is_exoplanet = (confirmed_prob + candidate_prob) > false_positive_prob

        # 5. 분류 결정
        classification = self._determine_classification(
            is_exoplanet,
            planet_probability,
            candidate_probability
        )

        # 6. PredictionResult 생성
        return PredictionResult(
            is_exoplanet=is_exoplanet,
            classification=classification,
            planet_probability=float(planet_probability),
            candidate_probability=float(candidate_probability)
        )

    def _determine_classification(
        self,
        is_exoplanet: bool,
        planet_prob: float,
        candidate_prob: float
    ) -> str:
        """
        분류 결정

        Parameters:
            is_exoplanet: 외계행성 여부
            planet_prob: 행성 확률
            candidate_prob: 후보 확률

        Returns:
            분류 결과 문자열
        """
        if not is_exoplanet:
            return PredictionClass.FALSE_POSITIVE

        # 높은 확률 -> 확인됨
        if planet_prob >= 0.8:
            return PredictionClass.CONFIRMED

        # 중간 확률 -> 확인 가능성 높음
        if planet_prob >= 0.6 or candidate_prob >= 0.7:
            return PredictionClass.LIKELY_CONFIRMED

        # 낮은 확률 -> 후보
        return PredictionClass.CANDIDATE

    def get_model_info(self) -> dict:
        """
        모델 정보 반환

        Returns:
            모델 메타데이터
        """
        model_info = self.model_loader.get_model_info()

        # 추가 정보
        model_info['feature_count'] = len(self.preprocessor.get_feature_names())
        model_info['features'] = self.preprocessor.get_feature_names()

        return model_info
