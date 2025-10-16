"""
데이터베이스 연결 설정
SQLAlchemy 엔진 및 세션 관리
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

# 데이터베이스 URL 설정
# MySQL: mysql+pymysql://user:password@host:port/database
# 환경변수에서 개별 DB 설정을 가져오거나 전체 DATABASE_URL 사용
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_NAME = os.getenv("DB_NAME", "exoplanet_db")

# DATABASE_URL이 직접 제공되면 사용, 아니면 개별 설정으로 구성
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # MySQL 연결 끊김 방지
    pool_recycle=3600,   # 1시간마다 연결 재사용
    echo=False  # True로 설정하면 SQL 쿼리 로그 출력
)

# 세션 로컬 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스 생성
Base = declarative_base()


def init_db():
    """
    데이터베이스 초기화
    모든 테이블 생성
    """
    from .models import PredictionModel  # noqa
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    """
    데이터베이스 세션 의존성
    FastAPI 라우터에서 사용

    Yields:
        데이터베이스 세션
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
