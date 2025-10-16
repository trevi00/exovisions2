# 12. KOI 데이터셋 (Kepler Object of Interest)

## 🌌 KOI 데이터셋이란?

**KOI (Kepler Object of Interest)**는 NASA의 케플러 우주 망원경이 수집한 외계행성 후보 데이터셋입니다.

### 역사

```
2009년: 케플러 망원경 발사
          ↓
4년간 20만 개 이상의 별 관측
          ↓
트랜짓 방법으로 행성 후보 발견
          ↓
KOI 데이터셋 생성
```

**KOI의 특징**:
- NASA Exoplanet Science Institute (NExScI) 개발
- 공개 데이터셋 (누구나 무료 사용)
- 확인된 외계행성 + 후보 + 오탐(False Positive) 포함

## 📊 데이터셋 구조

### 기본 정보

```
원본 데이터:
- 행(Rows): 9,654개
- 열(Columns): 50개
- 파일명: cumulative.csv
- 다운로드: NASA Exoplanet Archive
```

### 데이터 구성

```
KOI 데이터셋 내용:

1. 별 특성 (Stellar Parameters)
   - 위치 (Position)
   - 밝기 (Magnitude)
   - 온도 (Temperature)

2. 행성 특성 (Exoplanet Parameters)
   - 질량 (Mass)
   - 궤도 정보 (Orbital Information)
   - 주기 (Period)

3. 관측 데이터
   - 광도 곡선 (Light Curve)
   - 시간에 따른 밝기 변화

4. 분류 (Classification)
   - CONFIRMED: 확인된 외계행성
   - CANDIDATE: 외계행성 후보
   - FALSE POSITIVE: 오탐
```

## 🔧 데이터 전처리 과정

### 1단계: 불필요한 컬럼 제거

```python
# 제거된 6개 컬럼

제거 이유: 예측에 기여하지 않는 식별자

1. rowid
   - 단순 행 번호
   - Primary Key

2. kepid
   - 고유 랜덤 번호
   - 행성 식별자

3. kepoi_name
   - 두 번째 고유 번호
   - 행성 식별자

4. kepler_name
   - 텍스트 형식 행성 이름

5. koi_pdisposition
   - koi_disposition과 중복
   - 혼동 방지를 위해 제거

6. koi_score
   - 0과 1 사이 신뢰도 값
   - 예측에 간섭 가능성
```

### 추가 제거

```python
# 완전히 비어있는 컬럼
- koi_teq_err1
- koi_teq_err2

# 결과
원본: 50 컬럼 → 처리 후: 43 컬럼
```

### 2단계: 타겟 컬럼 정리

```python
# 원본 타겟 컬럼 (koi_disposition)
값: 'CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'

# 단계 1: FALSE POSITIVE 제거
이유: 확인된 행성과 후보만 필요

# 단계 2: 이진 변환
'CONFIRMED' → 0 (확인된 외계행성)
'CANDIDATE' → 1 (외계행성 후보)
```

**왜 이진 변환?**
```
머신러닝 분류 문제:
- 2개 클래스만 필요
- 0과 1로 단순화
- 알고리즘 학습 효율 향상
```

### 3단계: 결측치 처리

```python
# koi_tce_delivname 컬럼
결측치 → 평균값으로 대체

# 범주형 변수 변환
카테고리 → 더미 변수 (Dummy Variables)
           숫자로 변환
```

### 4단계: 데이터 분할

```python
# X (독립 변수): 43개 특징
features = [
    'koi_period',        # 궤도 주기
    'koi_time0bk',       # 트랜짓 시간
    'koi_impact',        # 충돌 매개변수
    'koi_duration',      # 트랜짓 지속 시간
    'koi_depth',         # 트랜짓 깊이
    ...                  # 나머지 38개
]

# y (종속 변수): 1개 타겟
target = 'koi_disposition'  # 0 or 1
```

### 5단계: 스케일링

```python
from sklearn.preprocessing import StandardScaler

# StandardScaler 적용
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 모든 특징을 같은 범위로 정규화
# 평균 = 0, 표준편차 = 1
```

**스케일링 전후 비교**:
```
스케일링 전:
koi_period: [0.5, 365, 4000, ...]  ← 범위가 매우 넓음
koi_depth:  [10, 500, 10000, ...]  ← 범위가 다름

스케일링 후:
koi_period: [-1.2, 0.3, 2.1, ...]  ← 평균 0, 표준편차 1
koi_depth:  [-0.8, 1.5, 0.2, ...]  ← 같은 범위
```

### 6단계: 학습/테스트 분할

```python
from sklearn.model_selection import train_test_split

# 70% 학습, 30% 테스트
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.3,
    random_state=42,    # 재현성을 위한 시드
    stratify=y          # 클래스 비율 유지
)

# 결과
학습 데이터: 3,178 행 × 43 컬럼
  - CONFIRMED: 1,589개
  - CANDIDATE: 1,589개

테스트 데이터: 1,362 행 × 43 컬럼
```

## 📈 최종 데이터셋 구조

### 처리 전후 비교

```
원본:
┌─────────────────────────────┐
│  9,654 행 × 50 컬럼          │
│  CONFIRMED / CANDIDATE /    │
│  FALSE POSITIVE             │
└─────────────────────────────┘

↓ 전처리

최종:
┌─────────────────────────────┐
│  4,540 행 × 43 컬럼          │
│  (FALSE POSITIVE 제거됨)     │
│  0 (CONFIRMED): 1,589개     │
│  1 (CANDIDATE): 1,589개     │
└─────────────────────────────┘

↓ 분할

학습 (70%):                    테스트 (30%):
3,178 행                       1,362 행
```

## 🔍 주요 특징(Features) 설명

### 1. 궤도 특성

```python
# 행성의 궤도 정보

koi_period         # 궤도 주기 (일)
                   # 예: 365일 = 지구와 비슷

koi_time0bk        # 첫 트랜짓 시간
                   # 관측 시작 시점 기준

koi_impact         # 충돌 매개변수
                   # 0 = 별 중심 통과
                   # 1 = 별 가장자리
```

### 2. 트랜짓 특성

```python
# 광도 곡선에서 추출

koi_duration       # 트랜짓 지속 시간 (시간)
                   # 행성이 별을 가리는 시간

koi_depth          # 트랜짓 깊이 (ppm)
                   # 밝기 감소량
                   # 클수록 큰 행성

koi_prad           # 행성 반지름 (지구 = 1)
                   # 예: 2.0 = 지구의 2배

koi_teq            # 평형 온도 (K)
                   # 행성 표면 예상 온도
```

### 3. 별 특성

```python
# 중심별(호스트 스타) 정보

koi_srad           # 별 반지름 (태양 = 1)
koi_smass          # 별 질량 (태양 = 1)
koi_steff          # 별 유효 온도 (K)
koi_slogg          # 별 표면 중력
```

### 4. 신호 품질

```python
# 관측 데이터 품질

koi_model_snr      # 신호 대 잡음 비 (S/N)
                   # 클수록 신뢰도 높음

koi_tce_plnt_num   # 동일 별 주위 행성 번호
                   # 1 = 첫 번째 행성
                   # 2 = 두 번째 행성
```

## 📊 KOI vs 다른 데이터셋 비교

### 데이터셋 비교표

| 특성 | KOI (Kepler) | TESS | K2 Campaign 7 |
|------|--------------|------|---------------|
| **망원경** | Kepler | TESS | Kepler |
| **관측 기간** | 4년 | 27일/섹터 | 80일 |
| **총 데이터** | 9,654개 | 수백만 | 7,873개 |
| **클래스 균형** | 균형잡힘 | 심한 불균형 | 균형잡힘 |
| **신호 품질** | 높음 | 중간 | 높음 |
| **사용 목적** | 연구용 | 최신 탐지 | 시뮬레이션 |

### 장단점 비교

```
KOI (Kepler):
✅ 장점:
  - 4년간 장기 관측 → 여러 트랜짓 확인
  - 클래스 균형 (50:50)
  - 높은 신호 품질
  - 43개의 다양한 특징

❌ 단점:
  - 관측이 끝남 (더 이상 데이터 추가 X)
  - 제한된 하늘 영역

TESS:
✅ 장점:
  - 현재 진행 중 (계속 데이터 추가)
  - 전천구 관측
  - 최신 데이터

❌ 단점:
  - 짧은 관측 (27일)
  - 심한 클래스 불균형 (3% vs 97%)
  - 단일 트랜짓만 있을 수 있음

K2 Campaign 7:
✅ 장점:
  - 시뮬레이션 데이터 (완벽한 라벨)
  - 클래스 균형
  - 연구 검증용

❌ 단점:
  - 실제 데이터가 아님
  - 제한적 사용
```

## 💻 데이터 로딩 코드

### 전체 전처리 파이프라인

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class KOIDataProcessor:
    """KOI 데이터셋 전처리 클래스"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.X = None
        self.y = None
        self.scaler = StandardScaler()

    def load_data(self):
        """데이터 로드"""
        print("1. 데이터 로딩 중...")
        self.df = pd.read_csv(self.filepath)
        print(f"   원본: {self.df.shape[0]} 행 × {self.df.shape[1]} 컬럼")
        return self

    def remove_columns(self):
        """불필요한 컬럼 제거"""
        print("2. 불필요한 컬럼 제거 중...")

        columns_to_remove = [
            'rowid', 'kepid', 'kepoi_name',
            'kepler_name', 'koi_pdisposition',
            'koi_score', 'koi_teq_err1', 'koi_teq_err2'
        ]

        self.df = self.df.drop(columns=columns_to_remove, errors='ignore')
        print(f"   남은 컬럼: {self.df.shape[1]}개")
        return self

    def filter_target(self):
        """FALSE POSITIVE 제거"""
        print("3. FALSE POSITIVE 제거 중...")

        before = len(self.df)
        self.df = self.df[self.df['koi_disposition'].isin(['CONFIRMED', 'CANDIDATE'])]
        after = len(self.df)

        print(f"   제거된 행: {before - after}개")
        print(f"   남은 행: {after}개")
        return self

    def encode_target(self):
        """타겟 컬럼 이진 인코딩"""
        print("4. 타겟 컬럼 인코딩 중...")

        self.df['koi_disposition'] = self.df['koi_disposition'].map({
            'CONFIRMED': 0,
            'CANDIDATE': 1
        })

        print(f"   CONFIRMED (0): {(self.df['koi_disposition'] == 0).sum()}개")
        print(f"   CANDIDATE (1): {(self.df['koi_disposition'] == 1).sum()}개")
        return self

    def handle_missing(self):
        """결측치 처리"""
        print("5. 결측치 처리 중...")

        # 수치형 컬럼: 평균으로 대체
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(
            self.df[numeric_cols].mean()
        )

        # 범주형 컬럼: 더미 변수 변환
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        categorical_cols = categorical_cols.drop('koi_disposition', errors='ignore')

        if len(categorical_cols) > 0:
            self.df = pd.get_dummies(self.df, columns=categorical_cols)

        print("   ✓ 결측치 처리 완료")
        return self

    def split_features_target(self):
        """특징과 타겟 분리"""
        print("6. 특징/타겟 분리 중...")

        self.y = self.df['koi_disposition']
        self.X = self.df.drop('koi_disposition', axis=1)

        print(f"   특징(X): {self.X.shape}")
        print(f"   타겟(y): {self.y.shape}")
        return self

    def scale_features(self):
        """특징 스케일링"""
        print("7. 특징 스케일링 중...")

        self.X = pd.DataFrame(
            self.scaler.fit_transform(self.X),
            columns=self.X.columns,
            index=self.X.index
        )

        print("   ✓ StandardScaler 적용 완료")
        return self

    def split_train_test(self, test_size=0.3, random_state=42):
        """학습/테스트 분할"""
        print("8. 학습/테스트 분할 중...")

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y
        )

        print(f"   학습 세트: {X_train.shape}")
        print(f"   테스트 세트: {X_test.shape}")
        print("\n✓ 전처리 완료!")

        return X_train, X_test, y_train, y_test

    def process_all(self, test_size=0.3, random_state=42):
        """전체 전처리 실행"""
        return (self.load_data()
                    .remove_columns()
                    .filter_target()
                    .encode_target()
                    .handle_missing()
                    .split_features_target()
                    .scale_features()
                    .split_train_test(test_size, random_state))

# 사용 예시
processor = KOIDataProcessor('cumulative.csv')
X_train, X_test, y_train, y_test = processor.process_all()
```

## 🎯 앙상블 알고리즘 적용 결과

### 5가지 알고리즘 성능

```
데이터: KOI 데이터셋 (4,540 행)
방법: 10-fold 교차 검증
평가: Accuracy, Precision, Recall, F1 Score

결과:
모든 앙상블 알고리즘이 80% 이상 달성!
```

| 알고리즘 | Accuracy | Precision | Recall | F1 Score | 시간(초) |
|---------|----------|-----------|--------|----------|---------|
| **Stacking** | **83.08%** | **83.23%** | **80.05%** | **82.84%** | 10,856 |
| Adaboost | 82.52% | 82.86% | 79.45% | 82.43% | 1,627 |
| Random Forest | 82.64% | 82.81% | 76.64% | 82.52% | 2,916 |
| Random Subspace | 81.91% | 81.98% | 78.39% | 81.78% | 1,312 |
| Extra Trees | 82.36% | 82.27% | 79.08% | 82.21% | 155 |

### 주요 발견

**1. Stacking이 최고 성능**
```
Accuracy: 83.08%
- 다양한 알고리즘의 장점 결합
- 메타-모델이 최적 조합 학습
```

**2. 모든 알고리즘이 우수**
```
평균 Accuracy: 82.50%
- 80% 이상의 일관된 성능
- 앙상블의 강력함 입증
```

**3. 하이퍼파라미터 튜닝의 중요성**
```
Adaboost 예시:
튜닝 전: 81.37%
튜닝 후: 82.52%
향상: +1.15%
```

## 🔄 교차 검증 (Cross-Validation)

### 10-Fold CV 적용

```python
from sklearn.model_selection import StratifiedKFold

# 10개로 분할
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# 각 폴드마다 학습 및 평가
for fold, (train_idx, val_idx) in enumerate(kfold.split(X_train, y_train)):
    # 폴드별 데이터 분할
    X_tr = X_train[train_idx]
    y_tr = y_train[train_idx]
    X_vl = X_train[val_idx]
    y_vl = y_train[val_idx]

    # 모델 학습
    model.fit(X_tr, y_tr)

    # 평가
    score = model.score(X_vl, y_vl)
    print(f"Fold {fold + 1}: {score:.4f}")

# 평균 점수
print(f"평균 Accuracy: {np.mean(scores):.4f}")
```

**교차 검증의 장점**:
```
1. 과적합 방지
   - 여러 번 검증으로 신뢰도 높임

2. 데이터 효율적 사용
   - 모든 데이터를 학습과 검증에 활용

3. 일반화 성능 평가
   - 새로운 데이터에 대한 예측력 측정
```

## 📝 요약

- **KOI 데이터셋**: Kepler 망원경의 외계행성 후보 데이터
- **규모**: 9,654 행 → 전처리 후 4,540 행
- **특징**: 50 컬럼 → 43 컬럼 (예측 관련)
- **분할**: 70% 학습 (3,178), 30% 테스트 (1,362)
- **클래스**: 균형잡힘 (50:50)
- **전처리**: 컬럼 제거, 이진 인코딩, 스케일링
- **성능**: 모든 앙상블 알고리즘 80% 이상
- **최고**: Stacking 83.08%

## 🤔 퀴즈로 확인하기

1. KOI 데이터셋의 타겟 컬럼 값은?
   <details>
   <summary>답 보기</summary>
   0 (CONFIRMED) 또는 1 (CANDIDATE)
   </details>

2. 왜 FALSE POSITIVE를 제거했나요?
   <details>
   <summary>답 보기</summary>
   확인된 행성과 후보만 필요하고, 오탐은 예측에 혼란을 줄 수 있기 때문
   </details>

3. KOI 데이터셋의 가장 큰 장점은?
   <details>
   <summary>답 보기</summary>
   4년 장기 관측으로 높은 신호 품질과 균형잡힌 클래스 분포
   </details>

## 🚀 다음 단계

KOI 데이터셋을 이해했습니다!

다음은 **앙상블 알고리즘의 상세 결과**를 분석해보겠습니다.

👉 **[다음: 앙상블 결과 분석](13_ensemble_results.md)**

---

**참고 자료**:
- 원본 논문: "Assessment of Ensemble-Based Machine Learning Algorithms for Exoplanet Identification" (Electronics, 2024)
- NASA Exoplanet Archive: https://exoplanetarchive.ipac.caltech.edu/
- Kaggle KOI Dataset: https://www.kaggle.com/datasets/nasa/kepler-exoplanet-search-results
- [← 이전: 앙상블 방법](11_ensemble_methods.md)
- [용어 사전](09_glossary.md)
