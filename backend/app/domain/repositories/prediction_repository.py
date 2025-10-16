"""
예측 리포지토리 인터페이스
도메인 계층에서 정의, 인프라 계층에서 구현
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.prediction import Prediction


class IPredictionRepository(ABC):
    """예측 리포지토리 인터페이스"""

    @abstractmethod
    async def save(self, prediction: Prediction) -> Prediction:
        """
        예측 저장

        Parameters:
            prediction: 저장할 예측 엔티티

        Returns:
            저장된 예측 엔티티
        """
        pass

    @abstractmethod
    async def find_by_id(self, prediction_id: str) -> Optional[Prediction]:
        """
        ID로 예측 조회

        Parameters:
            prediction_id: 예측 ID

        Returns:
            예측 엔티티 또는 None
        """
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """
        모든 예측 조회 (페이지네이션)

        Parameters:
            skip: 건너뛸 개수
            limit: 최대 개수

        Returns:
            예측 엔티티 리스트
        """
        pass

    @abstractmethod
    async def find_by_classification(
        self,
        is_exoplanet: bool,
        skip: int = 0,
        limit: int = 100
    ) -> List[Prediction]:
        """
        분류별 예측 조회

        Parameters:
            is_exoplanet: 외계행성 여부
            skip: 건너뛸 개수
            limit: 최대 개수

        Returns:
            예측 엔티티 리스트
        """
        pass

    @abstractmethod
    async def delete(self, prediction_id: str) -> bool:
        """
        예측 삭제

        Parameters:
            prediction_id: 삭제할 예측 ID

        Returns:
            삭제 성공 여부
        """
        pass

    @abstractmethod
    async def delete_all(self) -> int:
        """
        모든 예측 삭제

        Returns:
            삭제된 개수
        """
        pass

    @abstractmethod
    async def count(self) -> int:
        """
        전체 예측 개수

        Returns:
            예측 개수
        """
        pass

    @abstractmethod
    async def count_by_classification(self, is_exoplanet: bool) -> int:
        """
        분류별 예측 개수

        Parameters:
            is_exoplanet: 외계행성 여부

        Returns:
            예측 개수
        """
        pass
