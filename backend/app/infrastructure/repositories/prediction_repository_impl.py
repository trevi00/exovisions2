"""
예측 리포지토리 구현
도메인 리포지토리 인터페이스의 SQLAlchemy 구현
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ...domain.entities.prediction import Prediction
from ...domain.repositories.prediction_repository import IPredictionRepository
from ..database.models import PredictionModel


class PredictionRepositoryImpl(IPredictionRepository):
    """
    예측 리포지토리 SQLAlchemy 구현

    도메인 엔티티와 데이터베이스 모델 간 변환 및
    CRUD 작업 수행
    """

    def __init__(self, db: Session):
        """
        Parameters:
            db: SQLAlchemy 세션
        """
        self.db = db

    async def save(self, prediction: Prediction) -> Prediction:
        """
        예측 결과 저장

        Parameters:
            prediction: 예측 도메인 엔티티

        Returns:
            저장된 예측 엔티티
        """
        # 도메인 엔티티를 DB 모델로 변환
        db_prediction = PredictionModel(
            id=prediction.id,
            light_curve_data=prediction.light_curve_data,
            input_features=prediction.input_features,  # 입력 특징값 저장
            is_exoplanet=prediction.is_exoplanet,
            classification=prediction.get_classification(),  # 분류 저장
            confidence_score=prediction.confidence_score,
            planet_probability=prediction.planet_probability,
            candidate_probability=prediction.candidate_probability,
            created_at=prediction.created_at
        )

        # 저장
        self.db.add(db_prediction)
        self.db.commit()
        self.db.refresh(db_prediction)

        # DB 모델을 도메인 엔티티로 변환하여 반환
        return self._to_domain(db_prediction)

    async def find_by_id(self, prediction_id: str) -> Optional[Prediction]:
        """
        ID로 예측 결과 조회

        Parameters:
            prediction_id: 예측 ID

        Returns:
            예측 엔티티 또는 None
        """
        db_prediction = self.db.query(PredictionModel).filter(
            PredictionModel.id == prediction_id
        ).first()

        if db_prediction is None:
            return None

        return self._to_domain(db_prediction)

    async def find_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Prediction]:
        """
        모든 예측 결과 조회

        Parameters:
            skip: 건너뛸 개수
            limit: 최대 조회 개수

        Returns:
            예측 엔티티 리스트
        """
        db_predictions = self.db.query(PredictionModel)\
            .order_by(desc(PredictionModel.created_at))\
            .offset(skip)\
            .limit(limit)\
            .all()

        return [self._to_domain(db_pred) for db_pred in db_predictions]

    async def delete(self, prediction_id: str) -> bool:
        """
        예측 결과 삭제

        Parameters:
            prediction_id: 삭제할 예측 ID

        Returns:
            삭제 성공 여부
        """
        db_prediction = self.db.query(PredictionModel).filter(
            PredictionModel.id == prediction_id
        ).first()

        if db_prediction is None:
            return False

        self.db.delete(db_prediction)
        self.db.commit()

        return True

    async def delete_all(self) -> int:
        """
        모든 예측 결과 삭제

        Returns:
            삭제된 예측 개수
        """
        count = self.db.query(PredictionModel).count()
        self.db.query(PredictionModel).delete()
        self.db.commit()

        return count

    async def count(self) -> int:
        """
        전체 예측 개수 조회

        Returns:
            예측 개수
        """
        return self.db.query(PredictionModel).count()

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
        db_predictions = self.db.query(PredictionModel)\
            .filter(PredictionModel.is_exoplanet == is_exoplanet)\
            .order_by(desc(PredictionModel.created_at))\
            .offset(skip)\
            .limit(limit)\
            .all()

        return [self._to_domain(db_pred) for db_pred in db_predictions]

    async def count_by_classification(self, is_exoplanet: bool) -> int:
        """
        분류별 예측 개수

        Parameters:
            is_exoplanet: 외계행성 여부

        Returns:
            예측 개수
        """
        return self.db.query(PredictionModel)\
            .filter(PredictionModel.is_exoplanet == is_exoplanet)\
            .count()

    def _to_domain(self, db_prediction: PredictionModel) -> Prediction:
        """
        DB 모델을 도메인 엔티티로 변환

        Parameters:
            db_prediction: 데이터베이스 모델

        Returns:
            도메인 엔티티
        """
        return Prediction(
            id=db_prediction.id,
            light_curve_data=db_prediction.light_curve_data,
            input_features=db_prediction.input_features,  # 입력 특징값 로드
            is_exoplanet=db_prediction.is_exoplanet,
            confidence_score=db_prediction.confidence_score,
            planet_probability=db_prediction.planet_probability,
            candidate_probability=db_prediction.candidate_probability,
            created_at=db_prediction.created_at
        )
