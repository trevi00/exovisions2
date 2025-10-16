# 5. 데이터 처리

## 🎯 데이터 처리의 목적

원시 광도 곡선을 **머신러닝에 적합한 형태**로 변환하는 것입니다.

```
[원시 데이터]               [처리된 데이터]
노이즈 많음      →      깨끗함
불규칙한 간격    →      균일한 간격
별 변동성 포함   →      평탄화됨
```

## 🔧 데이터 처리 파이프라인

### 전체 흐름

```
1. 원시 광도 곡선 로드
   ↓
2. 우주선 충돌(Cosmic Ray) 제거
   ↓
3. 별 변동성 제거
   ↓
4. 데이터 갭 보간
   ↓
5. 균일한 리샘플링
   ↓
6. 정규화
   ↓
7. 처리된 광도 곡선 저장
```

## 🛠️ 각 단계 상세 설명

### 1. 우주선 충돌 제거

#### 문제
우주에서 날아온 고에너지 입자가 센서에 충돌하면 갑작스러운 밝기 증가가 발생합니다.

```
밝기
 ↑
1.00 │  •·•·•·•·|·•·•·•·     ← 우주선 충돌!
     │          ↑
     │        이상치
     └──────────────────→ 시간
```

#### 해결 방법: 5σ 아웃라이어 제거

```python
def remove_cosmic_rays(time, flux):
    """
    5σ 기준으로 우주선 충돌 제거
    """
    clean_flux = flux.copy()

    for i in range(1, len(flux) - 1):
        # 이전 점과 다음 점의 평균
        neighbors_mean = (flux[i-1] + flux[i+1]) / 2

        # 현재 점이 5σ 이상 높으면
        if flux[i] > neighbors_mean + 5 * std:
            # 제거하거나 보간
            clean_flux[i] = neighbors_mean

    return clean_flux
```

#### 예시

```
Before:
• • • • | • • •  ← 스파이크
      ↑
After:
• • • • • • • •  ← 평탄함
```

### 2. 별 변동성 제거

#### 문제
별 자체가 시간에 따라 밝기가 변합니다 (흑점, 회전 등).

```
밝기
 ↑
1.00 │ ·~·~·~·~·~·~·~·~    ← 별의 변동
     │  ╲╱
     │   트랜짓이 묻혀버림!
     └──────────────────→ 시간
```

#### 해결 방법: 반복적 스플라인 피팅

```python
def remove_stellar_variability(time, flux, iterations=5):
    """
    반복적으로 저주파 변동 제거
    """
    clean_flux = flux.copy()

    for iter in range(iterations):
        # 1. 데이터 스무딩
        smoothed = savgol_filter(clean_flux, window=51, polyorder=3)

        # 2. 데이터 비닝
        binned_time, binned_flux = bin_data(time, smoothed, bins=100)

        # 3. 스플라인 피팅
        spline = UnivariateSpline(binned_time, binned_flux, s=0.1)
        trend = spline(time)

        # 4. 트렌드 제거
        clean_flux = clean_flux / trend

        # 5. 음의 3σ 아웃라이어 클리핑
        mask = clean_flux < (mean - 3*std)
        if np.sum(mask) == 0:
            break  # 수렴

    return clean_flux
```

#### 단계별 시각화

```
원본:
━━╲  ╱━━╲  ╱━━
   ╲╱    ╲╱

스플라인 피팅:
━━~~~~~~~~~━━  ← 저주파 트렌드

트렌드 제거 후:
━━━━━━━━━━━━━  ← 평탄함!
```

### 3. 데이터 갭 보간

#### 문제 (특히 K2)
K2는 자세 제어 문제로 주기적인 관측 갭이 있습니다.

```
데이터
 ↑
 │ ••••••••    (갭)    ••••••••
 │         ↑          ↑
 │       중단        재개
 └──────────────────────────→ 시간
```

#### 해결 방법: 선형 보간

```python
from scipy.interpolate import interp1d

def interpolate_gaps(time, flux):
    """
    갭을 선형 보간으로 채우기
    """
    # 유효한 데이터만 선택
    valid_mask = ~np.isnan(flux)
    time_valid = time[valid_mask]
    flux_valid = flux[valid_mask]

    # 선형 보간 함수 생성
    interpolator = interp1d(
        time_valid, flux_valid,
        kind='linear',
        fill_value='extrapolate'
    )

    # 전체 시간에 대해 보간
    flux_interpolated = interpolator(time)

    return flux_interpolated
```

### 4. 균일한 리샘플링

#### 목적
tsfresh 특징 추출을 위해 **균일한 시간 간격** 필요합니다.

#### 방법: 1시간 윈도우

```python
def resample_uniform(time, flux, frequency='1H'):
    """
    1시간 간격으로 리샘플링
    """
    # pandas DataFrame으로 변환
    df = pd.DataFrame({'flux': flux}, index=pd.to_datetime(time, unit='D'))

    # 1시간 간격으로 리샘플링
    df_resampled = df.resample(frequency).mean()

    # 결측치는 선형 보간
    df_resampled = df_resampled.interpolate(method='linear')

    return df_resampled.index, df_resampled['flux'].values
```

#### 왜 1시간?

```
너무 짧으면 (예: 10분):
  ✗ 데이터 크기가 너무 커짐
  ✗ 계산 시간 증가

너무 길면 (예: 6시간):
  ✗ 트랜짓 세부 정보 손실
  ✗ 특징 품질 저하

1시간이 최적:
  ✓ 트랜짓 정보 보존
  ✓ 적당한 데이터 크기
  ✓ 빠른 계산
```

### 5. 정규화

#### 목적
모든 광도 곡선을 **동일한 스케일**로 만들기

#### 방법

```python
def normalize(flux):
    """
    중앙값으로 정규화
    """
    median = np.median(flux)
    normalized_flux = flux / median

    return normalized_flux
```

#### 효과

```
Before (다양한 스케일):
광도곡선 A:  [980, 975, 970, ...]   ← 밝은 별
광도곡선 B:  [50, 49.5, 49, ...]    ← 어두운 별

After (동일한 스케일):
광도곡선 A:  [1.00, 0.995, 0.990, ...]
광도곡선 B:  [1.00, 0.990, 0.980, ...]
```

## 📊 데이터셋별 특별 처리

### K2 시뮬레이션 데이터

```python
# K2 Campaign 7 처리
1. Vanderburg & Johnson (2014) 보정 데이터 사용
2. 추가 우주선 제거 (5σ)
3. 별 변동성 제거 (반복 스플라인)
4. S/N > 12인 곡선 제거 (행성 후보 제거)
5. 50% 곡선에 인공 트랜짓 주입

# 인공 트랜짓 파라미터
- 주기: 0.23 ~ 30일 (랜덤)
- 행성 반경: 랜덤
- 궤도 경사: 랜덤 (적어도 50% 트랜짓 보임)
- 별 림 다크닝: 랜덤
```

### Kepler 데이터

```python
# Shallue & Vanderburg (2018) 데이터 사용
1. Kepler 파이프라인 처리 완료 데이터
2. 약 70,000 데이터 포인트/곡선
3. 29.4분 간격
4. 평탄화 및 아웃라이어 제거 완료

# 추가 처리
- 1시간 리샘플링
- 정규화
```

### TESS 데이터

```python
# MIT QLP (Quick Look Pipeline) 데이터 사용
1. FFI (Full Frame Images)로부터 추출
2. QLP 내부 보정 적용됨
3. 27일 관측 (짧음!)
4. 케플러보다 밝은 별

# 주의사항
- 단일 트랜짓만 있을 수 있음
- 신호가 약할 수 있음
```

## 💻 전체 코드 예시

```python
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, UnivariateSpline
from scipy.signal import savgol_filter

class LightCurveProcessor:
    """광도 곡선 처리 클래스"""

    def __init__(self, time, flux):
        self.time = time
        self.flux = flux

    def process(self):
        """전체 처리 파이프라인"""
        print("1. 우주선 충돌 제거...")
        self.flux = self.remove_cosmic_rays()

        print("2. 별 변동성 제거...")
        self.flux = self.remove_stellar_variability()

        print("3. 갭 보간...")
        self.time, self.flux = self.interpolate_gaps()

        print("4. 리샘플링...")
        self.time, self.flux = self.resample_uniform()

        print("5. 정규화...")
        self.flux = self.normalize()

        print("✓ 처리 완료!")
        return self.time, self.flux

    def remove_cosmic_rays(self, sigma=5):
        """우주선 충돌 제거"""
        flux = self.flux.copy()
        for i in range(1, len(flux) - 1):
            neighbors_mean = (flux[i-1] + flux[i+1]) / 2
            if flux[i] > neighbors_mean + sigma * np.std(flux):
                flux[i] = neighbors_mean
        return flux

    def remove_stellar_variability(self, iterations=5):
        """별 변동성 제거"""
        flux = self.flux.copy()
        for _ in range(iterations):
            smoothed = savgol_filter(flux, 51, 3)
            binned_time, binned_flux = self._bin_data(self.time, smoothed)
            spline = UnivariateSpline(binned_time, binned_flux, s=0.1)
            trend = spline(self.time)
            flux = flux / trend

            # 음의 아웃라이어 클리핑
            mean, std = np.mean(flux), np.std(flux)
            mask = flux < (mean - 3 * std)
            if not mask.any():
                break
        return flux

    def interpolate_gaps(self):
        """갭 보간"""
        valid = ~np.isnan(self.flux)
        if not valid.all():
            f = interp1d(self.time[valid], self.flux[valid],
                        kind='linear', fill_value='extrapolate')
            flux = f(self.time)
        else:
            flux = self.flux
        return self.time, flux

    def resample_uniform(self, frequency='1H'):
        """균일 리샘플링"""
        df = pd.DataFrame({'flux': self.flux},
                         index=pd.to_datetime(self.time, unit='D'))
        df = df.resample(frequency).mean().interpolate()
        return df.index.values, df['flux'].values

    def normalize(self):
        """정규화"""
        return self.flux / np.median(self.flux)

    def _bin_data(self, time, flux, bins=100):
        """데이터 비닝"""
        bin_edges = np.linspace(time.min(), time.max(), bins+1)
        bin_indices = np.digitize(time, bin_edges)
        binned_time = []
        binned_flux = []
        for i in range(1, bins+1):
            mask = bin_indices == i
            if mask.any():
                binned_time.append(time[mask].mean())
                binned_flux.append(flux[mask].mean())
        return np.array(binned_time), np.array(binned_flux)

# 사용 예시
processor = LightCurveProcessor(time, flux)
processed_time, processed_flux = processor.process()
```

## 📝 요약

- **우주선 제거**: 5σ 아웃라이어 제거
- **별 변동성 제거**: 반복 스플라인 피팅
- **갭 보간**: 선형 보간
- **리샘플링**: 1시간 균일 간격
- **정규화**: 중앙값으로 스케일링

## 🤔 퀴즈로 확인하기

1. 왜 우주선 충돌을 제거해야 하나요?
   <details>
   <summary>답 보기</summary>
   갑작스러운 밝기 증가가 행성 신호로 오인될 수 있기 때문
   </details>

2. 별 변동성을 어떻게 제거하나요?
   <details>
   <summary>답 보기</summary>
   스플라인 피팅으로 저주파 트렌드를 찾아 제거
   </details>

3. 왜 1시간 리샘플링을 하나요?
   <details>
   <summary>답 보기</summary>
   특징 추출 라이브러리(tsfresh)가 균일한 간격을 필요로 하고, 1시간이 정보 손실과 계산량의 균형이 좋기 때문
   </details>

## 🚀 다음 단계

데이터 처리를 마쳤습니다!

다음은 **특징 추출** 방법을 알아보겠습니다.

👉 **[다음: 특징 추출](06_feature_extraction.md)**

---

**도움이 필요하신가요?**
- [← 이전: 연구 방법론 개요](04_methodology.md)
- [용어 사전](09_glossary.md)에서 모르는 용어를 찾아보세요
