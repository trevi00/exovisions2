# 7. 모델 학습 (Model Training)

## 🎯 모델 학습 개요

추출한 특징들로 **Gradient Boosted Trees (GBT)** 모델을 학습합니다.

```
[입력] 특징 배열 (789개 특징)  +  레이블 (0 or 1)
           ↓
    [GBT 모델 학습]
           ↓
[출력] 행성 탐지 분류기
```

## 🌲 LightGBM 설정

### 기본 설정

```python
import lightgbm as lgb

# 모델 생성
model = lgb.LGBMClassifier(
    objective='binary',       # 이진 분류
    metric='auc',            # 평가 지표: AUC
    boosting_type='gbdt',    # Gradient Boosting Decision Tree
    n_estimators=100,        # 트리 개수
    max_depth=5,             # 트리 최대 깊이
    learning_rate=0.1,       # 학습률
    num_leaves=31,           # 리프 노드 수
    min_child_samples=20,    # 리프의 최소 샘플 수
    subsample=0.8,           # 행 샘플링 비율
    colsample_bytree=0.8,    # 열 샘플링 비율
    random_state=42,         # 재현성
    n_jobs=-1                # 모든 CPU 코어 사용
)
```

## 📊 학습 데이터 준비

### 데이터 분할

```python
from sklearn.model_selection import train_test_split

# 전체 데이터
X = features_scaled  # (N, 789)
y = labels          # (N,) - 0 or 1

# 학습/검증/테스트 분할
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.111, random_state=42, stratify=y_temp
)

print(f"학습 세트: {X_train.shape}")  # (80%, 789)
print(f"검증 세트: {X_val.shape}")    # (10%, 789)
print(f"테스트 세트: {X_test.shape}")  # (10%, 789)
```

### 클래스 불균형 처리

```python
from collections import Counter

# 클래스 분포 확인
print("클래스 분포:")
print(f"  학습: {Counter(y_train)}")
print(f"  검증: {Counter(y_val)}")
print(f"  테스트: {Counter(y_test)}")

# TESS 예시:
# 학습: {0: 11000, 1: 400}  ← 심한 불균형!
# 검증: {0: 1400, 1: 50}
# 테스트: {0: 1400, 1: 50}

# 클래스 가중치 설정
from sklearn.utils.class_weight import compute_sample_weight

sample_weights = compute_sample_weight(
    class_weight='balanced',
    y=y_train
)

# 또는 모델에서 직접 설정
model = lgb.LGBMClassifier(
    class_weight='balanced',  # 자동 가중치 조정
    ...
)
```

## 🔧 10-Fold 교차 검증

### 교차 검증 구현

```python
from sklearn.model_selection import StratifiedKFold
import numpy as np

# 10-Fold CV
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# 결과 저장
cv_scores = []
cv_models = []

for fold, (train_idx, val_idx) in enumerate(kfold.split(X_train, y_train)):
    print(f"\n========== Fold {fold + 1}/10 ==========")

    # 데이터 분할
    X_tr = X_train[train_idx]
    y_tr = y_train[train_idx]
    X_vl = X_train[val_idx]
    y_vl = y_train[val_idx]

    # 모델 학습
    model = lgb.LGBMClassifier(**params)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_vl, y_vl)],
        eval_metric='auc',
        early_stopping_rounds=50,
        verbose=100
    )

    # 검증 점수
    y_pred = model.predict_proba(X_vl)[:, 1]
    auc = roc_auc_score(y_vl, y_pred)
    cv_scores.append(auc)
    cv_models.append(model)

    print(f"Fold {fold + 1} AUC: {auc:.4f}")

# 평균 성능
print(f"\n평균 AUC: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

### Early Stopping

```python
# 과적합 방지: 검증 성능이 개선되지 않으면 중단
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50,  # 50 에폭 동안 개선 없으면 중단
    verbose=100
)

print(f"최적 반복 횟수: {model.best_iteration_}")
```

## 🎛️ 하이퍼파라미터 최적화

### 1단계: AUC 최대화

```python
from sklearn.model_selection import GridSearchCV

# 탐색할 하이퍼파라미터 공간
param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'num_leaves': [15, 31, 63, 127],
    'min_child_samples': [10, 20, 30],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
}

# Grid Search
grid_search = GridSearchCV(
    estimator=lgb.LGBMClassifier(),
    param_grid=param_grid,
    scoring='roc_auc',
    cv=StratifiedKFold(n_splits=10),
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train)

# 최적 파라미터
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print(f"최적 AUC: {best_score:.4f}")
print(f"최적 파라미터: {best_params}")
```

### 2단계: 임계값 최적화

```python
# 최적 모델로 예측
model = lgb.LGBMClassifier(**best_params)
model.fit(X_train, y_train)

# 검증 세트에서 확률 예측
y_proba = model.predict_proba(X_val)[:, 1]

# 다양한 임계값 시도
thresholds = np.arange(0.1, 0.9, 0.05)
best_threshold = 0.5
best_recall = 0

for threshold in thresholds:
    y_pred = (y_proba >= threshold).astype(int)

    recall = recall_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)

    # Recall 최대화 (단, Precision > 0.7 유지)
    if recall > best_recall and precision > 0.7:
        best_recall = recall
        best_threshold = threshold

print(f"최적 임계값: {best_threshold:.2f}")
print(f"Recall: {best_recall:.4f}")
```

## 📈 학습 과정 시각화

### 학습 곡선

```python
import matplotlib.pyplot as plt

# 학습 이력
history = model.evals_result_

# 그래프
plt.figure(figsize=(12, 5))

# AUC
plt.subplot(1, 2, 1)
plt.plot(history['training']['auc'], label='Train')
plt.plot(history['valid_1']['auc'], label='Validation')
plt.xlabel('Iteration')
plt.ylabel('AUC')
plt.title('AUC over Iterations')
plt.legend()
plt.grid(True)

# Loss
plt.subplot(1, 2, 2)
plt.plot(history['training']['binary_logloss'], label='Train')
plt.plot(history['valid_1']['binary_logloss'], label='Validation')
plt.xlabel('Iteration')
plt.ylabel('Binary Log Loss')
plt.title('Loss over Iterations')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
```

### 특징 중요도

```python
# 특징 중요도
feature_importance = model.feature_importances_

# 상위 20개
top_20_idx = np.argsort(feature_importance)[-20:]
top_20_names = feature_names[top_20_idx]
top_20_scores = feature_importance[top_20_idx]

# 시각화
plt.figure(figsize=(10, 8))
plt.barh(range(20), top_20_scores)
plt.yticks(range(20), top_20_names, fontsize=8)
plt.xlabel('Importance')
plt.title('Top 20 Most Important Features')
plt.tight_layout()
plt.show()
```

## 🎯 최종 모델 학습

### 전체 학습 데이터로 재학습

```python
# 최적 파라미터와 임계값 확정
final_params = {
    **best_params,
    'n_estimators': model.best_iteration_  # Early stopping 반영
}

# 학습+검증 데이터 결합
X_full_train = np.vstack([X_train, X_val])
y_full_train = np.hstack([y_train, y_val])

# 최종 모델 학습
final_model = lgb.LGBMClassifier(**final_params)
final_model.fit(X_full_train, y_full_train)

print("최종 모델 학습 완료!")
```

## 💾 모델 저장 및 로드

```python
import pickle
import joblib

# 방법 1: pickle
with open('exoplanet_model.pkl', 'wb') as f:
    pickle.dump(final_model, f)

# 방법 2: joblib (더 효율적)
joblib.dump(final_model, 'exoplanet_model.joblib')

# 로드
model_loaded = joblib.load('exoplanet_model.joblib')

# 예측
y_pred = model_loaded.predict(X_test)
```

## 🔄 완전한 학습 파이프라인

```python
class ExoplanetTrainer:
    """외계행성 탐지 모델 학습 클래스"""

    def __init__(self, params=None):
        self.params = params or self._default_params()
        self.model = None
        self.threshold = 0.5
        self.scaler = None

    def _default_params(self):
        return {
            'objective': 'binary',
            'metric': 'auc',
            'n_estimators': 100,
            'max_depth': 5,
            'learning_rate': 0.1,
            'num_leaves': 31,
            'random_state': 42
        }

    def train(self, X_train, y_train, X_val=None, y_val=None):
        """모델 학습"""
        self.model = lgb.LGBMClassifier(**self.params)

        if X_val is not None:
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                early_stopping_rounds=50,
                verbose=100
            )
        else:
            self.model.fit(X_train, y_train)

        return self

    def optimize_threshold(self, X_val, y_val, target_recall=0.9):
        """임계값 최적화"""
        y_proba = self.model.predict_proba(X_val)[:, 1]

        best_threshold = 0.5
        best_precision = 0

        for threshold in np.arange(0.1, 0.9, 0.01):
            y_pred = (y_proba >= threshold).astype(int)
            recall = recall_score(y_val, y_pred)
            precision = precision_score(y_val, y_pred)

            if recall >= target_recall and precision > best_precision:
                best_precision = precision
                best_threshold = threshold

        self.threshold = best_threshold
        print(f"최적 임계값: {self.threshold:.3f}")
        return self

    def predict(self, X):
        """예측"""
        y_proba = self.model.predict_proba(X)[:, 1]
        y_pred = (y_proba >= self.threshold).astype(int)
        return y_pred

    def predict_proba(self, X):
        """확률 예측"""
        return self.model.predict_proba(X)[:, 1]

    def save(self, filepath):
        """모델 저장"""
        joblib.dump({
            'model': self.model,
            'threshold': self.threshold,
            'params': self.params
        }, filepath)

    @classmethod
    def load(cls, filepath):
        """모델 로드"""
        data = joblib.load(filepath)
        trainer = cls(params=data['params'])
        trainer.model = data['model']
        trainer.threshold = data['threshold']
        return trainer

# 사용 예시
trainer = ExoplanetTrainer()
trainer.train(X_train, y_train, X_val, y_val)
trainer.optimize_threshold(X_val, y_val, target_recall=0.95)
trainer.save('final_model.joblib')

# 예측
y_pred = trainer.predict(X_test)
```

## 📝 요약

- **모델**: LightGBM (Gradient Boosted Trees)
- **교차 검증**: 10-fold StratifiedKFold
- **최적화**: 2단계 (AUC → Recall)
- **Early Stopping**: 과적합 방지
- **클래스 불균형**: 가중치 조정
- **저장**: joblib로 모델 저장

## 🤔 퀴즈로 확인하기

1. 왜 교차 검증을 사용하나요?
   <details>
   <summary>답 보기</summary>
   과적합을 방지하고 모델 성능을 더 신뢰성 있게 평가하기 위해
   </details>

2. Early Stopping이란?
   <details>
   <summary>답 보기</summary>
   검증 성능이 일정 기간 개선되지 않으면 학습을 중단하여 과적합 방지
   </details>

3. 임계값을 왜 조정하나요?
   <details>
   <summary>답 보기</summary>
   Recall을 최대화하여 행성을 최대한 많이 찾기 위해
   </details>

## 🚀 다음 단계

모델 학습을 완료했습니다!

다음은 **결과 분석** 방법을 알아보겠습니다.

👉 **[다음: 결과 분석](08_results.md)**

---

**도움이 필요하신가요?**
- [← 이전: 특징 추출](06_feature_extraction.md)
- [용어 사전](09_glossary.md)에서 모르는 용어를 찾아보세요
