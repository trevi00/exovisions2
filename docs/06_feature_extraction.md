# 6. 특징 추출 (Feature Extraction)

## 🎯 특징 추출이란?

**특징(Feature)**은 데이터를 수치로 표현한 것입니다.

```
광도 곡선 (원시 데이터)     →     789개의 숫자 (특징)
[1.0, 0.99, 0.98, ...]    →     [평균, 표준편차, FFT계수, ...]
시간 시리즈 (복잡)         →     수치 배열 (간단)
```

## 🔧 tsfresh 라이브러리

### 왜 tsfresh인가?

**tsfresh (Time Series Feature extraction)**
- 시계열 데이터에서 **자동으로** 특징 추출
- **789개**의 다양한 특징 생성
- 통계적으로 검증된 특징들

### 설치

```bash
pip install tsfresh
```

### 기본 사용법

```python
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters
import pandas as pd

# 광도 곡선 데이터 준비
df = pd.DataFrame({
    'id': [1, 1, 1, 2, 2, 2],  # 광도 곡선 ID
    'time': [0, 1, 2, 0, 1, 2],
    'flux': [1.0, 0.99, 1.0, 1.0, 0.98, 1.0]
})

# 특징 추출
features = extract_features(
    df,
    column_id='id',
    column_sort='time',
    column_value='flux',
    default_fc_parameters=EfficientFCParameters()
)

print(features.shape)  # (2, 789) - 2개 곡선, 789개 특징
```

## 📊 추출되는 특징 유형

### 1. 통계적 특징 (Statistical Features)

기본적인 통계 값들:

```python
# 중심 경향
mean                    # 평균
median                  # 중앙값
variance                # 분산
standard_deviation      # 표준편차

# 분포 형태
skewness               # 왜도 (비대칭성)
kurtosis               # 첨도 (뾰족함)

# 위치 통계
minimum                # 최소값
maximum                # 최대값
quantile_25            # 1사분위수
quantile_75            # 3사분위수
```

**예시: 왜도(Skewness)**
```
대칭 분포 (skewness ≈ 0):
    •
  • • •
• • • • •

오른쪽 꼬리 (skewness > 0):
  •
• • •
    • • •

왼쪽 꼬리 (skewness < 0):
    • • •
  • • •
•
```

### 2. 에너지 및 파워 특징

```python
# 에너지
absolute_energy        # Σ(x²) - 신호의 총 에너지
absolute_sum_changes   # Σ|x[i+1] - x[i]| - 변화량 총합

# 파워
variance_larger_than_std  # 분산 > 표준편차인 비율
```

**예시: Absolute Energy**
```
flux = [1.0, 0.99, 0.98, 1.0]
absolute_energy = 1.0² + 0.99² + 0.98² + 1.0² = 3.9205
```

### 3. 주파수 영역 특징 (Frequency Domain)

FFT (Fast Fourier Transform)로 주파수 분석:

```python
# FFT 계수
fft_coefficient        # 푸리에 변환 계수
fft_aggregated         # 집계된 FFT 특성

# 파워 스펙트럼
spectral_centroid      # 스펙트럼 중심
spectral_entropy       # 스펙트럼 엔트로피
```

**시각적 이해**
```
시간 영역:
amplitude
    ↑
    │ ~·~·~·~·~
    └─────────→ time

주파수 영역:
power
    ↑  |
    │  |    |
    │  |  | |
    └─────────→ frequency
       주요 주파수!
```

### 4. 자기상관 특징 (Autocorrelation)

신호가 자기 자신과 얼마나 유사한지:

```python
autocorrelation        # 자기상관 함수
partial_autocorrelation  # 부분 자기상관
```

**주기적 신호 탐지**
```
주기적 신호:
╲╱╲╱╲╱╲╱  → 높은 자기상관

랜덤 노이즈:
·•·•·•·•  → 낮은 자기상관
```

### 5. 복잡도 측정

신호의 복잡도와 무작위성:

```python
# 엔트로피
entropy                # Shannon 엔트로피
approximate_entropy    # 근사 엔트로피
sample_entropy         # 샘플 엔트로피

# 복잡도
cid_ce                 # Complexity-Invariant Distance
```

### 6. 선형성 및 추세

```python
# 선형 추세
linear_trend           # 선형 회귀 기울기
agg_linear_trend       # 집계 선형 추세

# 자기회귀 모델
ar_coefficient         # AR 모델 계수
```

### 7. 카운트 및 비율

```python
# 임계값 기반
count_above_mean       # 평균보다 큰 값 개수
count_below_mean       # 평균보다 작은 값 개수

# 변화
number_peaks           # 피크 개수
number_crossing_m      # 평균 교차 횟수
```

## 📐 특징 추출 전체 과정

### 1단계: 데이터 준비

```python
import numpy as np
import pandas as pd
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters

# 여러 광도 곡선 준비
light_curves = []
for curve_id in range(100):
    time = np.linspace(0, 10, 1000)
    flux = load_light_curve(curve_id)  # 가상의 함수

    df = pd.DataFrame({
        'id': curve_id,
        'time': time,
        'flux': flux
    })
    light_curves.append(df)

# 하나의 DataFrame으로 결합
all_curves = pd.concat(light_curves)
```

### 2단계: 특징 추출

```python
# 특징 추출 (시간 소요: 수 분)
features = extract_features(
    all_curves,
    column_id='id',
    column_sort='time',
    column_value='flux',
    default_fc_parameters=EfficientFCParameters()
)

print(f"Shape: {features.shape}")
# Output: Shape: (100, 789)
```

### 3단계: 특징 정리

```python
# 1. 상수 특징 제거
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0)
features_filtered = selector.fit_transform(features)

# 2. 결측치 처리
features_filtered = pd.DataFrame(features_filtered)
features_filtered = features_filtered.fillna(features_filtered.mean())

# 3. 스케일링 (Robust Scaler)
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
features_scaled = scaler.fit_transform(features_filtered)

print(f"Final shape: {features_scaled.shape}")
# 약 700개 특징으로 축소됨
```

## 🔍 주요 특징 분석

### 특징 중요도 확인

```python
import lightgbm as lgb
import matplotlib.pyplot as plt

# 모델 학습
model = lgb.LGBMClassifier()
model.fit(X_train, y_train)

# 특징 중요도
feature_importance = model.feature_importances_
feature_names = features.columns

# 상위 20개 특징
top_20_idx = np.argsort(feature_importance)[-20:]
top_20_features = feature_names[top_20_idx]
top_20_importance = feature_importance[top_20_idx]

# 시각화
plt.figure(figsize=(10, 8))
plt.barh(range(20), top_20_importance)
plt.yticks(range(20), top_20_features)
plt.xlabel('Importance')
plt.title('Top 20 Most Important Features')
plt.tight_layout()
plt.show()
```

### 특징 상관관계 분석

```python
import seaborn as sns

# 상위 50개 특징만 선택
top_50_features = features[top_20_features[:50]]

# 상관관계 행렬
corr_matrix = top_50_features.corr()

# 히트맵
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.show()
```

## 💻 완전한 특징 추출 파이프라인

```python
class FeatureExtractor:
    """광도 곡선 특징 추출 클래스"""

    def __init__(self):
        self.scaler = None
        self.feature_names = None

    def extract_and_process(self, light_curves_df):
        """
        전체 특징 추출 및 처리

        Parameters:
        -----------
        light_curves_df : DataFrame
            columns: ['id', 'time', 'flux']

        Returns:
        --------
        features_processed : numpy array
            처리된 특징 배열
        """
        print("1. tsfresh로 특징 추출 중...")
        features = extract_features(
            light_curves_df,
            column_id='id',
            column_sort='time',
            column_value='flux',
            default_fc_parameters=EfficientFCParameters()
        )

        print(f"   추출된 특징: {features.shape[1]}개")

        print("2. 상수 특징 제거 중...")
        features = self._remove_constant_features(features)
        print(f"   남은 특징: {features.shape[1]}개")

        print("3. 결측치 처리 중...")
        features = self._handle_missing_values(features)

        print("4. 스케일링 중...")
        features = self._scale_features(features)

        print("✓ 특징 추출 완료!")
        return features

    def _remove_constant_features(self, features):
        """상수 특징 제거"""
        selector = VarianceThreshold(threshold=0)
        features_filtered = selector.fit_transform(features)
        self.feature_names = features.columns[selector.get_support()]
        return pd.DataFrame(features_filtered, columns=self.feature_names)

    def _handle_missing_values(self, features):
        """결측치를 평균으로 대체"""
        return features.fillna(features.mean())

    def _scale_features(self, features):
        """Robust Scaler로 스케일링"""
        from sklearn.preprocessing import RobustScaler

        if self.scaler is None:
            self.scaler = RobustScaler()
            scaled = self.scaler.fit_transform(features)
        else:
            scaled = self.scaler.transform(features)

        return scaled

# 사용 예시
extractor = FeatureExtractor()
X = extractor.extract_and_process(light_curves_df)
```

## 📊 특징 예시

실제 광도 곡선에서 추출된 특징 예:

```python
# 예시 광도 곡선
curve_id = 1
features_sample = features.loc[curve_id]

print("주요 특징:")
print(f"  평균: {features_sample['flux__mean']:.4f}")
print(f"  표준편차: {features_sample['flux__std']:.4f}")
print(f"  왜도: {features_sample['flux__skewness']:.4f}")
print(f"  FFT 계수(0): {features_sample['flux__fft_coefficient__coeff_0']:.4f}")
print(f"  자기상관(1): {features_sample['flux__autocorrelation__lag_1']:.4f}")

# 출력:
#   평균: 0.9985
#   표준편차: 0.0042
#   왜도: -0.2341
#   FFT 계수(0): 0.9985
#   자기상관(1): 0.9876
```

## 📝 요약

- **tsfresh**: 자동 시계열 특징 추출 라이브러리
- **789개 특징**: 다양한 유형의 특징 생성
- **특징 유형**: 통계, 에너지, 주파수, 자기상관, 복잡도 등
- **전처리**: 상수 제거, 결측치 처리, 스케일링
- **중요도 분석**: 어떤 특징이 중요한지 확인 가능

## 🤔 퀴즈로 확인하기

1. 특징 추출이 왜 필요한가요?
   <details>
   <summary>답 보기</summary>
   고전적 머신러닝은 원시 데이터를 직접 처리할 수 없어 수치로 표현된 특징이 필요
   </details>

2. tsfresh는 몇 개의 특징을 추출하나요?
   <details>
   <summary>답 보기</summary>
   약 789개의 시계열 특징
   </details>

3. 왜 스케일링을 하나요?
   <details>
   <summary>답 보기</summary>
   특징들이 서로 다른 범위를 가지므로 동일한 스케일로 만들어 모델 학습을 안정화
   </details>

## 🚀 다음 단계

특징 추출을 완료했습니다!

다음은 이 특징들로 **모델을 학습**하는 방법을 알아보겠습니다.

👉 **[다음: 모델 학습](07_model_training.md)**

---

**도움이 필요하신가요?**
- [← 이전: 데이터 처리](05_data_processing.md)
- [용어 사전](09_glossary.md)에서 모르는 용어를 찾아보세요
