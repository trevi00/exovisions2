# 10. 참고 자료 및 추가 학습

## 📄 원본 논문

### 주요 논문

**1. 이 프로젝트의 기반 논문**
```
제목: Exoplanet detection using machine learning
저자: Abhishek Malik, Benjamin P Moster, Christian Obermeier
발표: Monthly Notices of the Royal Astronomical Society (MNRAS)
연도: 2022
DOI: https://doi.org/10.1093/mnras/stab3692
```

**2. 딥러닝 비교 논문 (Kepler)**
```
제목: Identifying Exoplanets with Deep Learning
저자: Shallue & Vanderburg
발표: The Astronomical Journal
연도: 2018
링크: https://arxiv.org/abs/1712.05044
```

**3. 딥러닝 비교 논문 (TESS)**
```
제목: Identifying Exoplanets with Deep Learning III: Automated Triage and Vetting
저자: Yu et al.
발표: The Astronomical Journal
연도: 2019
링크: https://arxiv.org/abs/1906.11268
```

## 🌐 주요 웹사이트

### 외계행성 데이터베이스

**NASA Exoplanet Archive**
- https://exoplanetarchive.ipac.caltech.edu/
- 확인된 모든 외계행성 정보
- Kepler, K2, TESS 데이터 다운로드

**Exoplanet.eu**
- http://exoplanet.eu/
- 유럽의 외계행성 데이터베이스
- 시각화 도구 제공

**TESS Data Archive (MAST)**
- https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html
- TESS 원시 데이터 다운로드
- Light curve 파일 제공

### 우주 망원경 공식 사이트

**Kepler Mission**
- https://www.nasa.gov/mission_pages/kepler/main/index.html
- 미션 정보 및 발견 내역

**TESS Mission**
- https://tess.mit.edu/
- 실시간 관측 정보
- 데이터 처리 파이프라인 설명

**James Webb Space Telescope**
- https://www.jwst.nasa.gov/
- 외계행성 대기 분석

## 📚 학습 자료

### 머신러닝 기초

**온라인 강의**
1. **Coursera - Machine Learning by Andrew Ng**
   - https://www.coursera.org/learn/machine-learning
   - 머신러닝 기초의 정석
   - 무료 청강 가능

2. **Fast.ai - Practical Deep Learning**
   - https://www.fast.ai/
   - 실용적인 딥러닝
   - 무료

3. **Google - Machine Learning Crash Course**
   - https://developers.google.com/machine-learning/crash-course
   - 구글의 ML 입문 과정
   - 무료

**책**
1. **"Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"**
   - 저자: Aurélien Géron
   - 실습 중심의 머신러닝 교과서

2. **"Python Machine Learning"**
   - 저자: Sebastian Raschka
   - Python으로 배우는 ML

### 천문학 및 외계행성

**온라인 강의**
1. **Coursera - Astrobiology and the Search for Extraterrestrial Life**
   - https://www.coursera.org/learn/astrobiology
   - 생명 가능 행성 탐색

2. **edX - Exoplanets**
   - https://www.edx.org/
   - 외계행성 과학

**책**
1. **"Exoplanets" by Sara Seager**
   - 외계행성 과학의 종합서

2. **"The Exoplanet Handbook" by Michael Perryman**
   - 외계행성 탐지 방법 상세 설명

## 🛠️ 도구 및 라이브러리

### Python 라이브러리

**데이터 처리**
```python
numpy          # 수치 계산
pandas         # 데이터 분석
scipy          # 과학 계산
```

**시각화**
```python
matplotlib     # 기본 플로팅
seaborn        # 통계 시각화
plotly         # 인터랙티브 플로팅
```

**머신러닝**
```python
scikit-learn   # 전통적 ML
lightgbm       # Gradient Boosting
xgboost        # 또 다른 Gradient Boosting
tensorflow     # 딥러닝
pytorch        # 딥러닝
```

**시계열 분석**
```python
tsfresh        # 시계열 특징 추출 (우리가 사용!)
statsmodels    # 통계 모델
prophet        # 시계열 예측
```

**천문학 특화**
```python
astropy        # 천문학 계산
lightkurve     # Kepler/TESS 데이터 분석
```

### 설치 가이드

```bash
# 기본 패키지
pip install numpy pandas scipy matplotlib seaborn

# 머신러닝
pip install scikit-learn lightgbm

# 시계열 분석
pip install tsfresh

# 천문학
pip install astropy lightkurve
```

## 📖 튜토리얼 및 예제

### tsfresh 튜토리얼
```python
# 공식 문서
https://tsfresh.readthedocs.io/

# 기본 사용법
from tsfresh import extract_features
from tsfresh.feature_extraction import EfficientFCParameters

# 특징 추출
features = extract_features(
    timeseries_df,
    column_id='id',
    column_sort='time',
    default_fc_parameters=EfficientFCParameters()
)
```

### LightGBM 튜토리얼
```python
# 공식 문서
https://lightgbm.readthedocs.io/

# 기본 사용법
import lightgbm as lgb

model = lgb.LGBMClassifier(
    n_estimators=100,
    max_depth=5
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### Lightkurve 튜토리얼 (Kepler/TESS 데이터)
```python
# 공식 문서
https://docs.lightkurve.org/

# Kepler 데이터 다운로드
import lightkurve as lk

search_result = lk.search_lightcurve('Kepler-10', mission='Kepler')
lc = search_result.download()
lc.plot()
```

## 🎓 추가 학습 주제

### 초급 → 중급

1. **데이터 전처리 심화**
   - 이상치 탐지 알고리즘
   - 고급 보간 기법
   - 신호 처리 (Fourier, Wavelet)

2. **특징 공학 (Feature Engineering)**
   - 도메인 지식 기반 특징 생성
   - 특징 선택 (Feature Selection)
   - 차원 축소 (PCA, t-SNE)

3. **모델 앙상블**
   - Voting Classifier
   - Stacking
   - Blending

### 중급 → 고급

1. **딥러닝으로 확장**
   - CNN for time series
   - RNN/LSTM
   - Transformer for time series

2. **AutoML**
   - Hyperparameter optimization (Optuna)
   - Neural Architecture Search

3. **실시간 처리**
   - 스트리밍 데이터 처리
   - 온라인 학습

## 💻 GitHub 저장소

### 관련 프로젝트

**1. Astronet (Shallue & Vanderburg)**
- https://github.com/google-research/exoplanet-ml
- TensorFlow 기반 딥러닝 모델

**2. AstroNet-Vetting (Yu et al.)**
- https://github.com/yuliang419/AstroNet-Vetting
- TESS 데이터용 딥러닝

**3. Lightkurve**
- https://github.com/lightkurve/lightkurve
- Kepler/TESS 데이터 분석 도구

**4. tsfresh**
- https://github.com/blue-yonder/tsfresh
- 시계열 특징 추출

## 📊 데이터셋

### 공개 데이터셋

**1. Kepler Data**
```
위치: NASA Exoplanet Archive
크기: ~150,000 광도 곡선
기간: 4년
레이블: Autovetter Catalog
```

**2. TESS Data**
```
위치: MAST Archive
크기: 수백만 광도 곡선
기간: 27일/섹터
레이블: TESS TOI Catalog
```

**3. K2 Data**
```
위치: MAST Archive
캠페인: 19개 캠페인
기간: 80일/캠페인
```

## 🎯 연습 프로젝트 아이디어

### 초급
1. **간단한 트랜짓 시뮬레이터 만들기**
   - 인공 트랜짓 생성
   - 노이즈 추가
   - 시각화

2. **BLS 구현하기**
   - Box model 피팅
   - 주기 탐색
   - 성능 측정

### 중급
3. **tsfresh 특징 분석**
   - 어떤 특징이 중요한지 확인
   - 특징 선택 최적화
   - 시각화

4. **하이퍼파라미터 최적화**
   - Grid Search
   - Random Search
   - Bayesian Optimization

### 고급
5. **딥러닝 모델 구현**
   - CNN으로 광도 곡선 분류
   - Astronet 재현
   - 성능 비교

6. **실시간 탐지 시스템**
   - 새 데이터 자동 처리
   - 웹 대시보드 구축
   - 알림 시스템

## 📧 커뮤니티

### 포럼 및 Q&A

**Stack Overflow**
- 태그: `[machine-learning]`, `[astronomy]`, `[python]`

**Reddit**
- r/MachineLearning
- r/Astronomy
- r/datascience

**Kaggle**
- Exoplanet 관련 컴피티션
- 노트북 공유

## 📝 추가 읽을거리

### 리뷰 논문

1. **"Machine Learning in Astronomy"** (Baron, 2019)
   - 천문학에서의 ML 종합 리뷰

2. **"Deep Learning in Astronomy"** (Fluke & Jacobs, 2020)
   - 천문학에서의 딥러닝 응용

### 최신 연구

**arXiv.org**
- astro-ph 카테고리
- cs.LG (Machine Learning) 카테고리
- 매일 새로운 논문 업데이트

## 🎓 학위 과정

### 온라인 학위

**Georgia Tech - Online MS in Computer Science**
- Machine Learning Specialization
- 온라인으로 석사 학위

**University of London - BSc Computer Science**
- Machine Learning 과목 포함

### 천문학 연구기관

**NASA Exoplanet Science Institute (NExScI)**
- https://nexsci.caltech.edu/
- 연구 프로그램 및 인턴십

## 🏆 데이터 과학 경진대회

**Kaggle Competitions**
- 외계행성 관련 과거 대회 참고
- https://www.kaggle.com/

**DrivenData**
- 과학 데이터 대회
- https://www.drivendata.org/

## 📝 요약

이 가이드를 통해:
- ✅ 기초부터 고급까지 학습 자료 제공
- ✅ 실습 가능한 도구 및 라이브러리 소개
- ✅ 추가 프로젝트 아이디어 제시
- ✅ 커뮤니티 및 최신 연구 접근 방법

## 🚀 다음 단계

**학습을 완료했습니다!**

이제 실제 코드를 작성하고 실험해보세요:
1. 데이터 다운로드
2. 전처리 파이프라인 구축
3. 모델 학습 및 평가
4. 결과 분석 및 개선

---

**질문이 있으신가요?**
- [← README로 돌아가기](README.md)
- [← 용어 사전](09_glossary.md)
- 계속 학습하고 실험하세요!

**Good luck with your exoplanet detection project! 🌟🪐**
