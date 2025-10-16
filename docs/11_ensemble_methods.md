# 11. 앙상블 방법 (Ensemble Methods)

## 🎯 앙상블이란?

**앙상블(Ensemble)**은 여러 개의 머신러닝 모델을 결합하여 더 강력한 예측을 만드는 기법입니다.

### 일상생활 비유

```
혼자 결정:
당신 혼자 영화를 선택 → 실패 확률 높음

친구들과 함께:
친구 5명과 투표로 영화 선택 → 더 좋은 선택!

앙상블도 같은 원리:
여러 모델의 예측을 결합 → 더 정확한 결과!
```

## 📊 앙상블의 핵심 개념

### 기본 원리

```
단일 모델:
모델 A → 예측: 행성 (정확도 80%)

앙상블:
모델 A → 행성 (80%)  ┐
모델 B → 행성 (82%)  ├→ 투표 → 행성 (정확도 90%!)
모델 C → 행성 (85%)  ┘
```

**핵심**:
- 하나의 모델이 틀려도 다른 모델이 보완
- 여러 모델의 "집단 지성" 활용

## 🌟 왜 앙상블이 강력한가?

### 1. 편향-분산 트레이드오프

```
단일 모델의 문제:
- 너무 단순 → 편향 높음 (Underfitting)
- 너무 복잡 → 분산 높음 (Overfitting)

앙상블의 해결:
여러 모델을 결합 → 편향과 분산 동시에 감소!
```

### 2. 다양성의 힘

```
모델 다양성:
모델 A: 특징 1, 2, 3 사용
모델 B: 특징 2, 4, 5 사용
모델 C: 특징 1, 4, 6 사용

결과:
각 모델이 다른 패턴 학습 → 종합 판단력 향상!
```

## 🔧 앙상블의 3가지 주요 방법

### 1. Bagging (Bootstrap Aggregating)

**원리**: 데이터를 여러 번 샘플링하여 각각 모델 학습

```
원본 데이터 [1,2,3,4,5,6,7,8,9,10]
          ↓ 부트스트랩 샘플링
샘플 1: [1,3,3,5,7,9,9,10]  → 모델 A
샘플 2: [2,2,4,6,6,8,10,10] → 모델 B
샘플 3: [1,2,4,5,7,8,9,10]  → 모델 C
          ↓
        평균/투표
          ↓
       최종 예측
```

**대표 알고리즘**: Random Forest

**장점**:
- 과적합 감소
- 병렬 처리 가능 (빠름)
- 안정적인 성능

### 2. Boosting

**원리**: 이전 모델의 실수를 다음 모델이 보완

```
1단계: 모델 A 학습
     ✓ 80개 맞춤
     ✗ 20개 틀림

2단계: 틀린 20개에 가중치 부여
     모델 B 학습 (틀린 것에 집중)
     ✓ 85개 맞춤
     ✗ 15개 틀림

3단계: 틀린 15개에 가중치 부여
     모델 C 학습
     ✓ 90개 맞춤
     ✗ 10개 틀림

최종: A + B + C 결합 → 95개 맞춤!
```

**대표 알고리즘**: Adaboost, XGBoost

**장점**:
- 높은 정확도
- 약한 학습기도 강력하게 만듦

**단점**:
- 순차적 (느림)
- 과적합 위험

### 3. Stacking

**원리**: 다양한 모델의 예측을 메타-모델이 학습

```
레벨 0 (기본 모델):
모델 A → 예측 1  ┐
모델 B → 예측 2  ├→ [예측1, 예측2, 예측3]
모델 C → 예측 3  ┘
       ↓
레벨 1 (메타-모델):
메타 모델 → 최종 예측
```

**장점**:
- 여러 알고리즘의 장점 결합
- 매우 높은 성능 가능

**단점**:
- 복잡함
- 계산 비용 높음

## 📚 5가지 앙상블 알고리즘 상세

### 1. Adaboost (Adaptive Boosting)

**특징**: 가장 유명한 부스팅 알고리즘

```python
from sklearn.ensemble import AdaBoostClassifier

model = AdaBoostClassifier(
    n_estimators=50,      # 약한 학습기 개수
    learning_rate=1.0     # 학습률
)

model.fit(X_train, y_train)
```

**작동 방식**:
```
1. 모든 데이터에 동일한 가중치 부여
2. 첫 번째 모델 학습
3. 틀린 데이터의 가중치 증가
4. 다음 모델은 틀린 데이터에 집중
5. 반복...
```

**외계행성 탐지 결과** (2024년 논문):
- Accuracy: 81.37% → 88.57% (튜닝 후)
- Precision: 82.12% → 89.09%
- 학습 시간: 88초

### 2. Random Forest

**특징**: 가장 인기 있는 앙상블 알고리즘

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,     # 트리 개수
    max_depth=10,         # 트리 깊이
    min_samples_split=2   # 분할 최소 샘플 수
)

model.fit(X_train, y_train)
```

**작동 방식**:
```
데이터 샘플링 + 특징 샘플링

트리 1: 데이터 [A] + 특징 [1,3,5] → 예측
트리 2: 데이터 [B] + 특징 [2,4,6] → 예측
트리 3: 데이터 [C] + 특징 [1,4,7] → 예측
...
트리 100: 데이터 [Z] + 특징 [2,5,8] → 예측
            ↓
         다수결 투표
```

**외계행성 탐지 결과**:
- Accuracy: 86.73% → 88.13%
- Precision: 89.51% → 87.33%
- 학습 시간: 9초 (매우 빠름!)

### 3. Stacking (Stacked Generalization)

**특징**: 메타-학습으로 최고 성능

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# 기본 모델들
estimators = [
    ('dt', DecisionTreeClassifier()),
    ('svm', SVC()),
    ('rf', RandomForestClassifier())
]

# Stacking
model = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression()  # 메타-모델
)

model.fit(X_train, y_train)
```

**작동 방식**:
```
레벨 0 (다양한 알고리즘):
Decision Tree     → [0.8, 0.2]  ┐
SVM              → [0.7, 0.3]  ├→ 새로운 특징
Random Forest    → [0.9, 0.1]  ┘
                      ↓
레벨 1 (메타-모델):
Logistic Regression
    ↓
[0.85, 0.15] → 클래스 0 (행성!)
```

**외계행성 탐지 결과**:
- **Accuracy: 88.87% (최고!)**
- **Precision: 89.63% (최고!)**
- **F1 Score: 88.87% (최고!)**
- 학습 시간: 15초

### 4. Random Subspace Method

**특징**: 특징 공간을 랜덤하게 샘플링

```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

model = BaggingClassifier(
    DecisionTreeClassifier(),
    max_features=0.5,     # 50% 특징만 사용
    n_estimators=10
)

model.fit(X_train, y_train)
```

**작동 방식**:
```
전체 특징: [1,2,3,4,5,6,7,8,9,10]
              ↓ 랜덤 샘플링
모델 A: [1,3,5,7,9]      → 예측
모델 B: [2,4,6,8,10]     → 예측
모델 C: [1,4,7,9,10]     → 예측
              ↓
           투표
```

**외계행성 탐지 결과**:
- Accuracy: 85.60% → 88.28%
- Precision: 84.03% → 87.76%
- 학습 시간: 5초

### 5. Extremely Randomized Trees (Extra Trees)

**특징**: Random Forest보다 더 랜덤!

```python
from sklearn.ensemble import ExtraTreesClassifier

model = ExtraTreesClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=2
)

model.fit(X_train, y_train)
```

**Random Forest와의 차이**:
```
Random Forest:
- 데이터 부트스트랩 샘플링 O
- 최적의 분할점 찾기 ✓

Extra Trees:
- 데이터 샘플링 X (전체 사용)
- 랜덤한 분할점 사용! ⚡
```

**장점**:
- Random Forest보다 더 빠름
- 더 강한 랜덤성 → 과적합 방지

**외계행성 탐지 결과**:
- Accuracy: 86.06% → 87.84%
- Precision: 86.68% → 87.84%
- 학습 시간: 7초

## 📊 성능 비교 (2024년 논문 결과)

### 하이퍼파라미터 튜닝 후

| 알고리즘 | Accuracy | Precision | Recall | F1 Score | 시간(초) |
|---------|----------|-----------|--------|----------|---------|
| **Stacking** | **88.87%** | **89.63%** | 88.11% | **88.87%** | 15 |
| Adaboost | 88.57% | 89.09% | 88.04% | 88.56% | 88 |
| Random Forest | 88.13% | 87.33% | **89.02%** | 88.16% | **9** |
| Random Subspace | 88.28% | 87.76% | 88.85% | 88.30% | **5** |
| Extra Trees | 87.84% | 87.84% | 87.84% | 87.84% | 7 |

### 주요 발견

1. **Stacking이 전체적으로 최고 성능**
   - 다양한 알고리즘의 장점 결합

2. **Random Subspace가 가장 빠름**
   - 5초만에 88.28% 정확도

3. **모든 알고리즘이 80% 이상**
   - 앙상블의 강력함 입증

4. **하이퍼파라미터 튜닝의 중요성**
   - 평균 5-7% 성능 향상

## 🎛️ 하이퍼파라미터 튜닝

### Grid Search 사용

```python
from sklearn.model_selection import GridSearchCV

# 탐색할 파라미터 공간
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

# Grid Search
grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=10,          # 10-fold CV
    scoring='accuracy'
)

grid_search.fit(X_train, y_train)

# 최적 파라미터
best_params = grid_search.best_params_
print(f"최적 파라미터: {best_params}")
```

### 튜닝의 효과

```
Adaboost 예시:

튜닝 전:
- n_estimators: 50
- learning_rate: 1.0
→ Accuracy: 81.37%

튜닝 후:
- n_estimators: 100
- learning_rate: 0.5
→ Accuracy: 88.57% (+7.2%!)
```

## 💡 언제 어떤 앙상블을 사용할까?

### 선택 가이드

```
높은 정확도가 최우선?
→ Stacking (하지만 느림)

빠른 학습이 필요?
→ Random Subspace or Random Forest

해석 가능성 중요?
→ Random Forest (특징 중요도 쉽게 확인)

불균형 데이터?
→ Adaboost (가중치 조정 자동)

범용적 사용?
→ Random Forest (대부분 잘 작동)
```

## 📝 요약

- **앙상블**: 여러 모델을 결합하여 성능 향상
- **3가지 방법**: Bagging, Boosting, Stacking
- **5가지 알고리즘**: Adaboost, Random Forest, Stacking, Random Subspace, Extra Trees
- **최고 성능**: Stacking (88.87%)
- **가장 빠름**: Random Subspace (5초)
- **가장 인기**: Random Forest (범용성)

## 🤔 퀴즈로 확인하기

1. 앙상블의 핵심 원리는?
   <details>
   <summary>답 보기</summary>
   여러 모델의 예측을 결합하여 단일 모델보다 높은 성능 달성
   </details>

2. Bagging과 Boosting의 차이는?
   <details>
   <summary>답 보기</summary>
   Bagging: 병렬로 독립적 학습<br>
   Boosting: 순차적으로 이전 실수 보완
   </details>

3. 외계행성 탐지에서 최고 성능은?
   <details>
   <summary>답 보기</summary>
   Stacking (88.87% 정확도)
   </details>

## 🚀 다음 단계

앙상블 방법을 이해했습니다!

다음은 **KOI 데이터셋**에 대해 알아보겠습니다.

👉 **[다음: KOI 데이터셋](12_koi_dataset.md)**

---

**참고 자료**:
- 원본 논문: "Assessment of Ensemble-Based Machine Learning Algorithms for Exoplanet Identification" (Electronics, 2024)
- [← 이전: 참고 자료](10_references.md)
- [용어 사전](09_glossary.md)
