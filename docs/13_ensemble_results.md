# 13. 앙상블 결과 분석 (Ensemble Results Analysis)

## 📊 전체 결과 요약

KOI 데이터셋에서 5가지 앙상블 알고리즘의 성능을 비교했습니다.

### 최종 성능표 (하이퍼파라미터 튜닝 후)

| 알고리즘 | Accuracy | Sensitivity | Specificity | Precision | F1 Score | 시간(초) |
|---------|----------|-------------|-------------|-----------|----------|---------|
| **Stacking** | **83.08%** | 80.05% | 85.93% | **83.23%** | **82.84%** | 10,856 |
| Adaboost | 82.52% | 79.45% | 85.03% | 82.86% | 82.43% | 1,627 |
| Random Forest | 82.64% | 76.64% | **85.72%** | 82.81% | 82.52% | 2,916 |
| Random Subspace | 81.91% | 78.39% | 85.12% | 81.98% | 81.78% | 1,312 |
| Extra Trees | 82.36% | 79.08% | 84.85% | 82.27% | 82.21% | **155** |

**주요 발견**:
- ✅ 모든 알고리즘이 **80% 이상** 달성
- ✅ **Stacking**이 전체 1위
- ✅ **Extra Trees**가 가장 빠름 (155초)
- ✅ 하이퍼파라미터 튜닝으로 평균 **1-2% 향상**

## 🔍 알고리즘별 상세 분석

### 1. Adaboost

#### 1차 구현 (초기값)

```python
# 초기 하이퍼파라미터
AdaBoostClassifier(
    n_estimators=50,      # 약한 학습기 개수
    learning_rate=1.0     # 학습률
)

# 결과
Accuracy:    81.37%
Sensitivity: 77.50%
Specificity: 84.84%
Precision:   81.95%
F1 Score:    81.23%
시간:         88초
```

**Confusion Matrix (1차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      599              107
실제: Confirmed      102              502

TP (True Positive):  502  ← 정확히 찾은 확인된 행성
TN (True Negative):  599  ← 정확히 걸러낸 후보
FP (False Positive): 107  ← 후보를 확인된 것으로 오판
FN (False Negative): 102  ← 확인된 행성을 놓침
```

#### 2차 구현 (튜닝 후)

```python
# Grid Search로 찾은 최적값
AdaBoostClassifier(
    n_estimators=974,     # 50 → 974 (19배 증가!)
    learning_rate=0.1     # 1.0 → 0.1 (10배 감소)
)

# 결과
Accuracy:    82.52% (+1.15%)  ← 향상!
Sensitivity: 79.45% (+1.95%)
Specificity: 85.03% (+0.19%)
Precision:   82.86% (+0.91%)
F1 Score:    82.43% (+1.20%)
시간:         1,627초 (18배 증가)
```

**Confusion Matrix (2차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      599              107
실제: Confirmed       88              516

개선사항:
- TP: 502 → 516 (+14개) ✓ 더 많은 행성 발견!
- FN: 102 → 88 (-14개)  ✓ 놓친 행성 감소!
```

**분석**:
```
👍 장점:
- 학습기 개수를 늘려 성능 향상
- 낮은 학습률로 안정적 학습

👎 단점:
- 학습 시간이 18배 증가 (88초 → 1,627초)
- 성능 향상은 1.15%로 제한적
```

---

### 2. Random Forest

#### 1차 구현 (초기값)

```python
# 초기 하이퍼파라미터
RandomForestClassifier(
    n_estimators=100,           # 트리 개수
    max_features='sqrt',        # 최대 변수 개수
    max_depth=None,             # 트리 깊이 제한 없음
    criterion='gini'            # 분할 기준
)

# 결과
Accuracy:    82.25%
Sensitivity: 79.45%
Specificity: 84.68%
Precision:   82.01%
F1 Score:    82.12%
시간:         176초
```

**Confusion Matrix (1차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      593              113
실제: Confirmed      106              514
```

#### 2차 구현 (튜닝 후)

```python
# 최적 하이퍼파라미터
RandomForestClassifier(
    n_estimators=1600,          # 100 → 1600 (16배!)
    max_features='sqrt',        # 유지
    max_depth=None,             # 유지
    criterion='entropy'         # gini → entropy
)

# 결과
Accuracy:    82.64% (+0.39%)
Sensitivity: 76.64% (-2.81%)  ← 감소!
Specificity: 85.72% (+1.04%)
Precision:   82.81% (+0.80%)
F1 Score:    82.52% (+0.40%)
시간:         2,916초 (16배 증가)
```

**Confusion Matrix (2차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      605              101
실제: Confirmed      120              518

변화:
- TP: 514 → 518 (+4개)
- TN: 593 → 605 (+12개)
- FN: 106 → 120 (+14개) ← 놓친 행성 증가!
```

**분석**:
```
🤔 흥미로운 결과:
- Accuracy는 소폭 향상
- Sensitivity는 오히려 감소
- Specificity는 향상

💡 트레이드오프:
- 후보를 더 정확히 걸러냄 (Specificity ↑)
- 하지만 확인된 행성을 일부 놓침 (Sensitivity ↓)

⚖️ 결론:
- 트리 개수를 늘리면 보수적 예측
- 외계행성 탐지에서는 Sensitivity가 중요!
```

---

### 3. Stacking (최고 성능!)

#### 1차 구현 (초기값)

```python
# 기본 구성
StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier()),
        ('gb', GradientBoostingClassifier())
    ],
    final_estimator=LogisticRegression()  # 메타-모델
)

# 결과
Accuracy:    82.72%
Sensitivity: 80.05%
Specificity: 85.21%
Precision:   82.89%
F1 Score:    82.71%
시간:         2,772초
```

**Confusion Matrix (1차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      599              107
실제: Confirmed      127              527
```

#### 2차 구현 (튜닝 후)

```python
# 최적 구성
StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(
            n_estimators=1600,
            criterion='entropy'
        )),
        ('gb', GradientBoostingClassifier(
            n_estimators=1600,
            learning_rate=0.1
        ))
    ],
    final_estimator=LogisticRegression()
)

# 결과
Accuracy:    83.03% (+0.31%)
Sensitivity: 80.05% (동일)
Specificity: 85.82% (+0.61%)
Precision:   83.10% (+0.21%)
F1 Score:    82.93% (+0.22%)
시간:         10,856초 (3.9배 증가)
```

#### 다양한 Estimator 조합 실험

```python
# 9가지 알고리즘 테스트
테스트한 알고리즘:
1. LGBM Classifier
2. Gradient Boosting       ← 최고 단일 성능 (82.53%)
3. Random Forest
4. XGBoost Classifier
5. Adaboost
6. Neural Network
7. K Nearest Neighbor
8. Decision Tree           ← 최저 성능
9. Naive Bayes

결과:
- 앙상블 > 비앙상블
- Gradient Boosting이 단일 알고리즘 중 최고
```

**5가지 Estimator 조합 비교**:

| 조합 | Estimators | Accuracy |
|------|-----------|----------|
| **1** | **LGBM + Gradient Boosting** | **83.08%** ✨ |
| 2 | 5개 앙상블 (RF + GB + LGBM + XGB + Ada) | 82.95% |
| 3 | RF + Adaboost | 82.87% |
| 4 | RF + Naive Bayes | 82.80% |
| 5 | 3개 비앙상블 (NN + KNN + DT) | 81.55% |

**최종 최적 구성**:
```python
# 최고 성능 조합
StackingClassifier(
    estimators=[
        ('lgbm', LGBMClassifier()),
        ('gb', GradientBoostingClassifier())
    ],
    final_estimator=LogisticRegression()
)

# 결과
Accuracy:    83.08% 🏆
Sensitivity: 80.05%
Specificity: 85.93%
Precision:   83.23%
F1 Score:    82.84%
```

**분석**:
```
🌟 Stacking의 강점:
1. 다양한 알고리즘의 장점 결합
2. 메타-모델이 최적 조합 학습
3. 가장 높은 전체 성능

💎 핵심 발견:
- 2개의 강력한 앙상블 조합이 최고
- 많은 알고리즘보다 강력한 소수가 효과적
- 비앙상블만 사용하면 성능 저하
```

---

### 4. Random Subspace Method

#### 1차 구현 (초기값)

```python
# 초기 하이퍼파라미터
BaggingClassifier(
    base_estimator=DecisionTree(),
    n_estimators=10,           # 학습기 개수
    max_samples=1.0,           # 샘플 비율
    max_features=1.0           # 특징 비율
)

# 결과
Accuracy:    80.55%
Sensitivity: 75.88%
Specificity: 84.84%
Precision:   80.93%
F1 Score:    80.32%
시간:         217초
```

**Confusion Matrix (1차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      602              104
실제: Confirmed      158              478
```

#### 2차 구현 (튜닝 후)

```python
# 최적 하이퍼파라미터
BaggingClassifier(
    base_estimator=DecisionTree(),
    n_estimators=1000,         # 10 → 1000 (100배!)
    max_samples=0.1,           # 1.0 → 0.1 (샘플 감소)
    max_features=1.0           # 유지
)

# 결과
Accuracy:    81.91% (+1.36%)  ← 큰 향상!
Sensitivity: 78.39% (+2.51%)
Specificity: 85.12% (+0.28%)
Precision:   81.98% (+1.05%)
F1 Score:    81.78% (+1.46%)
시간:         1,312초 (6배 증가)
```

**Confusion Matrix (2차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      597              109
실제: Confirmed      129              507

개선사항:
- TP: 478 → 507 (+29개) ✓ 큰 향상!
- FN: 158 → 129 (-29개) ✓ 놓친 행성 대폭 감소!
- TN: 602 → 597 (-5개)  약간 감소
```

#### 다양한 Estimator 실험

```python
# 5가지 Base Estimator 테스트
테스트:
1. Random Forest
2. Adaboost
3. Gradient Boosting
4. Logistic Regression
5. Stacking

결과:
```

| Base Estimator | Accuracy | Sensitivity | Specificity | Precision | F1 |
|---------------|----------|-------------|-------------|-----------|-----|
| **Random Forest** | **81.88%** | **79.35%** | 84.19% | 82.47% | **81.25%** |
| Gradient Boosting | 81.65% | 78.45% | 84.61% | **83.71%** | 80.96% |
| Logistic Regression | 81.43% | 77.55% | **85.93%** | 83.05% | 80.18% |
| Adaboost | 81.32% | 77.10% | 85.21% | 82.73% | 79.80% |
| Stacking | 81.10% | 76.78% | 85.43% | 82.95% | 79.73% |

**분석**:
```
🎯 최적 조합:
Random Forest as Base Estimator

💡 발견:
- 단순한 Bagging보다 Random Subspace가 효과적
- 낮은 샘플 비율(0.1)이 더 좋은 결과
- 많은 Estimator(1000개)가 성능 향상

⚡ 장점:
- 적은 샘플로 빠른 학습
- 과적합 방지
```

---

### 5. Extremely Randomized Trees (Extra Trees)

#### 1차 구현 (초기값)

```python
# 초기 하이퍼파라미터
ExtraTreesClassifier(
    n_estimators=100,
    max_features='sqrt',
    max_depth=None,
    criterion='gini'
)

# 결과
Accuracy:    82.06%
Sensitivity: 78.91%
Specificity: 84.84%
Precision:   82.01%
F1 Score:    81.92%
시간:         67초  ← 매우 빠름!
```

**Confusion Matrix (1차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      596              110
실제: Confirmed      137              510
```

#### 2차 구현 (튜닝 후)

```python
# 최적 하이퍼파라미터
ExtraTreesClassifier(
    n_estimators=200,          # 100 → 200
    max_features='sqrt',       # 유지
    max_depth=None,            # 유지
    criterion='entropy'        # gini → entropy
)

# 결과
Accuracy:    82.36% (+0.30%)
Sensitivity: 79.08% (+0.17%)
Specificity: 84.85% (+0.01%)
Precision:   82.27% (+0.26%)
F1 Score:    82.21% (+0.29%)
시간:         155초 (2.3배 증가)
```

**Confusion Matrix (2차)**:
```
              예측: Candidate   예측: Confirmed
실제: Candidate      600              106
실제: Confirmed      133              515

변화:
- TP: 510 → 515 (+5개)
- TN: 596 → 600 (+4개)
- FN: 137 → 133 (-4개)
- FP: 110 → 106 (-4개)

모든 지표가 소폭 개선!
```

**분석**:
```
⚡ Extra Trees의 특징:
1. 가장 빠른 학습 시간 (67초 → 155초)
2. Random Forest보다 더 랜덤
3. 과적합 방지 효과

🤔 성능 개선이 작은 이유:
- 이미 충분히 랜덤 → 튜닝 효과 제한적
- 무작위성이 성능 향상의 상한선

👍 언제 사용?
- 빠른 프로토타이핑
- 리소스 제한적 환경
- 실시간 예측 필요
```

---

## 📈 성능 메트릭 깊이 이해

### Accuracy (정확도)

```
정의: 전체 예측 중 맞춘 비율

공식: (TP + TN) / (TP + TN + FP + FN)

예시 (Stacking):
(529 + 605) / (529 + 605 + 101 + 127) = 83.08%

의미:
✓ 100개 예측 중 83개 정확
✗ 17개는 틀림
```

### Sensitivity (민감도) = Recall

```
정의: 실제 양성 중 맞춘 비율

공식: TP / (TP + FN)

예시 (Stacking):
529 / (529 + 127) = 80.05%

의미:
✓ 확인된 행성 100개 중 80개 발견
✗ 20개는 놓침

외계행성 탐지에서 가장 중요!
→ 행성을 놓치면 안 됨
```

### Specificity (특이도)

```
정의: 실제 음성 중 맞춘 비율

공식: TN / (TN + FP)

예시 (Stacking):
605 / (605 + 101) = 85.93%

의미:
✓ 후보 100개 중 86개 정확히 걸러냄
✗ 14개를 확인된 것으로 오판

오탐이 많으면 전문가 검토 시간 낭비
```

### Precision (정밀도)

```
정의: 양성 예측 중 맞춘 비율

공식: TP / (TP + FP)

예시 (Stacking):
529 / (529 + 101) = 83.23%

의미:
✓ 확인된 행성이라 예측한 100개 중 83개 정답
✗ 17개는 실제로 후보

Precision vs Recall 트레이드오프!
```

### F1 Score

```
정의: Precision과 Recall의 조화 평균

공식: 2 × (Precision × Recall) / (Precision + Recall)

예시 (Stacking):
2 × (83.23% × 80.05%) / (83.23% + 80.05%) = 82.84%

의미:
균형잡힌 성능 지표
- 둘 다 높아야 F1이 높음
- 하나만 높으면 F1은 중간값
```

## ⏱️ 학습 시간 비교

### 알고리즘별 시간 분석

```
Extra Trees:         155초   ★★★★★ (가장 빠름!)
Random Subspace:   1,312초   ★★★☆☆
Adaboost:          1,627초   ★★☆☆☆
Random Forest:     2,916초   ★☆☆☆☆
Stacking:         10,856초   ☆☆☆☆☆ (가장 느림)

성능 대비 시간:
Extra Trees:    82.36% / 155초  = 0.53% per 초
Random Subspace: 81.91% / 1,312초 = 0.06% per 초
Adaboost:       82.52% / 1,627초 = 0.05% per 초
Random Forest:  82.64% / 2,916초 = 0.03% per 초
Stacking:       83.08% / 10,856초 = 0.01% per 초

결론:
Extra Trees가 시간 대비 가장 효율적!
```

### 하이퍼파라미터 튜닝 vs 시간

```
튜닝 전후 시간 증가:

Adaboost:      88초 →  1,627초 (18배 ↑)
Random Forest: 176초 →  2,916초 (16배 ↑)
Stacking:    2,772초 → 10,856초 (3.9배 ↑)
Random Subspace: 217초 → 1,312초 (6배 ↑)
Extra Trees:   67초 →    155초 (2.3배 ↑)

성능 향상:

Adaboost:      +1.15%
Random Forest: +0.39%
Stacking:      +0.31%
Random Subspace: +1.36%
Extra Trees:   +0.30%

효율성 순위:
1. Random Subspace: 6배 시간 → 1.36% 향상
2. Extra Trees: 2.3배 시간 → 0.30% 향상
3. Adaboost: 18배 시간 → 1.15% 향상
```

## 🎯 실용적 적용 가이드

### 상황별 알고리즘 선택

```
1. 최고 성능이 필요할 때
   → Stacking (83.08%)
   단점: 가장 느림 (10,856초)
   용도: 최종 분석, 논문 발표

2. 빠른 프로토타이핑
   → Extra Trees (155초)
   성능: 82.36% (충분히 높음)
   용도: 빠른 실험, 초기 탐색

3. 균형잡힌 선택
   → Random Subspace (1,312초)
   성능: 81.91%
   용도: 일반적 사용

4. 해석 가능성 중요
   → Random Forest (2,916초)
   성능: 82.64%
   용도: 특징 중요도 분석

5. 클래스 불균형 데이터
   → Adaboost (1,627초)
   성능: 82.52%
   용도: 불균형한 데이터셋
```

### 실전 파이프라인

```python
# 단계별 접근법

# 1단계: 빠른 탐색 (Extra Trees)
model_fast = ExtraTreesClassifier(n_estimators=100)
model_fast.fit(X_train, y_train)
print(f"빠른 평가: {model_fast.score(X_test, y_test):.2%}")

# 2단계: 중간 성능 (Random Forest)
model_mid = RandomForestClassifier(n_estimators=200)
model_mid.fit(X_train, y_train)
print(f"중간 평가: {model_mid.score(X_test, y_test):.2%}")

# 3단계: 최고 성능 (Stacking)
model_best = StackingClassifier(
    estimators=[
        ('lgbm', LGBMClassifier()),
        ('gb', GradientBoostingClassifier())
    ],
    final_estimator=LogisticRegression()
)
model_best.fit(X_train, y_train)
print(f"최고 평가: {model_best.score(X_test, y_test):.2%}")

# 4단계: 앙상블의 앙상블 (Voting)
from sklearn.ensemble import VotingClassifier

ensemble_of_ensembles = VotingClassifier(
    estimators=[
        ('et', model_fast),
        ('rf', model_mid),
        ('stacking', model_best)
    ],
    voting='soft'  # 확률 기반 투표
)
ensemble_of_ensembles.fit(X_train, y_train)
print(f"최종: {ensemble_of_ensembles.score(X_test, y_test):.2%}")
```

## 🔬 하이퍼파라미터 튜닝 전략

### Grid Search 사용법

```python
from sklearn.model_selection import GridSearchCV

# 탐색할 파라미터 공간
param_grid = {
    'n_estimators': [50, 100, 200, 500, 1000, 1600],
    'learning_rate': [0.01, 0.05, 0.1, 0.2, 0.5, 1.0],
    'max_depth': [3, 5, 7, 10, None]
}

# Grid Search 실행
grid_search = GridSearchCV(
    estimator=AdaBoostClassifier(),
    param_grid=param_grid,
    cv=10,                    # 10-fold CV
    scoring='accuracy',
    n_jobs=-1,               # 모든 CPU 사용
    verbose=2
)

# 학습
grid_search.fit(X_train, y_train)

# 최적 파라미터
print("최적 파라미터:", grid_search.best_params_)
print("최적 점수:", grid_search.best_score_)

# 상위 5개 조합
results = pd.DataFrame(grid_search.cv_results_)
top_5 = results.nlargest(5, 'mean_test_score')[
    ['params', 'mean_test_score', 'std_test_score']
]
print(top_5)
```

### 효율적 튜닝 전략

```python
# 1단계: 넓은 범위로 빠른 탐색
coarse_param_grid = {
    'n_estimators': [50, 200, 500, 1000],
    'learning_rate': [0.01, 0.1, 1.0]
}

# 2단계: 좁은 범위로 세밀한 탐색
fine_param_grid = {
    'n_estimators': [800, 900, 1000, 1100, 1200],
    'learning_rate': [0.08, 0.09, 0.1, 0.11, 0.12]
}

# 3단계: Random Search (더 빠름)
from sklearn.model_selection import RandomizedSearchCV

random_search = RandomizedSearchCV(
    estimator=AdaBoostClassifier(),
    param_distributions=param_grid,
    n_iter=100,              # 100번만 시도
    cv=10,
    random_state=42,
    n_jobs=-1
)
```

## 📊 Confusion Matrix 시각화

```python
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# 5개 알고리즘 비교
algorithms = {
    'Stacking': model_stacking,
    'Adaboost': model_adaboost,
    'Random Forest': model_rf,
    'Random Subspace': model_rs,
    'Extra Trees': model_et
}

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

for idx, (name, model) in enumerate(algorithms.items()):
    # 예측
    y_pred = model.predict(X_test)

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)

    # 시각화
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
    axes[idx].set_title(f'{name}\nAccuracy: {model.score(X_test, y_test):.2%}')
    axes[idx].set_xlabel('Predicted')
    axes[idx].set_ylabel('Actual')

plt.tight_layout()
plt.show()
```

## 💡 핵심 발견사항

### 1. 앙상블의 강력함

```
전통적 ML vs 앙상블:
Decision Tree 단독: ~75% accuracy
Random Forest:       82.64% accuracy
Stacking:            83.08% accuracy

결론: 앙상블이 7-8% 더 높음!
```

### 2. 하이퍼파라미터 튜닝의 중요성

```
평균 향상:
- Adaboost:      +1.15%
- Random Forest: +0.39%
- Stacking:      +0.31%
- Random Subspace: +1.36%
- Extra Trees:   +0.30%

결론: 1-2% 향상은 작아 보여도
      실제로는 수십 개의 행성 차이!
```

### 3. 시간 vs 성능 트레이드오프

```
Pareto 최적:
- Extra Trees: 82.36% / 155초
- Stacking:    83.08% / 10,856초

0.72% 성능 향상을 위해
70배의 시간 필요!

선택:
연구용 → Stacking
실전용 → Extra Trees
```

### 4. Stacking의 우월함

```
Stacking이 최고인 이유:
1. 다양한 알고리즘 결합
2. 메타-모델의 최적화
3. 각 알고리즘의 장점 활용

증명:
LGBM + Gradient Boosting 조합이
5개 앙상블 조합보다 우수
→ 품질 > 양
```

## 🚀 미래 연구 방향

### 1. 다른 데이터셋 적용

```
KOI 이외의 데이터셋:
- TESS (짧은 관측 기간)
- K2 (다양한 캠페인)
- CoRoT (유럽 망원경)

연구 질문:
앙상블 성능이 데이터셋에 따라 달라지나?
```

### 2. 딥러닝과 비교

```
현재:
앙상블 (고전 ML): 83.08%

비교 대상:
CNN + LSTM (딥러닝): ?%

질문:
- 어떤 상황에서 앙상블이 유리한가?
- 딥러닝과 앙상블을 결합하면?
```

### 3. 해석 가능성 향상

```
블랙박스 문제:
앙상블은 왜 이렇게 예측했을까?

해결책:
- SHAP (SHapley Additive exPlanations)
- LIME (Local Interpretable Model-agnostic Explanations)
- 특징 중요도 분석

목표:
천문학자가 신뢰할 수 있는 설명 제공
```

### 4. 온라인 학습

```
현재 문제:
새로운 데이터마다 전체 재학습

해결책:
- Incremental Learning
- Online Ensemble
- Transfer Learning

장점:
실시간 외계행성 탐지 시스템
```

## 📝 최종 요약

### 핵심 결론

**1. 모든 앙상블 알고리즘이 우수 (80% 이상)**
```
최고: Stacking        83.08%
최저: Random Subspace 81.91%
범위: 1.17% 차이 (매우 작음!)
```

**2. Stacking이 전체 1위**
```
Accuracy:  83.08%
Precision: 83.23%
F1 Score:  82.84%

이유: 다양한 알고리즘의 장점 결합
```

**3. Extra Trees가 가장 효율적**
```
시간: 155초 (가장 빠름)
성능: 82.36% (충분히 높음)

추천: 빠른 프로토타이핑
```

**4. 하이퍼파라미터 튜닝 필수**
```
평균 향상: 1-2%
중요도: 매우 높음

예시: Adaboost
튜닝 전: 81.37%
튜닝 후: 82.52% (+1.15%)
```

**5. KOI 데이터셋에 매우 적합**
```
클래스 균형: 50:50
신호 품질: 높음
결과: 안정적 성능
```

### 실전 권장사항

```
1. 프로젝트 시작
   → Extra Trees로 빠른 베이스라인

2. 성능 개선
   → Random Forest로 중간 단계

3. 최종 모델
   → Stacking으로 최고 성능

4. 배포
   → 시간 제약에 따라 선택
   - 빠름: Extra Trees
   - 정확: Stacking
```

## 🤔 퀴즈로 확인하기

1. 5개 알고리즘 중 최고 성능은?
   <details>
   <summary>답 보기</summary>
   Stacking (83.08% accuracy)
   </details>

2. 가장 빠른 알고리즘은?
   <details>
   <summary>답 보기</summary>
   Extra Trees (155초)
   </details>

3. 하이퍼파라미터 튜닝의 효과는?
   <details>
   <summary>답 보기</summary>
   평균 1-2% 성능 향상 (매우 중요!)
   </details>

4. Sensitivity가 중요한 이유는?
   <details>
   <summary>답 보기</summary>
   외계행성을 놓치지 않기 위해 (행성 탐지가 최우선)
   </details>

---

**축하합니다! 모든 문서 학습을 완료했습니다!** 🎉

이제 여러분은:
- ✅ 외계행성 탐지의 원리 이해
- ✅ 머신러닝과 앙상블의 개념 파악
- ✅ KOI 데이터셋 전처리 방법 숙지
- ✅ 5가지 앙상블 알고리즘 비교 분석
- ✅ 실전 적용 가능한 지식 습득

**다음 단계**:
1. 실제 코드 작성해보기
2. 다른 데이터셋 실험하기
3. 딥러닝과 비교해보기
4. 자신만의 프로젝트 시작하기

👉 **[README로 돌아가기](README.md)**
👉 **[참고 자료](10_references.md)**
👉 **[용어 사전](09_glossary.md)**

**Good luck with your exoplanet detection journey! 🌟🪐🔭**
