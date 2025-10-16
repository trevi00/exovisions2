# 9. 용어 사전

## 📖 A-Z 순서

### A

**Accuracy (정확도)**
- 전체 예측 중 올바르게 분류된 비율
- `(TP + TN) / (TP + TN + FP + FN)`
- 불균형 데이터에서는 신뢰도 낮음

**AUC (Area Under the Curve)**
- ROC 곡선 아래 면적
- 모델의 전체 성능을 하나의 수치로 표현
- 0.5 (랜덤) ~ 1.0 (완벽)

**Autocorrelation (자기상관)**
- 시계열 데이터가 자기 자신과 얼마나 유사한지 측정
- 주기적 신호 탐지에 유용

### B

**BLS (Box Least Squares)**
- 트랜짓 탐지를 위한 전통적 알고리즘
- 상자 모양을 광도 곡선에 피팅
- 장점: 간단하고 효과적
- 단점: 낮은 S/N에 약함, 오탐 많음

**Binary Classification (이진 분류)**
- 데이터를 2개 클래스로 분류
- 이 프로젝트: 행성 vs 비행성

**Boosting**
- 약한 학습기들을 순차적으로 결합하여 강한 학습기 생성
- 각 학습기가 이전 학습기의 실수를 보완

### C

**Cosmic Ray (우주선)**
- 우주에서 날아오는 고에너지 입자
- 센서에 충돌하면 갑작스러운 스파이크 발생
- 전처리에서 제거 필요

**Cross-Validation (교차 검증)**
- 데이터를 여러 부분으로 나눠 반복 평가
- 과적합 방지 및 신뢰도 높은 성능 평가
- 이 프로젝트: 10-fold CV 사용

### D

**Decision Tree (결정 트리)**
- 트리 구조로 데이터를 분류하는 알고리즘
- if-then 규칙의 연속
- GBT의 기본 단위

**Deep Learning (딥러닝)**
- 다층 신경망을 사용하는 머신러닝
- 자동으로 특징 추출
- 많은 데이터와 계산 자원 필요

### E

**Eclipsing Binary (식쌍성)**
- 두 별이 서로를 가리는 쌍성계
- 행성 트랜짓과 유사한 광도 곡선
- 주요 오탐 원인

**Exoplanet (외계행성)**
- 태양계 밖의 별 주위를 도는 행성
- 현재 5,000개 이상 확인

### F

**False Positive (오탐, 위양성)**
- 행성이 아닌데 행성으로 예측
- FP (False Positive)
- 식쌍성, 별 활동, 노이즈 등이 원인

**False Negative (미탐, 위음성)**
- 행성인데 놓침
- FN (False Negative)
- 약한 신호, 단일 트랜짓 등이 원인

**Feature (특징)**
- 데이터를 수치로 표현한 것
- 이 프로젝트: 광도 곡선 → 789개 특징

**FFT (Fast Fourier Transform)**
- 시계열을 주파수 성분으로 분해
- 주기적 신호 탐지에 유용

### G

**GBT (Gradient Boosted Trees)**
- 그래디언트 부스팅 결정 트리
- 여러 트리를 순차적으로 학습
- LightGBM으로 구현

### H

**Hyperparameter (하이퍼파라미터)**
- 모델의 설정값
- 예: 트리 개수, 깊이, 학습률
- 성능에 큰 영향

### K

**Kepler**
- NASA의 외계행성 탐사 우주 망원경 (2009-2018)
- 2,600개 이상 행성 확인
- 한 영역을 4년간 관측

**K2**
- Kepler의 연장 임무 (2014-2018)
- 500개 이상 행성 발견
- 다양한 영역 관측

**Kurtosis (첨도)**
- 분포의 꼬리가 얼마나 두꺼운지 측정
- 정규분포 = 3
- 이상치 탐지에 유용

### L

**Label (레이블)**
- 지도 학습의 정답
- 이 프로젝트: 0 (비행성) or 1 (행성)

**Light Curve (광도 곡선)**
- 시간에 따른 별의 밝기 변화 그래프
- 트랜짓 방법의 핵심 데이터

**LightGBM**
- Microsoft의 GBT 구현체
- 빠르고 메모리 효율적
- 이 프로젝트에서 사용

### M

**Machine Learning (머신러닝)**
- 데이터로부터 자동으로 학습하는 기술
- 명시적 프로그래밍 없이 패턴 발견

### N

**Normalization (정규화)**
- 데이터를 일정한 범위/스케일로 변환
- 이 프로젝트: 중앙값으로 나눔

### O

**Overfitting (과적합)**
- 학습 데이터에만 너무 잘 맞춤
- 새로운 데이터에는 성능 떨어짐
- 교차 검증으로 방지

### P

**Phase-Folded (위상 접기)**
- 여러 트랜짓을 주기에 맞춰 겹침
- 약한 신호를 강화

**Precision (정밀도)**
- 행성으로 예측한 것 중 실제 행성 비율
- `TP / (TP + FP)`
- 오탐률과 관련

### R

**Recall (재현율)**
- 실제 행성 중 찾아낸 비율
- `TP / (TP + FN)`
- **가장 중요한 지표!**
- 행성을 놓치지 않는 것이 목표

**Resampling (리샘플링)**
- 데이터를 균일한 간격으로 재배치
- 이 프로젝트: 1시간 간격

**ROC Curve**
- 여러 임계값에서의 성능 곡선
- x축: 거짓 양성률, y축: 진짜 양성률
- AUC로 요약

### S

**Signal-to-Noise Ratio (S/N, 신호 대 잡음비)**
- 신호의 강도 대 노이즈의 강도
- 높을수록 신호가 명확함
- S/N > 12 면 양호

**Skewness (왜도)**
- 분포의 비대칭성 측정
- 0 = 대칭, + = 오른쪽 꼬리, - = 왼쪽 꼬리

**Supervised Learning (지도 학습)**
- 레이블이 있는 데이터로 학습
- 이 프로젝트에서 사용

### T

**TCE (Threshold Crossing Event)**
- 임계값을 넘는 이벤트
- 행성 후보로 추가 검토 필요

**TESS (Transiting Exoplanet Survey Satellite)**
- NASA의 외계행성 탐사 위성 (2018-현재)
- 하늘의 85% 관측
- 밝은 별 주변 행성 탐색

**Transit (트랜짓)**
- 행성이 별 앞을 지나가는 현상
- 별빛이 잠깐 감소

**Transit Method (트랜짓 방법)**
- 트랜짓을 이용한 외계행성 탐지 방법
- 가장 많이 사용 (75%)

**tsfresh**
- Time Series Feature extraction 라이브러리
- 시계열에서 자동으로 특징 추출
- 이 프로젝트: 789개 특징 추출

### U

**Unsupervised Learning (비지도 학습)**
- 레이블 없이 패턴 발견
- 클러스터링 등

### V

**Validation Set (검증 세트)**
- 하이퍼파라미터 조정용 데이터
- 학습에는 사용 안 함

### W

**Window (윈도우)**
- 시계열의 특정 구간
- 리샘플링에서 시간 단위

## 🔤 약어 정리

| 약어 | 전체 이름 | 설명 |
|------|----------|------|
| AFP | Astrophysical False Positive | 천체물리학적 오탐 |
| AUC | Area Under the Curve | ROC 곡선 아래 면적 |
| BLS | Box Least Squares | 상자 최소제곱법 |
| CNN | Convolutional Neural Network | 합성곱 신경망 |
| CV | Cross-Validation | 교차 검증 |
| DL | Deep Learning | 딥러닝 |
| EB | Eclipsing Binary | 식쌍성 |
| FFI | Full Frame Image | 전체 프레임 이미지 |
| FFT | Fast Fourier Transform | 고속 푸리에 변환 |
| FN | False Negative | 위음성, 미탐 |
| FP | False Positive | 위양성, 오탐 |
| GBT | Gradient Boosted Trees | 그래디언트 부스팅 트리 |
| ML | Machine Learning | 머신러닝 |
| NGTS | Next-Generation Transit Survey | 차세대 트랜짓 탐사 |
| NTP | Non-Transiting Phenomenon | 비트랜짓 현상 |
| PC | Planet Candidate | 행성 후보 |
| QLP | Quick Look Pipeline | 신속 처리 파이프라인 |
| RNN | Recurrent Neural Network | 순환 신경망 |
| ROC | Receiver Operating Characteristic | 수신자 조작 특성 |
| S/N | Signal-to-Noise Ratio | 신호 대 잡음비 |
| TCE | Threshold Crossing Event | 임계값 초과 이벤트 |
| TESS | Transiting Exoplanet Survey Satellite | 트랜짓 외계행성 탐사 위성 |
| TN | True Negative | 진음성 |
| TP | True Positive | 진양성 |
| t-SNE | t-distributed Stochastic Neighbor Embedding | t-분포 확률적 이웃 임베딩 |

## 📊 성능 지표 계산식

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)

Precision = TP / (TP + FP)

Recall = TP / (TP + FN)

F1 Score = 2 × (Precision × Recall) / (Precision + Recall)

TPR (True Positive Rate) = Recall = TP / (TP + FN)

FPR (False Positive Rate) = FP / (FP + TN)
```

여기서:
- **TP** (True Positive): 행성을 행성으로 예측 ✓
- **TN** (True Negative): 비행성을 비행성으로 예측 ✓
- **FP** (False Positive): 비행성을 행성으로 예측 ✗
- **FN** (False Negative): 행성을 비행성으로 예측 ✗

## 🚀 다음 단계

용어를 이해했습니다!

마지막으로 **참고 자료**를 확인해보세요.

👉 **[다음: 참고 자료](10_references.md)**

---

**도움이 필요하신가요?**
- [← README로 돌아가기](README.md)
- 이해가 안 되는 용어가 있나요? 질문해주세요!
