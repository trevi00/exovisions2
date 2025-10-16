"""
의존성 주입
FastAPI 엔드포인트에서 사용할 의존성
"""

from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session
from ...infrastructure.database import get_db
from ...infrastructure.ml import (
    ModelLoader,
    FeatureExtractor,
    Preprocessor,
    ExoplanetDetectorImpl
)
from ...infrastructure.repositories import PredictionRepositoryImpl
from ...application.use_cases import (
    PredictExoplanetUseCase,
    GetPredictionsUseCase,
    GetPredictionByIdUseCase,
    DeletePredictionUseCase,
    DeleteAllPredictionsUseCase
)


# 싱글톤 인스턴스를 위한 캐시
@lru_cache()
def get_model_loader() -> ModelLoader:
    """모델 로더 싱글톤"""
    return ModelLoader(model_dir="models")


@lru_cache()
def get_feature_extractor() -> FeatureExtractor:
    """특징 추출기 싱글톤"""
    return FeatureExtractor()


@lru_cache()
def get_preprocessor() -> Preprocessor:
    """전처리기 싱글톤"""
    return Preprocessor()


@lru_cache()
def get_exoplanet_detector() -> ExoplanetDetectorImpl:
    """외계행성 탐지기 싱글톤"""
    model_loader = get_model_loader()
    feature_extractor = get_feature_extractor()
    preprocessor = get_preprocessor()

    return ExoplanetDetectorImpl(
        model_loader=model_loader,
        feature_extractor=feature_extractor,
        preprocessor=preprocessor
    )


# Use Case 의존성
def get_prediction_repository(db: Session = Depends(get_db)) -> PredictionRepositoryImpl:
    """예측 리포지토리"""
    return PredictionRepositoryImpl(db=db)


def get_predict_exoplanet_use_case(
    db: Session = Depends(get_db)
) -> PredictExoplanetUseCase:
    """예측 Use Case"""
    detector = get_exoplanet_detector()
    repository = PredictionRepositoryImpl(db=db)
    return PredictExoplanetUseCase(detector=detector, repository=repository)


def get_get_predictions_use_case(
    db: Session = Depends(get_db)
) -> GetPredictionsUseCase:
    """예측 목록 조회 Use Case"""
    repository = PredictionRepositoryImpl(db=db)
    return GetPredictionsUseCase(repository=repository)


def get_get_prediction_by_id_use_case(
    db: Session = Depends(get_db)
) -> GetPredictionByIdUseCase:
    """예측 단건 조회 Use Case"""
    repository = PredictionRepositoryImpl(db=db)
    return GetPredictionByIdUseCase(repository=repository)


def get_delete_prediction_use_case(
    db: Session = Depends(get_db)
) -> DeletePredictionUseCase:
    """예측 삭제 Use Case"""
    repository = PredictionRepositoryImpl(db=db)
    return DeletePredictionUseCase(repository=repository)


def get_delete_all_predictions_use_case(
    db: Session = Depends(get_db)
) -> DeleteAllPredictionsUseCase:
    """전체 예측 삭제 Use Case"""
    repository = PredictionRepositoryImpl(db=db)
    return DeleteAllPredictionsUseCase(repository=repository)
