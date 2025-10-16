"""
SQLAlchemy 데이터베이스 모델
"""

from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON
from datetime import datetime
from .connection import Base


class PredictionModel(Base):
    """
    예측 결과 테이블 모델

    Attributes:
        id: 예측 고유 ID
        light_curve_data: 광도 곡선 데이터 (JSON)
        input_features: 입력 특징값 (JSON) - 통계 계산용
        is_exoplanet: 외계행성 여부
        classification: 분류 (CONFIRMED, CANDIDATE, FALSE_POSITIVE)
        confidence_score: 신뢰도 점수
        planet_probability: 행성 확률
        candidate_probability: 후보 확률
        created_at: 생성 시간
        updated_at: 수정 시간
    """

    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, index=True)  # UUID 길이
    light_curve_data = Column(JSON, nullable=True)
    input_features = Column(JSON, nullable=True)  # 입력 특징값 저장
    is_exoplanet = Column(Boolean, nullable=False)
    classification = Column(String(20), nullable=True, index=True)  # 분류 저장
    confidence_score = Column(Float, nullable=False)
    planet_probability = Column(Float, nullable=False)
    candidate_probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Prediction(id={self.id}, "
            f"is_exoplanet={self.is_exoplanet}, "
            f"confidence_score={self.confidence_score}, "
            f"classification={self.classification})>"
        )
