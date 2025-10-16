"""
외계행성 탐지 모델 테스트 스크립트
학습된 모델을 로드하여 샘플 데이터로 예측 수행
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime


class ExoplanetModelTester:
    """외계행성 탐지 모델 테스터"""

    def __init__(self, model_dir: str = "models"):
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.metadata = None
        self.class_names = ['FALSE POSITIVE', 'CANDIDATE', 'CONFIRMED']

    def load_model(self):
        """모델 및 관련 파일 로드"""
        print("\n" + "="*60)
        print("Loading Model...")
        print("="*60)

        # 모델 로드
        model_path = self.model_dir / "exoplanet_multiclass_model.pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")

        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"[OK] Model loaded: {model_path}")

        # 스케일러 로드
        scaler_path = self.model_dir / "scaler.pkl"
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        print(f"[OK] Scaler loaded: {scaler_path}")

        # 특징 이름 로드
        features_path = self.model_dir / "feature_names.pkl"
        with open(features_path, 'rb') as f:
            self.feature_names = pickle.load(f)
        print(f"[OK] Features loaded: {len(self.feature_names)} features")

        # 메타데이터 로드
        metadata_path = self.model_dir / "model_metadata.pkl"
        if metadata_path.exists():
            with open(metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            print(f"[OK] Metadata loaded")

        print("\n" + "-"*60)
        print("Model Information:")
        print("-"*60)
        if self.metadata:
            print(f"Model Type: {self.metadata.get('model_type', 'N/A')}")
            print(f"Number of Classes: {self.metadata.get('num_classes', 'N/A')}")
            print(f"Class Names: {', '.join(self.metadata.get('class_names', []))}")
            print(f"Feature Count: {self.metadata.get('feature_count', 'N/A')}")

        print(f"\nFeatures used:")
        for i, feature in enumerate(self.feature_names, 1):
            print(f"  {i:2}. {feature}")

    def create_sample_data(self) -> dict:
        """샘플 테스트 데이터 생성"""
        # 전형적인 외계행성 후보 특징값
        samples = {
            "typical_exoplanet": {
                "name": "Typical Exoplanet Candidate",
                "features": {
                    'orbital_period': 3.5,           # 3.5일 주기
                    'transit_duration': 2.5,         # 2.5시간 지속
                    'transit_depth': 500,            # 500 ppm 깊이
                    'planet_radius': 2.0,            # 지구 반지름의 2배
                    'equilibrium_temp': 1200,        # 1200K
                    'insolation': 100,               # 지구 플럭스의 100배
                    'signal_to_noise': 50,           # SNR 50
                    'stellar_temp': 5800,            # 태양과 유사
                    'stellar_logg': 4.5,             # log g
                    'stellar_radius': 1.0            # 태양 반지름
                },
                "description": "태양과 유사한 별 주위를 도는 지구형 행성"
            },
            "hot_jupiter": {
                "name": "Hot Jupiter",
                "features": {
                    'orbital_period': 1.5,           # 매우 짧은 주기
                    'transit_duration': 3.0,         # 긴 지속 시간
                    'transit_depth': 15000,          # 매우 깊은 transit
                    'planet_radius': 10.0,           # 목성급
                    'equilibrium_temp': 2000,        # 매우 뜨거움
                    'insolation': 1000,              # 매우 높은 복사
                    'signal_to_noise': 100,          # 높은 SNR
                    'stellar_temp': 6200,            # 뜨거운 별
                    'stellar_logg': 4.3,
                    'stellar_radius': 1.2
                },
                "description": "별에 매우 가까운 거대 가스 행성 (Hot Jupiter)"
            },
            "earth_analog": {
                "name": "Earth Analog",
                "features": {
                    'orbital_period': 365.0,         # 1년 주기
                    'transit_duration': 13.0,        # ~13시간
                    'transit_depth': 84,             # 지구 크기
                    'planet_radius': 1.0,            # 지구 크기
                    'equilibrium_temp': 288,         # 지구와 유사
                    'insolation': 1.0,               # 지구 플럭스
                    'signal_to_noise': 10,           # 낮은 SNR
                    'stellar_temp': 5778,            # 태양
                    'stellar_logg': 4.44,            # 태양
                    'stellar_radius': 1.0            # 태양
                },
                "description": "지구와 매우 유사한 조건의 행성 (생명체 가능 영역)"
            },
            "false_positive": {
                "name": "Likely False Positive",
                "features": {
                    'orbital_period': 0.5,           # 매우 짧음
                    'transit_duration': 0.5,         # 매우 짧음
                    'transit_depth': 50000,          # 너무 깊음 (항성 식)
                    'planet_radius': 50.0,           # 비정상적으로 큼
                    'equilibrium_temp': 3000,        # 너무 뜨거움
                    'insolation': 10000,             # 비정상적으로 높음
                    'signal_to_noise': 5,            # 낮은 SNR
                    'stellar_temp': 3500,            # 적색왜성
                    'stellar_logg': 5.0,
                    'stellar_radius': 0.5
                },
                "description": "항성 식(stellar eclipse) 가능성이 높은 False Positive"
            }
        }

        return samples

    def predict_sample(self, features: dict) -> dict:
        """샘플 데이터로 예측 수행"""
        # DataFrame 생성
        df = pd.DataFrame([features])

        # 특징 순서 맞추기
        df = df[self.feature_names]

        # 스케일링
        features_scaled = self.scaler.transform(df)

        # 예측
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]

        # 결과 정리
        result = {
            'predicted_class': int(prediction),
            'predicted_label': self.class_names[int(prediction)],
            'probabilities': {
                self.class_names[i]: float(prob)
                for i, prob in enumerate(probabilities)
            },
            'confidence': float(max(probabilities))
        }

        return result

    def print_prediction_result(self, sample_name: str, sample_data: dict, result: dict):
        """예측 결과 출력"""
        print("\n" + "="*60)
        print(f"Sample: {sample_name}")
        print("="*60)

        print(f"\nDescription: {sample_data['description']}")

        print(f"\nInput Features:")
        for feature, value in sample_data['features'].items():
            print(f"  - {feature:20s}: {value:>10.2f}")

        print(f"\n" + "-"*60)
        print("Prediction Results:")
        print("-"*60)

        print(f"\n>> Predicted Class: {result['predicted_label']}")
        print(f">> Confidence: {result['confidence']*100:.2f}%")

        print(f"\nProbabilities for each class:")
        for class_name, prob in result['probabilities'].items():
            bar_length = int(prob * 40)
            bar = "#" * bar_length + "-" * (40 - bar_length)
            print(f"  {class_name:15s} {bar} {prob*100:5.2f}%")

    def run_tests(self):
        """전체 테스트 실행"""
        print("\n" + "="*60)
        print("EXOPLANET MODEL TESTING")
        print("="*60)
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 모델 로드
        self.load_model()

        # 샘플 데이터 생성
        samples = self.create_sample_data()

        # 각 샘플에 대해 예측
        for sample_name, sample_data in samples.items():
            result = self.predict_sample(sample_data['features'])
            self.print_prediction_result(sample_name, sample_data, result)

        print("\n" + "="*60)
        print("Testing Completed!")
        print("="*60)

    def interactive_test(self):
        """대화형 테스트 모드"""
        print("\n" + "="*60)
        print("Interactive Test Mode")
        print("="*60)
        print("\n모델에 임의의 값을 입력하여 예측을 테스트할 수 있습니다.")
        print("종료하려면 'quit'를 입력하세요.\n")

        while True:
            try:
                print("\n" + "-"*60)
                print("특징값 입력 (Enter를 누르면 기본값 사용):")
                print("-"*60)

                features = {}
                defaults = {
                    'orbital_period': 3.5,
                    'transit_duration': 2.5,
                    'transit_depth': 500,
                    'planet_radius': 2.0,
                    'equilibrium_temp': 1200,
                    'insolation': 100,
                    'signal_to_noise': 50,
                    'stellar_temp': 5800,
                    'stellar_logg': 4.5,
                    'stellar_radius': 1.0
                }

                for feature in self.feature_names:
                    default = defaults.get(feature, 0.0)
                    value_str = input(f"  {feature} (default: {default}): ").strip()

                    if value_str.lower() == 'quit':
                        return

                    if value_str == '':
                        value = default
                    else:
                        try:
                            value = float(value_str)
                        except ValueError:
                            print(f"  [Warning] Invalid input, using default: {default}")
                            value = default

                    features[feature] = value

                # 예측 수행
                result = self.predict_sample(features)

                # 결과 출력
                sample_data = {
                    'description': 'User provided custom values',
                    'features': features
                }
                self.print_prediction_result("Custom Input", sample_data, result)

                # 계속할지 물어보기
                cont = input("\n다른 값을 테스트하시겠습니까? (y/n): ").strip().lower()
                if cont != 'y':
                    break

            except KeyboardInterrupt:
                print("\n\n테스트를 종료합니다.")
                break


def main():
    """메인 함수"""
    import sys

    tester = ExoplanetModelTester()

    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        # 대화형 모드
        tester.load_model()
        tester.interactive_test()
    else:
        # 자동 테스트 모드
        tester.run_tests()


if __name__ == "__main__":
    main()
