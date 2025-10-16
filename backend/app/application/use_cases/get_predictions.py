"""
예측 결과 조회 Use Cases
"""

from typing import List, Optional
from ...domain.repositories.prediction_repository import IPredictionRepository
from ...domain.value_objects.confidence_score import ConfidenceScore
from ...domain.value_objects.prediction_result import PredictionResult, PredictionClass
from ..dto.prediction_response import PredictionResponse


class GetPredictionsUseCase:
    """모든 예측 결과 조회 Use Case"""

    def __init__(self, repository: IPredictionRepository):
        self.repository = repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        is_exoplanet: Optional[bool] = None
    ) -> List[PredictionResponse]:
        """
        예측 결과 목록 조회

        Parameters:
            skip: 건너뛸 개수 (페이지네이션)
            limit: 최대 조회 개수
            is_exoplanet: 외계행성 여부 필터 (None이면 전체 조회)

        Returns:
            예측 응답 DTO 리스트
        """
        # 리포지토리에서 데이터 조회
        predictions = await self.repository.find_all(
            skip=skip,
            limit=limit
        )

        # 필터 적용
        if is_exoplanet is not None:
            predictions = [
                p for p in predictions
                if p.is_exoplanet == is_exoplanet
            ]

        # DTO로 변환
        return [
            self._to_response_dto(prediction)
            for prediction in predictions
        ]

    def _to_response_dto(self, prediction) -> PredictionResponse:
        """도메인 엔티티를 응답 DTO로 변환"""
        # 신뢰도 레벨 계산
        confidence = ConfidenceScore(score=prediction.confidence_score)
        confidence_level = confidence.get_level()

        # 분류 결정
        classification = self._determine_classification(
            prediction.is_exoplanet,
            prediction.planet_probability,
            prediction.candidate_probability
        )

        return PredictionResponse.from_domain(
            prediction=prediction,
            classification=classification,
            confidence_level=confidence_level
        )

    def _determine_classification(
        self,
        is_exoplanet: bool,
        planet_prob: float,
        candidate_prob: float
    ) -> str:
        """분류 결정 로직"""
        if not is_exoplanet:
            return PredictionClass.FALSE_POSITIVE

        if planet_prob >= 0.8:
            return PredictionClass.CONFIRMED
        elif planet_prob >= 0.6:
            return PredictionClass.LIKELY_CONFIRMED
        else:
            return PredictionClass.CANDIDATE


class GetPredictionByIdUseCase:
    """단일 예측 결과 조회 Use Case"""

    def __init__(self, repository: IPredictionRepository):
        self.repository = repository

    async def execute(self, prediction_id: str) -> Optional[PredictionResponse]:
        """
        ID로 예측 결과 조회

        Parameters:
            prediction_id: 예측 ID

        Returns:
            예측 응답 DTO 또는 None
        """
        # 리포지토리에서 데이터 조회
        prediction = await self.repository.find_by_id(prediction_id)

        if not prediction:
            return None

        # 신뢰도 레벨 계산
        confidence = ConfidenceScore(score=prediction.confidence_score)
        confidence_level = confidence.get_level()

        # 분류 결정
        classification = self._determine_classification(
            prediction.is_exoplanet,
            prediction.planet_probability,
            prediction.candidate_probability
        )

        # DTO로 변환
        return PredictionResponse.from_domain(
            prediction=prediction,
            classification=classification,
            confidence_level=confidence_level
        )

    def _determine_classification(
        self,
        is_exoplanet: bool,
        planet_prob: float,
        candidate_prob: float
    ) -> str:
        """분류 결정 로직"""
        if not is_exoplanet:
            return PredictionClass.FALSE_POSITIVE

        if planet_prob >= 0.8:
            return PredictionClass.CONFIRMED
        elif planet_prob >= 0.6:
            return PredictionClass.LIKELY_CONFIRMED
        else:
            return PredictionClass.CANDIDATE
