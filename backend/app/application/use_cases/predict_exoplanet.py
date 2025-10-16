"""
외계행성 예측 Use Case
"""

from typing import Optional
from ...domain.entities.light_curve import LightCurve
from ...domain.entities.prediction import Prediction
from ...domain.repositories.prediction_repository import IPredictionRepository
from ...domain.services.exoplanet_detector import IExoplanetDetector
from ...domain.value_objects.confidence_score import ConfidenceScore
from ..dto.prediction_request import PredictionRequest
from ..dto.prediction_response import PredictionResponse


class PredictExoplanetUseCase:
    """외계행성 예측 Use Case"""

    def __init__(
        self,
        detector: IExoplanetDetector,
        repository: IPredictionRepository
    ):
        self.detector = detector
        self.repository = repository

    async def execute(
        self,
        request: PredictionRequest,
        save_result: bool = True
    ) -> PredictionResponse:
        """
        외계행성 예측 실행

        Parameters:
            request: 예측 요청 DTO
            save_result: 결과 저장 여부 (기본값: True)

        Returns:
            예측 응답 DTO

        Raises:
            ValueError: 유효하지 않은 요청 데이터
        """
        # 특징값으로부터 예측 (우선순위 높음)
        if request.has_features():
            prediction_result = await self.detector.detect_from_features(
                request.features
            )
            light_curve_data = None
        # 광도 곡선 데이터로부터 예측
        elif request.has_light_curve():
            prediction_result = await self._predict_from_light_curve(
                request.light_curve_data
            )
            light_curve_data = request.light_curve_data
        else:
            raise ValueError("광도 곡선 데이터 또는 특징값이 필요합니다")

        # 신뢰도 점수 계산
        confidence = ConfidenceScore(
            score=max(
                prediction_result.planet_probability,
                prediction_result.candidate_probability
            )
        )

        # 도메인 엔티티 생성
        prediction = Prediction(
            light_curve_data=light_curve_data,
            input_features=request.features if request.has_features() else None,
            is_exoplanet=prediction_result.is_exoplanet,
            confidence_score=confidence.score,
            planet_probability=prediction_result.planet_probability,
            candidate_probability=prediction_result.candidate_probability
        )

        # 결과 저장 (옵션)
        if save_result:
            prediction = await self.repository.save(prediction)

        # 응답 DTO 생성
        return PredictionResponse.from_domain(
            prediction=prediction,
            classification=prediction_result.classification,
            confidence_level=confidence.get_level()
        )

    async def _predict_from_light_curve(self, light_curve_data: dict):
        """광도 곡선 데이터로부터 예측"""
        # 광도 곡선 엔티티 생성
        light_curve = LightCurve(
            time=light_curve_data.get('time', []),
            flux=light_curve_data.get('flux', []),
            flux_err=light_curve_data.get('flux_err')
        )

        # 데이터 검증
        light_curve.validate()

        # 예측 수행
        return await self.detector.detect(light_curve)
