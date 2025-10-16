# 외계행성 탐지 머신러닝 학습 가이드

## 🌟 환영합니다!

이 문서는 **머신러닝을 이용한 외계행성 탐지**에 대해 초보자도 쉽게 이해할 수 있도록 만들어진 학습 자료입니다.

## 📚 학습 순서

이 가이드는 순차적으로 읽으실 것을 권장합니다:

### 기초 개념
1. **[외계행성 탐지 소개](01_introduction.md)**
   - 외계행성이란?
   - 왜 중요한가?
   - 탐지 방법들

2. **[트랜짓 방법 이해하기](02_transit_method.md)**
   - 트랜짓 방법의 원리
   - 광도 곡선이란?
   - 실제 예시

3. **[머신러닝 기초](03_machine_learning_basics.md)**
   - 머신러닝이란?
   - 분류(Classification)란?
   - 왜 외계행성 탐지에 사용하나?

### 연구 방법론
4. **[연구 방법론 개요](04_methodology.md)**
   - 전체 프로세스 이해하기
   - 3단계 워크플로우
   - 사용된 도구들

5. **[데이터 처리](05_data_processing.md)**
   - 광도 곡선 전처리
   - 노이즈 제거
   - 데이터 정규화

6. **[특징 추출](06_feature_extraction.md)**
   - 시계열 특징이란?
   - tsfresh 라이브러리
   - 789개의 특징들

7. **[모델 학습](07_model_training.md)**
   - Gradient Boosted Trees
   - 교차 검증
   - 하이퍼파라미터 최적화

### 결과와 분석
8. **[결과 분석](08_results.md)**
   - 성능 평가 지표
   - 데이터셋별 결과
   - 기존 방법과의 비교

### 앙상블 방법 (추가 학습)
9. **[앙상블 방법](11_ensemble_methods.md)**
   - 앙상블 기본 개념
   - Bagging, Boosting, Stacking
   - 5가지 앙상블 알고리즘 상세

10. **[KOI 데이터셋](12_koi_dataset.md)**
    - KOI 데이터셋 소개
    - 데이터 전처리 과정
    - 특징(Features) 설명

11. **[앙상블 결과 분석](13_ensemble_results.md)**
    - 알고리즘별 상세 결과
    - 하이퍼파라미터 튜닝 효과
    - 실전 적용 가이드

### 참고 자료
12. **[용어 사전](09_glossary.md)**
    - 주요 용어 설명
    - 약어 정리

13. **[참고 자료 및 추가 학습](10_references.md)**
    - 논문 링크
    - 추천 학습 자료
    - 유용한 웹사이트

## 🎯 학습 목표

이 가이드를 완료하면 다음을 할 수 있게 됩니다:

- ✅ 외계행성 탐지의 기본 개념 이해
- ✅ 트랜짓 방법의 원리 파악
- ✅ 머신러닝 기반 탐지 방법의 작동 원리 이해
- ✅ 실제 데이터 처리 과정 이해
- ✅ 모델 성능 평가 방법 습득
- ✅ 앙상블 방법의 원리와 장단점 파악 (추가)
- ✅ KOI 데이터셋 전처리 방법 숙지 (추가)
- ✅ 5가지 앙상블 알고리즘 비교 분석 (추가)

## 📊 프로젝트 구조

```
exovisions2/
├── docs/                      # 📖 학습 문서 (지금 여기!)
│   ├── README.md
│   ├── 01_introduction.md
│   ├── 02_transit_method.md
│   ├── 03_machine_learning_basics.md
│   ├── 04_methodology.md
│   ├── 05_data_processing.md
│   ├── 06_feature_extraction.md
│   ├── 07_model_training.md
│   ├── 08_results.md
│   ├── 09_glossary.md
│   ├── 10_references.md
│   ├── 11_ensemble_methods.md    # 🆕 앙상블 방법
│   ├── 12_koi_dataset.md         # 🆕 KOI 데이터셋
│   └── 13_ensemble_results.md    # 🆕 앙상블 결과
├── cumulative_2025.10.14_06.16.25.csv  # 📈 Kepler 데이터
├── TOI_2025.10.14_06.16.33.csv         # 📈 TESS 데이터
└── k2pandc_2025.10.14_06.16.39.csv     # 📈 K2 데이터
```

## 💡 학습 팁

1. **순서대로 읽기**: 각 문서는 이전 내용을 기반으로 작성되었습니다.
2. **실습하기**: 이론을 읽은 후 코드 예제를 직접 실행해보세요.
3. **용어 확인**: 모르는 용어는 [용어 사전](09_glossary.md)을 참고하세요.
4. **천천히**: 한 번에 모든 것을 이해하려 하지 마세요. 천천히 반복해서 읽으세요.

## 🚀 시작하기

준비되셨나요? [첫 번째 문서: 외계행성 탐지 소개](01_introduction.md)부터 시작해보세요!

## ❓ 질문이 있으신가요?

- 각 문서의 끝에는 "다음 단계" 섹션이 있습니다.
- 용어가 어려우면 [용어 사전](09_glossary.md)을 참고하세요.
- 더 깊이 공부하고 싶다면 [참고 자료](10_references.md)를 확인하세요.

---

## 📖 추가 자료

2024년 논문 "Assessment of Ensemble-Based Machine Learning Algorithms for Exoplanet Identification"의 내용을 기반으로 **앙상블 방법** 섹션을 추가했습니다.

- 5가지 앙상블 알고리즘 상세 설명
- KOI 데이터셋 완전 분석
- 실전 적용 가능한 코드 예제

---

**마지막 업데이트**: 2025년 1월 14일
