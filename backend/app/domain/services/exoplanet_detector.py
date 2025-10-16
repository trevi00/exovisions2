"""
외계행성 탐지 도메인 서비스 인터페이스
ML 모델을 사용한 예측 로직
"""

from abc import ABC, abstractmethod
from ..entities.light_curve import LightCurve
from ..value_objects.prediction_result import PredictionResult


class IExoplanetDetector(ABC):
    """외계행성 탐지 서비스 인터페이스"""

    @abstractmethod
    async def detect(self, light_curve: LightCurve) -> PredictionResult:
        """
        광도 곡선으로부터 외계행성 탐지

        Parameters:
            light_curve: 광도 곡선 데이터

        Returns:
            예측 결과
        """
        pass

    @abstractmethod
    async def detect_from_features(self, features: dict) -> PredictionResult:
        """
        특징값으로부터 외계행성 탐지

        Parameters:
            features: 추출된 특징값 딕셔너리

        Returns:
            예측 결과
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        모델 정보 반환

        Returns:
            모델 메타데이터 (정확도, 버전 등)
        """
        pass
