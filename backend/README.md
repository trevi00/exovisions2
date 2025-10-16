# Exoplanet Detection API

NASA 2025 Space Apps Challenge - 외계행성 탐지 ML 모델 백엔드 API

## 프로젝트 구조

이 프로젝트는 **DDD (Domain-Driven Design)** 아키텍처를 사용합니다.

```
backend/
├── app/
│   ├── domain/                 # Domain Layer
│   │   ├── entities/          # 핵심 엔티티 (Prediction, LightCurve)
│   │   ├── value_objects/     # 값 객체 (PredictionResult, ConfidenceScore)
│   │   ├── repositories/      # 리포지토리 인터페이스
│   │   └── services/          # 도메인 서비스 인터페이스
│   ├── application/           # Application Layer
│   │   ├── dto/              # Data Transfer Objects
│   │   └── use_cases/        # 유스케이스 (비즈니스 로직)
│   ├── infrastructure/        # Infrastructure Layer
│   │   ├── database/         # DB 연결 및 모델
│   │   ├── ml/               # ML 모델, 특징 추출, 전처리
│   │   └── repositories/     # 리포지토리 구현
│   └── presentation/          # Presentation Layer
│       ├── api/              # FastAPI 엔드포인트
│       └── main.py           # 메인 애플리케이션
├── models/                    # 학습된 ML 모델 저장
├── train_model.py            # 모델 학습 스크립트
└── requirements.txt          # 의존성 패키지
```

## 주요 기능

### 1. 외계행성 예측 (POST /api/v1/predictions/)
- 광도 곡선 데이터 또는 특징값을 입력받아 외계행성 여부 예측
- Stacking 앙상블 모델 사용 (LGBM + GradientBoosting + RandomForest)
- 결과를 데이터베이스에 저장 (옵션)

### 2. 예측 결과 조회 (GET /api/v1/predictions/)
- 모든 예측 결과 조회 (페이지네이션 지원)
- 외계행성 여부로 필터링 가능

### 3. 예측 결과 단건 조회 (GET /api/v1/predictions/{id})
- ID로 특정 예측 결과 조회

### 4. 예측 결과 삭제 (DELETE /api/v1/predictions/{id})
- 특정 예측 결과 삭제

### 5. 전체 예측 결과 삭제 (DELETE /api/v1/predictions/)
- 모든 예측 결과 삭제
- 외계행성 여부로 필터링 가능

### 6. 헬스 체크 (GET /api/v1/health)
- 서버 상태 확인

### 7. 모델 정보 조회 (GET /api/v1/model/info)
- 현재 로드된 ML 모델 정보 조회

## 설치 및 실행

### 1. 환경 설정

```bash
# uv 환경 활성화
cd backend

# 의존성 설치
uv pip install -r requirements.txt
```

### 2. 데이터 준비

프로젝트 루트의 `data/` 디렉터리에 다음 파일들을 준비:
- `cumulative.csv` - Kepler KOI 데이터
- `TOI.csv` - TESS TOI 데이터 (옵션)
- `k2pandc.csv` - K2 데이터 (옵션)

### 3. 모델 학습

```bash
cd backend
python train_model.py
```

학습이 완료되면 `models/` 디렉터리에 다음 파일들이 생성됩니다:
- `exoplanet_model.pkl` - 학습된 모델
- `scaler.pkl` - 스케일러
- `feature_names.pkl` - 특징 이름 목록

### 4. API 서버 실행

```bash
cd backend/app/presentation
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

또는

```bash
python -m uvicorn app.presentation.main:app --reload
```

서버가 실행되면:
- API 문서: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Base URL: http://localhost:8000/api/v1

## API 사용 예시

### 1. 외계행성 예측

```bash
curl -X POST "http://localhost:8000/api/v1/predictions/" \
  -H "Content-Type: application/json" \
  -d '{
    "light_curve_data": {
      "time": [0.0, 0.1, 0.2, 0.3, 0.4],
      "flux": [1.0, 0.95, 0.98, 1.0, 0.99],
      "flux_err": [0.01, 0.01, 0.01, 0.01, 0.01]
    },
    "save_result": true
  }'
```

### 2. 예측 결과 조회

```bash
# 모든 예측 조회
curl "http://localhost:8000/api/v1/predictions/"

# 외계행성만 조회
curl "http://localhost:8000/api/v1/predictions/?is_exoplanet=true"

# 페이지네이션
curl "http://localhost:8000/api/v1/predictions/?skip=0&limit=10"
```

### 3. 특정 예측 조회

```bash
curl "http://localhost:8000/api/v1/predictions/{prediction_id}"
```

### 4. 예측 삭제

```bash
# 단건 삭제
curl -X DELETE "http://localhost:8000/api/v1/predictions/{prediction_id}"

# 전체 삭제
curl -X DELETE "http://localhost:8000/api/v1/predictions/"
```

### 5. 헬스 체크

```bash
curl "http://localhost:8000/api/v1/health"
```

## 모델 성능

- **모델**: Stacking Ensemble (LGBM + GradientBoosting + RandomForest)
- **데이터**: NASA Kepler KOI dataset
- **평가 메트릭**:
  - Accuracy: ~95%+
  - Precision: ~90%+
  - Recall: ~85%+
  - F1 Score: ~87%+
  - ROC AUC: ~95%+

## 데이터베이스

- **기본**: SQLite (개발용)
- **프로덕션**: PostgreSQL 또는 MySQL 권장

데이터베이스 URL은 환경 변수로 설정 가능:
```bash
export DATABASE_URL="postgresql://user:password@localhost/exoplanet_db"
```

## 환경 변수

- `DATABASE_URL`: 데이터베이스 연결 URL (기본값: sqlite:///./exoplanet_predictions.db)

## 개발

### 테스트 실행

```bash
pytest tests/
```

### 코드 스타일

```bash
# 포맷팅
black app/

# 린팅
flake8 app/
```

## 기술 스택

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **ML**: LightGBM, scikit-learn
- **Data Processing**: pandas, numpy, scipy
- **Architecture**: DDD (Domain-Driven Design)

## 라이선스

MIT License

## 참고 자료

- [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
- [Kepler Mission](https://www.nasa.gov/mission_pages/kepler/main/index.html)
- [TESS Mission](https://tess.mit.edu/)
