"""
ML 모델 로더
저장된 모델을 로드하고 관리
"""

import os
import pickle
from pathlib import Path
from typing import Optional


class ModelLoader:
    """
    머신러닝 모델 로더

    학습된 모델과 스케일러를 로드하여 관리
    """

    def __init__(self, model_dir: str = "models"):
        """
        Parameters:
            model_dir: 모델이 저장된 디렉터리 경로
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None
        self.model_info = {}

    def load_model(self, model_name: str = "exoplanet_model.pkl") -> bool:
        """
        모델 로드

        Parameters:
            model_name: 모델 파일 이름

        Returns:
            로드 성공 여부
        """
        model_path = self.model_dir / model_name

        if not model_path.exists():
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)

            # 모델 정보 추출
            self.model_info = {
                'name': model_name,
                'type': type(self.model).__name__,
                'path': str(model_path)
            }

            return True

        except Exception as e:
            raise RuntimeError(f"모델 로드 중 오류 발생: {str(e)}")

    def load_scaler(self, scaler_name: str = "scaler.pkl") -> bool:
        """
        스케일러 로드

        Parameters:
            scaler_name: 스케일러 파일 이름

        Returns:
            로드 성공 여부
        """
        scaler_path = self.model_dir / scaler_name

        if not scaler_path.exists():
            raise FileNotFoundError(f"스케일러 파일을 찾을 수 없습니다: {scaler_path}")

        try:
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)

            return True

        except Exception as e:
            raise RuntimeError(f"스케일러 로드 중 오류 발생: {str(e)}")

    def load_all(
        self,
        model_name: str = "exoplanet_model.pkl",
        scaler_name: str = "scaler.pkl"
    ) -> bool:
        """
        모델과 스케일러 모두 로드

        Parameters:
            model_name: 모델 파일 이름
            scaler_name: 스케일러 파일 이름

        Returns:
            로드 성공 여부
        """
        self.load_model(model_name)
        self.load_scaler(scaler_name)
        return True

    def get_model(self):
        """로드된 모델 반환"""
        if self.model is None:
            raise RuntimeError("모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")
        return self.model

    def get_scaler(self):
        """로드된 스케일러 반환"""
        if self.scaler is None:
            raise RuntimeError("스케일러가 로드되지 않았습니다. load_scaler()를 먼저 호출하세요.")
        return self.scaler

    def get_model_info(self) -> dict:
        """모델 정보 반환"""
        return self.model_info

    def is_loaded(self) -> bool:
        """모델과 스케일러 로드 여부 확인"""
        return self.model is not None and self.scaler is not None
