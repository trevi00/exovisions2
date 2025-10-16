"""
예측 결과 삭제 Use Cases
"""

from ...domain.repositories.prediction_repository import IPredictionRepository


class DeletePredictionUseCase:
    """단일 예측 결과 삭제 Use Case"""

    def __init__(self, repository: IPredictionRepository):
        self.repository = repository

    async def execute(self, prediction_id: str) -> bool:
        """
        예측 결과 삭제

        Parameters:
            prediction_id: 삭제할 예측 ID

        Returns:
            삭제 성공 여부

        Raises:
            ValueError: 존재하지 않는 예측 ID
        """
        # 예측 존재 여부 확인
        prediction = await self.repository.find_by_id(prediction_id)
        if not prediction:
            raise ValueError(f"예측 ID {prediction_id}를 찾을 수 없습니다")

        # 삭제 수행
        return await self.repository.delete(prediction_id)


class DeleteAllPredictionsUseCase:
    """모든 예측 결과 삭제 Use Case"""

    def __init__(self, repository: IPredictionRepository):
        self.repository = repository

    async def execute(self, is_exoplanet: bool = None) -> int:
        """
        모든 예측 결과 삭제

        Parameters:
            is_exoplanet: 특정 분류만 삭제 (None이면 전체 삭제)
                - True: 외계행성으로 예측된 결과만 삭제
                - False: 외계행성이 아닌 결과만 삭제
                - None: 모든 결과 삭제

        Returns:
            삭제된 예측 개수
        """
        if is_exoplanet is None:
            # 모든 예측 삭제
            return await self.repository.delete_all()
        else:
            # 특정 분류만 삭제
            predictions = await self.repository.find_all(limit=10000)
            filtered_predictions = [
                p for p in predictions
                if p.is_exoplanet == is_exoplanet
            ]

            deleted_count = 0
            for prediction in filtered_predictions:
                success = await self.repository.delete(prediction.id)
                if success:
                    deleted_count += 1

            return deleted_count
