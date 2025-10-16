# 4. 연구 방법론 개요

## 🎯 전체 워크플로우

이 연구는 **3단계 파이프라인**으로 구성됩니다:

```
┌─────────────────────────────────────────────────────────┐
│                    전체 프로세스                          │
└─────────────────────────────────────────────────────────┘

[1단계] 데이터 처리
    원시 광도 곡선
         ↓
    노이즈 제거
         ↓
    정규화 및 리샘플링
         ↓
    깨끗한 광도 곡선

[2단계] 특징 추출
    깨끗한 광도 곡선
         ↓
    tsfresh로 분석
         ↓
    789개 특징 추출
         ↓
    특징 배열 (Feature Array)

[3단계] 모델 학습
    특징 배열 + 레이블
         ↓
    Gradient Boosted Trees
         ↓
    10-fold 교차 검증
         ↓
    행성 탐지 모델
```

## 📊 사용된 데이터셋

### 1. K2 시뮬레이션 데이터 (개념 검증)

```python
데이터 소스:   K2 Campaign 7 실제 데이터
처리 방법:     인공 트랜짓 신호 주입
총 광도 곡선:  7,873개
  - 행성 있음:   3,937개 (50%)
  - 행성 없음:   3,936개 (50%)

분할:
  - 학습/검증:   7,086개 (90%)
  - 테스트:      787개 (10%)

목적:          방법의 유효성 검증
```

### 2. Kepler 실제 데이터

```python
데이터 소스:   Kepler 우주 망원경
관측 기간:     2009-2018 (약 4년간)
총 광도 곡선:  15,737개
  - 행성 후보:   3,600개 (23%)
  - 비행성:      12,137개 (77%)

데이터 길이:   ~70,000 데이터 포인트/곡선
샘플링 간격:   29.4분

분할:
  - 학습 세트:   12,590개 (80%)
  - 검증 세트:   1,574개 (10%)
  - 테스트 세트: 1,573개 (10%)

레이블 출처:   Autovetter Planet Candidate Catalog
```

### 3. TESS 실제 데이터

```python
데이터 소스:   TESS 우주 망원경
관측 기간:     2018-현재
총 광도 곡선:  16,500개
  - 행성 후보:   492개 (3%)     ← 심한 불균형!
  - 식쌍성:      2,154개 (13%)
  - 잡음:        13,854개 (84%)

관측 기간:     27일/섹터 (짧음!)
데이터 특징:   Kepler보다 30-100배 밝은 별

분할:
  - 학습 세트:   13,200개 (80%)
  - 검증 세트:   1,650개 (10%)
  - 테스트 세트: 1,650개 (10%)

처리 방법:     MIT Quick Look Pipeline (QLP)
```

## 🔬 연구의 3단계 상세

### 1단계: 데이터 처리 및 레이블링

#### 목적
원시 광도 곡선을 머신러닝에 적합한 형태로 변환

#### 주요 작업

```python
1. 우주선 충돌 제거 (Cosmic Ray Removal)
   if point > 5σ above neighbors:
       remove point

2. 별 변동성 제거 (Stellar Variability Removal)
   - 스플라인 피팅
   - 저주파 성분 제거
   - 반복적 적용 (수렴까지)

3. 데이터 갭 보간 (Gap Interpolation)
   - K2는 관측 갭이 있음
   - 선형 보간으로 메움

4. 균일한 리샘플링 (Uniform Resampling)
   - 1시간 간격으로 리샘플링
   - tsfresh 특징 추출을 위해 필요

5. 레이블링 (Labeling)
   - 클래스 1: 행성 후보
   - 클래스 0: 비행성
```

### 2단계: 특징 추출

#### 사용 도구: tsfresh

```python
from tsfresh import extract_features

# 시계열 특징 자동 추출
features = extract_features(
    light_curve,
    default_fc_parameters=EfficientFCParameters()
)

# 결과: 789개의 특징!
```

#### 추출되는 특징 유형

```
📈 통계적 특징 (Statistical Features)
  - 평균 (Mean)
  - 표준편차 (Standard Deviation)
  - 왜도 (Skewness)
  - 첨도 (Kurtosis)
  - 최소/최대값
  - 사분위수 (Quantiles)

🌊 주파수 영역 특징 (Frequency Domain)
  - FFT 계수 (Fourier Coefficients)
  - 파워 스펙트럼
  - 주요 주파수

📊 시계열 특징 (Time Series)
  - 자기상관 (Autocorrelation)
  - 평균보다 큰 값의 개수
  - 절대 에너지 (Absolute Energy)
  - 변화율 (Change Rate)

🔍 복잡도 측정 (Complexity)
  - 엔트로피
  - 근사 엔트로피
  - 샘플 엔트로피
```

#### 특징 전처리

```python
1. 불필요한 특징 제거
   - 상수 값 특징 제거

2. 결측치 처리
   - 보간법으로 채움

3. 스케일링 (Robust Scaler)
   - 특징 값 범위 정규화
   - 이상치에 강건
```

### 3단계: 모델 학습

#### 사용 모델: LightGBM (Gradient Boosted Trees)

```python
import lightgbm as lgb

# 모델 설정
model = lgb.LGBMClassifier(
    objective='binary',        # 이진 분류
    n_estimators=100,          # 트리 100개
    max_depth=5,               # 최대 깊이
    learning_rate=0.1,         # 학습률
    num_leaves=31,             # 리프 노드 수
    min_child_samples=20       # 최소 샘플 수
)

# 10-fold 교차 검증으로 학습
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=10, shuffle=True)
for train_idx, val_idx in cv.split(X, y):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    model.fit(X_train, y_train)
    score = model.score(X_val, y_val)
```

## 📏 성능 평가 지표

### 1. AUC (Area Under the Curve)

```
ROC 곡선:
진짜양성률 ↑
        1.0│        ╱━━━━━━
           │       ╱
           │      ╱
        0.5│     ╱
           │    ╱
           │   ╱
        0.0└──────────────→ 거짓양성률
           0.0    0.5    1.0

AUC = 곡선 아래 면적
- 1.0 = 완벽
- 0.9+ = 우수
- 0.8+ = 좋음
- 0.5 = 랜덤 추측
```

### 2. Recall (재현율) - 가장 중요!

```
Recall = 실제 행성 중 찾은 것 / 실제 행성 전체

예시:
실제 행성 100개 중 96개 찾음
→ Recall = 96/100 = 0.96 (96%)

목표: 가능한 많은 행성 찾기!
```

### 3. Precision (정밀도)

```
Precision = 행성으로 예측한 것 중 실제 행성 / 행성으로 예측한 것 전체

예시:
행성이라고 예측한 120개 중 96개가 진짜
→ Precision = 96/120 = 0.80 (80%)

목표: 오탐을 줄이기
```

### 4. Accuracy (정확도)

```
Accuracy = 맞게 예측한 것 / 전체

예시:
1000개 중 940개 맞춤
→ Accuracy = 940/1000 = 0.94 (94%)

주의: 불균형 데이터에서는 의미 없음!
```

### 지표 간의 트레이드오프

```
높은 Recall ↔ 낮은 Precision

┌─────────────┬──────────┬───────────┐
│ 임계값      │ Recall   │ Precision │
├─────────────┼──────────┼───────────┤
│ 0.1 (낮음)  │ 0.98 ↑   │ 0.70 ↓    │
│ 0.5 (기본)  │ 0.90     │ 0.85      │
│ 0.9 (높음)  │ 0.75 ↓   │ 0.95 ↑    │
└─────────────┴──────────┴───────────┘
```

## 🎛️ 하이퍼파라미터 최적화

### 2단계 최적화 과정

```python
# 1단계: AUC 최대화 (임계값 제외)
best_auc = 0
for n_trees in [50, 100, 200]:
    for depth in [3, 5, 7, 10]:
        for lr in [0.01, 0.05, 0.1]:
            model = train(n_trees, depth, lr)
            auc = evaluate_auc(model)
            if auc > best_auc:
                best_params = (n_trees, depth, lr)
                best_auc = auc

# 2단계: Recall 최대화 (임계값 조정)
best_recall = 0
for threshold in [0.1, 0.2, ..., 0.9]:
    recall, precision = evaluate(model, threshold)
    if recall > best_recall and precision > 0.8:
        best_threshold = threshold
        best_recall = recall
```

## 📋 실험 설계

### 각 데이터셋별 실험

| 데이터셋 | 목적 | 난이도 |
|---------|------|--------|
| **K2 시뮬레이션** | 개념 검증 | 쉬움 |
| **Kepler 실제** | 성능 평가 | 중간 |
| **TESS 실제** | 실용성 테스트 | 어려움 |

### 비교 대상

```python
우리 방법 vs 기존 방법

1. BLS (Box Least Squares)
   - 전통적인 알고리즘 방법
   - 속도 및 정확도 비교

2. Astronet (Shallue & Vanderburg 2018)
   - 딥러닝 방법
   - Kepler 데이터 성능 비교

3. AstroNet-Vetting (Yu et al. 2019)
   - 딥러닝 방법
   - TESS 데이터 성능 비교
```

## 🔄 전체 코드 흐름

```python
# 전체 파이프라인 예시

# 1. 데이터 로드 및 처리
light_curves = load_data('kepler_data.csv')
processed_curves = preprocess(light_curves)

# 2. 특징 추출
features = extract_features(processed_curves)

# 3. 학습/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.1
)

# 4. 모델 학습
model = LGBMClassifier(**best_params)
model.fit(X_train, y_train)

# 5. 예측
predictions = model.predict_proba(X_test)

# 6. 평가
auc = roc_auc_score(y_test, predictions[:, 1])
recall = recall_score(y_test, predictions[:, 1] > threshold)
precision = precision_score(y_test, predictions[:, 1] > threshold)

print(f"AUC: {auc:.3f}")
print(f"Recall: {recall:.3f}")
print(f"Precision: {precision:.3f}")
```

## 📝 요약

- **3단계 파이프라인**: 데이터 처리 → 특징 추출 → 모델 학습
- **3개 데이터셋**: K2 시뮬레이션, Kepler, TESS
- **주요 도구**: tsfresh (특징 추출), LightGBM (분류)
- **핵심 지표**: AUC (전체 성능), Recall (행성 발견율)
- **최적화**: 2단계 하이퍼파라미터 최적화
- **검증**: 10-fold 교차 검증

## 🤔 퀴즈로 확인하기

1. 3단계 파이프라인은 무엇인가요?
   <details>
   <summary>답 보기</summary>
   데이터 처리 → 특징 추출 → 모델 학습
   </details>

2. tsfresh는 무엇을 하나요?
   <details>
   <summary>답 보기</summary>
   시계열 데이터에서 자동으로 789개의 특징을 추출
   </details>

3. 왜 Recall이 중요한가요?
   <details>
   <summary>답 보기</summary>
   실제 행성을 최대한 많이 찾아야 하기 때문 (놓치면 안 됨!)
   </details>

4. 10-fold 교차 검증이란?
   <details>
   <summary>답 보기</summary>
   데이터를 10개로 나눠서 각각을 검증 세트로 사용하며 10번 평가
   </details>

## 🚀 다음 단계

전체 방법론을 이해했습니다!

다음은 **데이터 처리** 단계를 자세히 알아보겠습니다.

👉 **[다음: 데이터 처리](05_data_processing.md)**

---

**도움이 필요하신가요?**
- [← 이전: 머신러닝 기초](03_machine_learning_basics.md)
- [용어 사전](09_glossary.md)에서 모르는 용어를 찾아보세요
