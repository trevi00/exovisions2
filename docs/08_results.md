# 8. 결과 분석

## 📊 전체 결과 요약

세 가지 데이터셋에서의 성능 비교:

| 데이터셋 | AUC | Recall | Precision | Accuracy |
|---------|-----|--------|-----------|----------|
| **K2 시뮬레이션** | 0.92 | 0.94 | 0.92 | 0.91 |
| **Kepler 실제** | 0.948 | 0.96 | 0.82 | - |
| **TESS 실제** | 0.81 | 0.82 | 0.63 | 0.98 |

## 🔬 K2 시뮬레이션 데이터 결과

### 성능 지표

```python
데이터 구성:
- 총 7,873개 광도 곡선
- 행성: 3,937개 (50%)
- 비행성: 3,936개 (50%)

결과:
- AUC: 0.92
- Recall: 0.94 (94%의 행성 탐지)
- Precision: 0.92
- Accuracy: 0.91
```

### BLS와의 비교

```
BLS 방법:
- 탐지율: 96%
- 문제점: 오탐 많음, 느림

우리 방법:
- 탐지율: 94%
- 장점: 훨씬 빠름 (2분 vs 수일)
        오탐 적음
```

### 결정 임계값별 성능

```python
임계값: 0.5 (기본)
- Recall: 0.85
- Precision: 0.95

임계값: 0.13 (최적화)
- Recall: 0.94  ← 선택!
- Precision: 0.92
```

**선택 이유**: 행성을 놓치지 않는 것이 우선!

## 🌌 Kepler 데이터 결과

### 성능 지표

```python
데이터 구성:
- 총 15,737개 광도 곡선
- 행성 후보: 3,600개 (23%)
- 비행성: 12,137개 (77%)

결과:
- AUC: 0.948
- Recall: 0.96 (96%의 행성 탐지)
- Precision: 0.82
- 임계값: 0.46 (최적화)
```

### 딥러닝(Astronet)과의 비교

| 방법 | AUC | Recall | Precision |
|------|-----|--------|-----------|
| **Astronet (딥러닝)** | 0.988 | 0.95 | 0.93 |
| **우리 방법 (ML)** | 0.948 | 0.96 | 0.82 |

**분석**:
- AUC: 딥러닝이 약간 우수
- Recall: 우리 방법이 약간 높음 (더 많은 행성 발견)
- Precision: 딥러닝이 높음 (오탐 적음)
- **학습 시간**: 우리 방법이 압도적으로 빠름 (2분 vs 5시간)

### t-SNE 시각화

```python
# 고차원 특징을 2D로 압축
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, random_state=42)
features_2d = tsne.fit_transform(features)

# 시각화
plt.figure(figsize=(10, 8))
plt.scatter(features_2d[y==0, 0], features_2d[y==0, 1],
           c='blue', label='Non-Planet', alpha=0.5)
plt.scatter(features_2d[y==1, 0], features_2d[y==1, 1],
           c='red', label='Planet', alpha=0.7)
plt.legend()
plt.title('t-SNE Visualization of Kepler Light Curves')
plt.show()
```

**관찰**: 행성 광도 곡선들이 한 영역에 군집!

## 🛰️ TESS 데이터 결과

### 성능 지표

```python
데이터 구성:
- 총 16,500개 광도 곡선
- 행성 후보: 492개 (3%) ← 심한 불균형!
- 식쌍성: 2,154개
- 잡음: 13,854개

결과 (기본 임계값 0.5):
- AUC: 0.81
- Recall: 0.62
- Precision: 0.84
- Accuracy: 0.98

결과 (최적화 임계값 0.12):
- AUC: 0.81
- Recall: 0.82  ← 선택!
- Precision: 0.63
```

### 딥러닝(AstroNet-Vetting)과의 비교

#### 기본 임계값 (0.5)

| 방법 | AUC | Recall | Precision |
|------|-----|--------|-----------|
| **AstroNet-Vetting** | 0.98 | 0.57 | 0.65 |
| **우리 방법** | 0.81 | 0.62 | 0.84 |

#### 최적화 임계값

| 방법 | AUC | Recall | Precision |
|------|-----|--------|-----------|
| **AstroNet-Vetting** | 0.98 | 0.89 | 0.45 |
| **우리 방법** | 0.81 | 0.82 | 0.63 |

**분석**:
- AUC: 딥러닝이 확실히 높음
- Recall: 비슷한 수준
- **Precision: 우리 방법이 40% 더 높음!**
  - 오탐이 거의 절반!
  - 전문가 검토 시간 대폭 절감

### TESS의 어려움

```
1. 짧은 관측 기간 (27일)
   → 단일 트랜짓만 있을 수 있음
   → 신호가 약함

2. 심한 클래스 불균형 (3% vs 97%)
   → 학습이 어려움
   → 더 많은 행성 데이터 필요

3. 다양한 오탐 원인
   → 식쌍성, 별 활동, 노이즈
```

## 📈 Precision vs Recall 트레이드오프

### 세 데이터셋 비교

```python
# Precision-Recall 곡선
plt.figure(figsize=(10, 6))

for dataset, results in zip(['K2 Sim', 'Kepler', 'TESS'],
                            [k2_results, kepler_results, tess_results]):
    plt.plot(results['recall'], results['precision'],
            label=dataset, linewidth=2)

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend()
plt.grid(True)
plt.show()
```

**관찰**:
- K2와 Kepler: 비슷한 성능
- TESS: 낮은 성능 (클래스 불균형)

## 🔍 오류 분석

### 놓친 행성 (False Negative)

```python
# FN 샘플 분석
fn_samples = X_test[(y_test == 1) & (y_pred == 0)]

print(f"놓친 행성: {len(fn_samples)}개")

# 특징 분석
fn_features = pd.DataFrame(fn_samples, columns=feature_names)
print(fn_features.describe())

# 주요 원인
원인 1: S/N < 12 (신호가 너무 약함)
원인 2: 단일 트랜짓
원인 3: 불규칙한 트랜짓 모양
```

### 오탐 (False Positive)

```python
# FP 샘플 분석
fp_samples = X_test[(y_test == 0) & (y_pred == 1)]

print(f"오탐: {len(fp_samples)}개")

# 주요 원인
원인 1: 식쌍성 (44%)
원인 2: 별 활동성 (32%)
원인 3: 우주선 충돌 잔여 (15%)
원인 4: 기기 노이즈 (9%)
```

## 📊 혼동 행렬 (Confusion Matrix)

### Kepler 데이터 예시

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

# 혼동 행렬 계산
cm = confusion_matrix(y_test, y_pred)

# 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix - Kepler Data')
plt.show()

# 출력:
#              예측: 비행성   예측: 행성
# 실제: 비행성    1,150        64
# 실제: 행성        14         345
```

**해석**:
- TP (진양성): 345개 - 정확히 찾은 행성
- TN (진음성): 1,150개 - 정확히 걸러낸 비행성
- FP (위양성): 64개 - 비행성을 행성으로 잘못 예측
- FN (위음성): 14개 - 행성을 놓침

## 🎯 최적 임계값 선택

### 임계값에 따른 성능 변화

```python
thresholds = np.arange(0.1, 0.9, 0.05)
recalls = []
precisions = []
f1_scores = []

for threshold in thresholds:
    y_pred = (y_proba >= threshold).astype(int)

    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    recalls.append(recall)
    precisions.append(precision)
    f1_scores.append(f1)

# 시각화
plt.figure(figsize=(10, 6))
plt.plot(thresholds, recalls, label='Recall', marker='o')
plt.plot(thresholds, precisions, label='Precision', marker='s')
plt.plot(thresholds, f1_scores, label='F1 Score', marker='^')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Performance vs Threshold')
plt.legend()
plt.grid(True)
plt.show()
```

## 💡 주요 발견사항

### 1. 효율성

```
우리 방법 (고전 ML):
✓ 학습 시간: 2-5분
✓ CPU만 필요
✓ 메모리 효율적

딥러닝:
✗ 학습 시간: 5+ 시간
✗ GPU 필요
✗ 큰 메모리 필요
```

### 2. 성능

```
K2 시뮬레이션: BLS와 거의 동등
Kepler 실제: 딥러닝과 비슷
TESS 실제: 딥러닝보다 오탐 50% 감소
```

### 3. 해석 가능성

```python
# 중요 특징 top 10
중요 특징:
1. flux__fft_coefficient__coeff_1
2. flux__autocorrelation__lag_1
3. flux__variance
4. flux__absolute_energy
5. flux__skewness
6. flux__kurtosis
7. flux__mean
8. flux__standard_deviation
9. flux__quantile__q_0.25
10. flux__count_above_mean
```

**장점**: 어떤 특징이 중요한지 알 수 있음!

## 🚀 실용적 응용

### 자동 탐지 시스템

```python
# 1단계: 전처리
processed_curves = preprocess(raw_light_curves)

# 2단계: 특징 추출
features = extract_features(processed_curves)

# 3단계: 예측
predictions = model.predict_proba(features)

# 4단계: 필터링
planet_candidates = predictions[predictions >= threshold]

# 5단계: 우선순위 정렬
sorted_candidates = np.argsort(planet_candidates)[::-1]

# 상위 100개만 전문가 검토
top_candidates = sorted_candidates[:100]
```

**효과**:
- TESS 1개 섹터: 100만 곡선 → 100개로 축소
- 전문가 검토 시간: 수 주 → 수 일

## 📝 요약

### 주요 성과

1. **K2 시뮬레이션**: 94% 탐지율, BLS와 동등
2. **Kepler**: 96% 탐지율, 딥러닝과 비슷
3. **TESS**: 82% 탐지율, 오탐 50% 감소

### 장점

- ✅ 빠른 학습 (2-5분)
- ✅ 낮은 하드웨어 요구사항
- ✅ 해석 가능
- ✅ 여러 데이터셋에 범용적

### 한계

- ❌ TESS에서 낮은 AUC (0.81)
- ❌ 클래스 불균형에 민감
- ❌ 딥러닝보다 약간 낮은 성능

### 개선 방향

1. **더 많은 TESS 데이터 수집**
2. **앙상블 방법 적용**
3. **도메인 특화 특징 추가**
4. **준지도 학습 탐색**

## 🤔 퀴즈로 확인하기

1. 세 데이터셋 중 가장 어려운 것은?
   <details>
   <summary>답 보기</summary>
   TESS (짧은 관측 기간, 심한 클래스 불균형)
   </details>

2. 우리 방법의 가장 큰 장점은?
   <details>
   <summary>답 보기</summary>
   빠른 학습 시간 (2-5분)과 낮은 하드웨어 요구사항
   </details>

3. TESS에서 딥러닝보다 나은 점은?
   <details>
   <summary>답 보기</summary>
   오탐이 절반으로 감소 (Precision 0.63 vs 0.45)
   </details>

## 🎓 결론

머신러닝을 이용한 외계행성 탐지 방법은 **빠르고 효율적**이며, 딥러닝과 **비슷한 성능**을 달성합니다.

특히 **실용적 응용**에서 큰 장점:
- 일반 컴퓨터로 실행 가능
- 빠른 프로토타이핑
- 해석 가능한 결과

---

**축하합니다! 전체 학습을 완료했습니다!** 🎉

- [← 이전: 모델 학습](07_model_training.md)
- [← README로 돌아가기](README.md)
- [참고 자료](10_references.md)에서 추가 학습하세요!
