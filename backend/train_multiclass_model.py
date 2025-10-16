"""
외계행성 다중 클래스 분류 ML 모델 학습
NASA Kepler/K2/TESS 데이터를 통합하여 사용

분류 클래스:
- 0: FALSE POSITIVE (거짓 양성)
- 1: CANDIDATE (행성 후보)
- 2: CONFIRMED (확인된 외계행성)
"""

import os
import sys
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import (
    StackingClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)
import lightgbm as lgb
import xgboost as xgb
import optuna
from sklearn.neural_network import MLPClassifier
import warnings
warnings.filterwarnings('ignore')
optuna.logging.set_verbosity(optuna.logging.WARNING)


class MultiClassExoplanetTrainer:
    """외계행성 다중 클래스 분류 모델 학습기"""

    def __init__(self, data_dir: str = "../data", model_dir: str = "models"):
        self.data_dir = Path(data_dir)
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.class_names = ['FALSE POSITIVE', 'CANDIDATE', 'CONFIRMED']
        self.roc_metrics = None  # ROC 메트릭 저장용
        self.distribution_metrics = None  # 분포 메트릭 저장용
        self.best_params = None  # Optuna 최적 파라미터 저장용

        # 모델 저장 디렉터리 생성
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def load_kepler_data(self) -> pd.DataFrame:
        """Kepler KOI 데이터 로드"""
        print("\n" + "="*50)
        print("Loading Kepler KOI data...")
        print("="*50)

        file_path = self.data_dir / "cumulative_2025.10.14_06.16.25.csv"
        df = pd.read_csv(file_path, comment='#', low_memory=False)

        # 타겟 매핑
        disposition_map = {
            'FALSE POSITIVE': 0,
            'CANDIDATE': 1,
            'CONFIRMED': 2
        }

        df['label'] = df['koi_disposition'].map(disposition_map)
        df = df.dropna(subset=['label'])  # 매핑되지 않은 값 제거

        print(f"Loaded {len(df)} Kepler samples")
        print(f"Class distribution:\n{df['label'].value_counts().sort_index()}")

        return df

    def load_tess_data(self) -> pd.DataFrame:
        """TESS TOI 데이터 로드"""
        print("\n" + "="*50)
        print("Loading TESS TOI data...")
        print("="*50)

        file_path = self.data_dir / "TOI_2025.10.14_06.16.33.csv"
        df = pd.read_csv(file_path, comment='#', low_memory=False)

        # TESS disposition 매핑
        disposition_map = {
            'FP': 0,      # False Positive
            'PC': 1,      # Planet Candidate
            'APC': 1,     # Ambiguous Planet Candidate -> Candidate로 취급
            'CP': 2,      # Confirmed Planet
            'KP': 2       # Known Planet -> Confirmed로 취급
        }

        df['label'] = df['tfopwg_disp'].map(disposition_map)
        df = df.dropna(subset=['label'])

        print(f"Loaded {len(df)} TESS samples")
        print(f"Class distribution:\n{df['label'].value_counts().sort_index()}")

        return df

    def load_k2_data(self) -> pd.DataFrame:
        """K2 데이터 로드"""
        print("\n" + "="*50)
        print("Loading K2 data...")
        print("="*50)

        file_path = self.data_dir / "k2pandc_2025.10.14_06.16.39.csv"
        df = pd.read_csv(file_path, comment='#', low_memory=False)

        # K2 disposition 매핑 (Kepler와 동일)
        disposition_map = {
            'FALSE POSITIVE': 0,
            'CANDIDATE': 1,
            'CONFIRMED': 2,
            'REFUTED': 0  # REFUTED는 FALSE POSITIVE로 취급
        }

        df['label'] = df['disposition'].map(disposition_map)
        df = df.dropna(subset=['label'])

        print(f"Loaded {len(df)} K2 samples")
        print(f"Class distribution:\n{df['label'].value_counts().sort_index()}")

        return df

    def integrate_datasets(self, kepler_df: pd.DataFrame, tess_df: pd.DataFrame, k2_df: pd.DataFrame) -> pd.DataFrame:
        """
        데이터셋 통합 (Kepler + TESS + K2)
        공통 특징 선택 및 정규화
        """
        print("\n" + "="*50)
        print("Integrating 3 datasets (Kepler + TESS + K2)...")
        print("="*50)

        # 공통 특징 매핑
        kepler_features = {
            'koi_period': 'orbital_period',
            'koi_duration': 'transit_duration',
            'koi_depth': 'transit_depth',
            'koi_prad': 'planet_radius',
            'koi_teq': 'equilibrium_temp',
            'koi_insol': 'insolation',
            'koi_model_snr': 'signal_to_noise',
            'koi_steff': 'stellar_temp',
            'koi_slogg': 'stellar_logg',
            'koi_srad': 'stellar_radius'
        }

        tess_features = {
            'pl_orbper': 'orbital_period',
            'pl_trandurh': 'transit_duration',
            'pl_trandep': 'transit_depth',
            'pl_rade': 'planet_radius',
            'pl_eqt': 'equilibrium_temp',
            'pl_insol': 'insolation',
            # TOI에는 SNR이 없음
            'st_teff': 'stellar_temp',
            'st_logg': 'stellar_logg',
            'st_rad': 'stellar_radius'
        }

        # K2는 NASA Exoplanet Archive 포맷 (Kepler와 유사하지만 다름)
        k2_features = {
            'pl_orbper': 'orbital_period',
            # K2에는 transit_duration이 없음
            'pl_rade': 'planet_radius',
            'pl_eqt': 'equilibrium_temp',
            'pl_insol': 'insolation',
            'st_teff': 'stellar_temp',
            'st_logg': 'stellar_logg',
            'st_rad': 'stellar_radius'
        }

        # Kepler 데이터 변환
        kepler_common = kepler_df.rename(columns=kepler_features)
        kepler_common = kepler_common[list(kepler_features.values()) + ['label']]
        kepler_common['source'] = 'kepler'

        # TESS 데이터 변환
        tess_common = tess_df.rename(columns=tess_features)
        if 'signal_to_noise' not in tess_common.columns:
            tess_common['signal_to_noise'] = np.nan
        tess_common = tess_common[list(kepler_features.values()) + ['label']]
        tess_common['source'] = 'tess'

        # K2 데이터 변환
        k2_common = k2_df.rename(columns=k2_features)
        # K2에 없는 컬럼들 추가 (NaN으로)
        missing_cols = ['transit_duration', 'transit_depth', 'signal_to_noise']
        for col in missing_cols:
            if col not in k2_common.columns:
                k2_common[col] = np.nan
        k2_common = k2_common[list(kepler_features.values()) + ['label']]
        k2_common['source'] = 'k2'

        # 3개 데이터셋 통합
        combined_df = pd.concat([kepler_common, tess_common, k2_common], ignore_index=True)

        print(f"\nCombined dataset: {len(combined_df)} total samples")
        print(f"  Kepler: {len(kepler_common)}")
        print(f"  TESS:   {len(tess_common)}")
        print(f"  K2:     {len(k2_common)}")
        print(f"\nClass distribution in combined data:")
        for i in range(3):
            count = (combined_df['label'] == i).sum()
            print(f"  Class {i} ({self.class_names[i]}): {count}")
        print(f"\nSource distribution:")
        print(combined_df['source'].value_counts())

        return combined_df

    def preprocess_data(self, df: pd.DataFrame) -> tuple:
        """데이터 전처리"""
        print("\n" + "="*50)
        print("Preprocessing data...")
        print("="*50)

        # 레이블 추출
        y = df['label'].astype(int)

        # 특징 추출 (source와 label 제외)
        X = df.drop(columns=['label', 'source'])

        # 결측치가 너무 많은 컬럼 제거 (70% 이상)
        missing_threshold = 0.7
        missing_ratio = X.isnull().sum() / len(X)
        cols_to_drop = missing_ratio[missing_ratio > missing_threshold].index
        X = X.drop(columns=cols_to_drop)

        if len(cols_to_drop) > 0:
            print(f"Dropped {len(cols_to_drop)} columns with >70% missing values:")
            print(f"  {list(cols_to_drop)}")

        # 결측치 처리 (median)
        X = X.fillna(X.median())

        # 무한값 처리
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())

        # 숫자형만 선택
        X = X.select_dtypes(include=[np.number])

        # Feature Engineering - 새로운 특징 생성
        print("\n" + "-"*50)
        print("Feature Engineering...")
        print("-"*50)

        # 1. Transit depth per planet radius squared (밀도 관련)
        if 'transit_depth' in X.columns and 'planet_radius' in X.columns:
            X['depth_per_radius_sq'] = X['transit_depth'] / (X['planet_radius'] ** 2 + 1e-10)
            print("  [+] Added: depth_per_radius_sq")

        # 2. Planet to stellar radius ratio (상대적 크기)
        if 'planet_radius' in X.columns and 'stellar_radius' in X.columns:
            X['planet_star_radius_ratio'] = X['planet_radius'] / (X['stellar_radius'] + 1e-10)
            print("  [+] Added: planet_star_radius_ratio")

        # 3. Temperature ratio (온도 비율)
        if 'equilibrium_temp' in X.columns and 'stellar_temp' in X.columns:
            X['temp_ratio'] = X['equilibrium_temp'] / (X['stellar_temp'] + 1e-10)
            print("  [+] Added: temp_ratio")

        # 4. Orbital-transit interaction (궤도-통과 상호작용)
        if 'orbital_period' in X.columns and 'transit_duration' in X.columns:
            X['orbit_transit_product'] = X['orbital_period'] * X['transit_duration']
            print("  [+] Added: orbit_transit_product")

        # 5. Signal strength (신호 강도)
        if 'signal_to_noise' in X.columns and 'transit_depth' in X.columns:
            X['signal_strength'] = X['signal_to_noise'] * X['transit_depth']
            print("  [+] Added: signal_strength")

        # 무한값 및 NaN 처리 (새로운 특징에서 발생할 수 있음)
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())

        print(f"Total engineered features: {X.shape[1] - 10}")

        # 특징 이름 저장
        self.feature_names = X.columns.tolist()

        print(f"\nFinal features: {len(self.feature_names)}")
        print(f"Features: {self.feature_names}")

        print(f"\nFinal class distribution:")
        for i, class_name in enumerate(self.class_names):
            count = (y == i).sum()
            percentage = count / len(y) * 100
            print(f"  Class {i} ({class_name}): {count} ({percentage:.1f}%)")

        return X, y

    def optimize_hyperparameters(self, X, y, n_trials=100):
        """
        Optuna를 사용한 하이퍼파라미터 최적화

        Args:
            X: 특징 데이터
            y: 타겟 데이터
            n_trials: Optuna 시행 횟수
        """
        print("\n" + "="*50)
        print(f"Optimizing hyperparameters with Optuna ({n_trials} trials)...")
        print("="*50)

        # 데이터 분할 및 스케일링
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        def objective(trial):
            """Optuna objective function"""
            # LightGBM 파라미터
            lgbm_params = {
                'n_estimators': trial.suggest_int('lgbm_n_estimators', 200, 500),
                'max_depth': trial.suggest_int('lgbm_max_depth', 6, 12),
                'learning_rate': trial.suggest_float('lgbm_learning_rate', 0.01, 0.15),
                'num_leaves': trial.suggest_int('lgbm_num_leaves', 20, 60),
            }

            # XGBoost 파라미터
            xgb_params = {
                'n_estimators': trial.suggest_int('xgb_n_estimators', 200, 500),
                'max_depth': trial.suggest_int('xgb_max_depth', 5, 10),
                'learning_rate': trial.suggest_float('xgb_learning_rate', 0.01, 0.15),
            }

            # GradientBoosting 파라미터
            gb_params = {
                'n_estimators': trial.suggest_int('gb_n_estimators', 150, 400),
                'max_depth': trial.suggest_int('gb_max_depth', 4, 8),
                'learning_rate': trial.suggest_float('gb_learning_rate', 0.01, 0.15),
            }

            # RandomForest 파라미터
            rf_params = {
                'n_estimators': trial.suggest_int('rf_n_estimators', 100, 300),
                'max_depth': trial.suggest_int('rf_max_depth', 8, 20),
                'min_samples_split': trial.suggest_int('rf_min_samples_split', 2, 10),
            }

            # MLP 파라미터
            mlp_hidden_size = trial.suggest_int('mlp_hidden_size', 64, 256)
            mlp_alpha = trial.suggest_float('mlp_alpha', 0.0001, 0.01, log=True)

            # 모델 생성
            estimators = [
                ('lgbm', lgb.LGBMClassifier(
                    **lgbm_params,
                    random_state=42,
                    verbose=-1,
                    objective='multiclass',
                    num_class=3,
                    class_weight='balanced'
                )),
                ('xgb', xgb.XGBClassifier(
                    **xgb_params,
                    random_state=42,
                    eval_metric='mlogloss',
                    verbosity=0
                )),
                ('gb', GradientBoostingClassifier(
                    **gb_params,
                    random_state=42
                )),
                ('rf', RandomForestClassifier(
                    **rf_params,
                    random_state=42,
                    class_weight='balanced',
                    n_jobs=-1
                )),
                ('mlp', MLPClassifier(
                    hidden_layer_sizes=(mlp_hidden_size, mlp_hidden_size // 2),
                    alpha=mlp_alpha,
                    random_state=42,
                    max_iter=500,
                    early_stopping=True
                ))
            ]

            # Stacking 모델
            model = StackingClassifier(
                estimators=estimators,
                final_estimator=LogisticRegression(
                    multi_class='multinomial',
                    max_iter=1500,
                    random_state=42,
                    class_weight='balanced'
                ),
                cv=3,  # 빠른 최적화를 위해 3-fold
                n_jobs=-1
            )

            # 훈련 및 평가
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_val_scaled)
            accuracy = accuracy_score(y_val, y_pred)

            return accuracy

        # Optuna 최적화 실행
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

        print(f"\nOptimization completed!")
        print(f"Best accuracy: {study.best_value:.4f}")
        print(f"Best parameters:")
        for key, value in study.best_params.items():
            print(f"  {key}: {value}")

        # 최적 파라미터 저장
        self.best_params = study.best_params

        return study.best_params

    def create_multiclass_model(self):
        """다중 클래스 분류 Stacking 모델 생성 (Optuna 최적화 버전 + MLP)"""
        print("\n" + "="*50)
        print("Creating optimized multi-class stacking model...")
        print("="*50)

        # 최적 파라미터가 있으면 사용, 없으면 기본값
        if self.best_params:
            print("Using Optuna-optimized parameters")
            params = self.best_params
        else:
            print("Using default parameters (no optimization)")
            params = {
                'lgbm_n_estimators': 300,
                'lgbm_max_depth': 8,
                'lgbm_learning_rate': 0.08,
                'lgbm_num_leaves': 31,
                'xgb_n_estimators': 300,
                'xgb_max_depth': 7,
                'xgb_learning_rate': 0.08,
                'gb_n_estimators': 250,
                'gb_max_depth': 6,
                'gb_learning_rate': 0.08,
                'rf_n_estimators': 150,
                'rf_max_depth': 12,
                'rf_min_samples_split': 2,
                'mlp_hidden_size': 128,
                'mlp_alpha': 0.0001
            }

        # Base 모델들 (5개: LightGBM, XGBoost, GradientBoosting, RandomForest, MLP)
        estimators = [
            ('lgbm', lgb.LGBMClassifier(
                n_estimators=params.get('lgbm_n_estimators', 300),
                max_depth=params.get('lgbm_max_depth', 8),
                learning_rate=params.get('lgbm_learning_rate', 0.08),
                num_leaves=params.get('lgbm_num_leaves', 31),
                random_state=42,
                verbose=-1,
                objective='multiclass',
                num_class=3,
                class_weight='balanced'
            )),
            ('xgb', xgb.XGBClassifier(
                n_estimators=params.get('xgb_n_estimators', 300),
                max_depth=params.get('xgb_max_depth', 7),
                learning_rate=params.get('xgb_learning_rate', 0.08),
                random_state=42,
                eval_metric='mlogloss',
                verbosity=0
            )),
            ('gb', GradientBoostingClassifier(
                n_estimators=params.get('gb_n_estimators', 250),
                max_depth=params.get('gb_max_depth', 6),
                learning_rate=params.get('gb_learning_rate', 0.08),
                random_state=42
            )),
            ('rf', RandomForestClassifier(
                n_estimators=params.get('rf_n_estimators', 150),
                max_depth=params.get('rf_max_depth', 12),
                min_samples_split=params.get('rf_min_samples_split', 2),
                random_state=42,
                class_weight='balanced',
                n_jobs=-1
            )),
            ('mlp', MLPClassifier(
                hidden_layer_sizes=(
                    params.get('mlp_hidden_size', 128),
                    params.get('mlp_hidden_size', 128) // 2
                ),
                alpha=params.get('mlp_alpha', 0.0001),
                random_state=42,
                max_iter=500,
                early_stopping=True
            ))
        ]

        # Stacking 모델
        model = StackingClassifier(
            estimators=estimators,
            final_estimator=LogisticRegression(
                multi_class='multinomial',
                max_iter=1500,
                random_state=42,
                class_weight='balanced'
            ),
            cv=5,
            n_jobs=-1
        )

        print(f"Model configuration:")
        print(f"  - Base models: {len(estimators)} (LightGBM, XGBoost, GB, RF, MLP)")
        print(f"  - Class weight: balanced")
        print(f"  - Ensemble: 5-fold CV stacking")

        return model

    def train(self, X, y):
        """모델 학습"""
        print("\n" + "="*50)
        print("Training multi-class model...")
        print("="*50)

        # 데이터 분할 (층화 추출)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"\nTrain set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")

        # 각 세트의 클래스 분포
        print(f"\nTrain class distribution:")
        for i, class_name in enumerate(self.class_names):
            count = (y_train == i).sum()
            print(f"  {class_name}: {count}")

        print(f"\nTest class distribution:")
        for i, class_name in enumerate(self.class_names):
            count = (y_test == i).sum()
            print(f"  {class_name}: {count}")

        # 스케일링
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # 모델 학습
        self.model = self.create_multiclass_model()

        print("\nTraining stacking model (this may take a while)...")
        self.model.fit(X_train_scaled, y_train)

        # 예측
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)

        # 평가
        self.evaluate(y_test, y_pred, y_pred_proba)

        # ROC 곡선 계산 (Binary classification으로 변환: 외계행성 vs 비외계행성)
        # Class 2 (CONFIRMED)를 양성으로, 나머지를 음성으로 변환
        print("\n" + "="*50)
        print("Calculating ROC curve metrics...")
        print("="*50)

        # Binary classification으로 변환 (CONFIRMED vs 나머지)
        y_test_binary = (y_test == 2).astype(int)  # CONFIRMED = 1, 나머지 = 0
        y_proba_positive = y_pred_proba[:, 2]      # CONFIRMED 클래스 확률

        # ROC 곡선 계산
        fpr, tpr, thresholds = roc_curve(y_test_binary, y_proba_positive)
        roc_auc = auc(fpr, tpr)

        # ROC 메트릭 저장
        self.roc_metrics = {
            'fpr': fpr.tolist(),
            'tpr': tpr.tolist(),
            'thresholds': thresholds.tolist(),
            'auc': float(roc_auc)
        }

        print(f"\nROC AUC Score: {roc_auc:.4f}")
        print(f"FPR/TPR points: {len(fpr)}")

        return X_test_scaled, y_test, y_pred, y_pred_proba

    def calculate_distributions(self, X: pd.DataFrame):
        """원본 데이터의 특징 분포 계산"""
        print("\n" + "="*50)
        print("Calculating feature distributions...")
        print("="*50)

        def create_histogram(data, edges):
            """히스토그램 생성"""
            if len(data) == 0:
                bins = [f"{edges[i]}-{edges[i+1]}" for i in range(len(edges)-1)]
                counts = [0] * (len(edges)-1)
                return bins, counts

            # numpy histogram 사용
            counts, _ = np.histogram(data, bins=edges)
            bins = [f"{edges[i]}-{edges[i+1]}" for i in range(len(edges)-1)]

            return bins, counts.tolist()

        # Planet Radius 분포
        if 'planet_radius' in X.columns:
            planet_radii = X['planet_radius'].dropna().values
            radius_edges = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
            radius_bins, radius_counts = create_histogram(planet_radii, radius_edges)
            print(f"\nPlanet Radius distribution: {len(planet_radii)} valid samples")
        else:
            radius_bins, radius_counts = [], []
            print("\nPlanet Radius not available in dataset")

        # Transit Duration 분포
        if 'transit_duration' in X.columns:
            transit_durations = X['transit_duration'].dropna().values
            duration_edges = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24]
            duration_bins, duration_counts = create_histogram(transit_durations, duration_edges)
            print(f"Transit Duration distribution: {len(transit_durations)} valid samples")
        else:
            duration_bins, duration_counts = [], []
            print("Transit Duration not available in dataset")

        # 분포 메트릭 저장
        self.distribution_metrics = {
            'planet_radius_distribution': {
                'bins': radius_bins,
                'counts': radius_counts
            },
            'transit_duration_distribution': {
                'bins': duration_bins,
                'counts': duration_counts
            },
            'total_samples': len(X),
            'features_available': {
                'planet_radius': 'planet_radius' in X.columns,
                'transit_duration': 'transit_duration' in X.columns
            }
        }

        print(f"\nDistribution metrics calculated successfully")

    def evaluate(self, y_test, y_pred, y_pred_proba):
        """모델 평가"""
        print("\n" + "="*50)
        print("Model Evaluation (Multi-Class)")
        print("="*50)

        # 전체 정확도
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nOverall Accuracy: {accuracy:.4f}")

        # 클래스별 메트릭
        precision = precision_score(y_test, y_pred, average=None)
        recall = recall_score(y_test, y_pred, average=None)
        f1 = f1_score(y_test, y_pred, average=None)

        print(f"\nPer-Class Metrics:")
        for i, class_name in enumerate(self.class_names):
            print(f"\n{class_name}:")
            print(f"  Precision: {precision[i]:.4f}")
            print(f"  Recall:    {recall[i]:.4f}")
            print(f"  F1 Score:  {f1[i]:.4f}")

        # 분류 리포트
        print("\n" + "-"*50)
        print("Classification Report:")
        print("-"*50)
        print(classification_report(y_test, y_pred, target_names=self.class_names))

        # 혼동 행렬
        print("\n" + "-"*50)
        print("Confusion Matrix:")
        print("-"*50)
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n{'':20} {'Predicted →':>50}")
        print(f"{'Actual ↓':20} {' '.join([f'{name:>15}' for name in self.class_names])}")
        for i, class_name in enumerate(self.class_names):
            print(f"{class_name:20} {' '.join([f'{cm[i, j]:>15}' for j in range(3)])}")

    def save_model(self, model_name: str = "exoplanet_multiclass_model.pkl"):
        """모델 저장"""
        if self.model is None:
            raise ValueError("모델이 학습되지 않았습니다")

        model_path = self.model_dir / model_name
        scaler_path = self.model_dir / "scaler.pkl"
        features_path = self.model_dir / "feature_names.pkl"
        metadata_path = self.model_dir / "model_metadata.pkl"
        roc_path = self.model_dir / "roc_metrics.pkl"
        distribution_path = self.model_dir / "distribution_metrics.pkl"

        print(f"\n" + "="*50)
        print(f"Saving model...")
        print("="*50)

        # 모델 저장
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)

        # 스케일러 저장
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)

        # 특징 이름 저장
        with open(features_path, 'wb') as f:
            pickle.dump(self.feature_names, f)

        # 메타데이터 저장
        metadata = {
            'model_type': 'multi-class',
            'num_classes': 3,
            'class_names': self.class_names,
            'feature_count': len(self.feature_names),
            'features': self.feature_names
        }
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)

        # ROC 메트릭 저장
        if self.roc_metrics is not None:
            with open(roc_path, 'wb') as f:
                pickle.dump(self.roc_metrics, f)
            print(f"ROC metrics saved: {roc_path}")

        # 분포 메트릭 저장
        if self.distribution_metrics is not None:
            with open(distribution_path, 'wb') as f:
                pickle.dump(self.distribution_metrics, f)
            print(f"Distribution metrics saved: {distribution_path}")

        print(f"\nModel saved: {model_path}")
        print(f"Scaler saved: {scaler_path}")
        print(f"Features saved: {features_path}")
        print(f"Metadata saved: {metadata_path}")

    def run(self, optimize=True, n_trials=100):
        """
        전체 학습 파이프라인 실행

        Args:
            optimize: Optuna 최적화 여부 (기본값: True)
            n_trials: Optuna 최적화 시행 횟수 (기본값: 100)
        """
        try:
            print("\n" + "="*70)
            print("MULTI-CLASS EXOPLANET CLASSIFICATION MODEL TRAINING")
            print("="*70)

            # 1. 데이터 로드
            kepler_df = self.load_kepler_data()
            tess_df = self.load_tess_data()
            k2_df = self.load_k2_data()

            # 2. 데이터 통합 (3개 데이터셋)
            combined_df = self.integrate_datasets(kepler_df, tess_df, k2_df)

            # 3. 전처리
            X, y = self.preprocess_data(combined_df)

            # 4. 하이퍼파라미터 최적화 (선택적)
            if optimize:
                self.optimize_hyperparameters(X, y, n_trials=n_trials)
            else:
                print("\nSkipping hyperparameter optimization...")

            # 5. 분포 계산 (원본 데이터 사용)
            self.calculate_distributions(X)

            # 6. 학습
            X_test, y_test, y_pred, y_pred_proba = self.train(X, y)

            # 7. 모델 저장
            self.save_model()

            print("\n" + "="*70)
            print("TRAINING COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"\nModel Type: Multi-Class Classification (3 classes)")
            print(f"Classes: {', '.join(self.class_names)}")
            print(f"Total Samples: {len(X)}")
            print(f"Features: {len(self.feature_names)}")

        except Exception as e:
            print(f"\nError during training: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    trainer = MultiClassExoplanetTrainer()
    trainer.run()
