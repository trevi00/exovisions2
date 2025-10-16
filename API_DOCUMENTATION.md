# Exoplanet Detection API Documentation

## Overview
외계행성 탐지 머신러닝 모델을 위한 FastAPI 기반 REST API입니다. NASA의 Kepler, K2, TESS 데이터셋을 활용한 3-class classification 모델을 제공합니다.

**Version:** 1.0.0
**Base URL:** `http://127.0.0.1:8000`
**API Prefix:** `/api/v1`

---

## Model Information

### Classification Model
- **Type:** Multi-class Classification (3 classes)
- **Classes:**
  - `FALSE_POSITIVE`: 외계행성이 아님
  - `CANDIDATE`: 외계행성 후보
  - `CONFIRMED`: 확인된 외계행성
- **Algorithm:** Stacking Ensemble (LightGBM + GradientBoosting + RandomForest + LogisticRegression)
- **Training Data:**
  - Kepler: 9,618 samples
  - K2: 4,104 samples
  - TESS: 7,773 samples
  - **Total:** 21,495 samples

### Features (10)
1. `orbital_period` - 궤도 주기 (일)
2. `transit_duration` - 통과 지속시간 (시간)
3. `transit_depth` - 통과 깊이 (ppm)
4. `planet_radius` - 행성 반지름 (지구 반지름 단위)
5. `equilibrium_temp` - 평형 온도 (K)
6. `insolation` - 일사량 (지구 기준)
7. `signal_to_noise` - 신호 대 잡음비
8. `stellar_temp` - 별의 온도 (K)
9. `stellar_logg` - 별의 표면 중력 (log g)
10. `stellar_radius` - 별의 반지름 (태양 반지름 단위)

---

## API Endpoints

### 1. Root Endpoint
**GET** `/`

API 기본 정보 제공

#### Response
```json
{
  "message": "Welcome to Exoplanet Detection API",
  "version": "1.0.0",
  "docs": "/docs",
  "api": "/api/v1"
}
```

---

### 2. Health Check
**GET** `/api/v1/health`

서버 상태 확인

#### Response
```json
{
  "status": "healthy",
  "service": "Exoplanet Detection API",
  "version": "1.0.0"
}
```

---

### 3. Predict Exoplanet
**POST** `/api/v1/predictions/`

외계행성 여부를 예측합니다. 광도 곡선 데이터 또는 특징값 중 하나는 필수입니다.

#### Request Body
```json
{
  "features": {
    "orbital_period": 3.5,
    "transit_duration": 2.5,
    "transit_depth": 500.0,
    "planet_radius": 2.0,
    "equilibrium_temp": 1200.0,
    "insolation": 100.0,
    "signal_to_noise": 50.0,
    "stellar_temp": 5800.0,
    "stellar_logg": 4.5,
    "stellar_radius": 1.0
  },
  "save_result": true
}
```

#### Request Parameters
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `features` | object | conditional | 10개의 특징값 (위 참조) |
| `light_curve_data` | object | conditional | 광도 곡선 데이터 (time, flux, flux_err) |
| `save_result` | boolean | optional | 결과 저장 여부 (기본값: true) |

**Note:** `features` 또는 `light_curve_data` 중 하나는 반드시 제공해야 합니다.

#### Response (201 Created)
```json
{
  "id": "5ef0383f-5520-4642-ad95-83d74ed1feb3",
  "is_exoplanet": true,
  "classification": "CONFIRMED",
  "planet_probability": 0.901032,
  "candidate_probability": 0.0694371,
  "confidence_score": 0.901032,
  "confidence_level": "VERY_HIGH",
  "created_at": "2025-10-14T16:16:30",
  "light_curve_data": null
}
```

#### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | 예측 결과 고유 ID (UUID) |
| `is_exoplanet` | boolean | 외계행성 여부 |
| `classification` | string | 분류 결과 (CONFIRMED/LIKELY_CONFIRMED/CANDIDATE/FALSE_POSITIVE) |
| `planet_probability` | float | CONFIRMED 클래스 확률 (0.0-1.0) |
| `candidate_probability` | float | CANDIDATE 클래스 확률 (0.0-1.0) |
| `confidence_score` | float | 신뢰도 점수 (0.0-1.0) |
| `confidence_level` | string | 신뢰도 레벨 (VERY_HIGH/HIGH/MEDIUM/LOW/VERY_LOW) |
| `created_at` | datetime | 예측 생성 시간 |
| `light_curve_data` | object/null | 입력된 광도 곡선 데이터 |

#### Example curl
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predictions/" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "orbital_period": 3.5,
      "transit_duration": 2.5,
      "transit_depth": 500.0,
      "planet_radius": 2.0,
      "equilibrium_temp": 1200.0,
      "insolation": 100.0,
      "signal_to_noise": 50.0,
      "stellar_temp": 5800.0,
      "stellar_logg": 4.5,
      "stellar_radius": 1.0
    },
    "save_result": false
  }'
```

---

### 4. Get Predictions List
**GET** `/api/v1/predictions/`

저장된 모든 예측 결과를 조회합니다. 페이지네이션 및 필터링을 지원합니다.

#### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skip` | integer | optional | 0 | 건너뛸 개수 (페이지네이션) |
| `limit` | integer | optional | 100 | 조회할 개수 (최대 1000) |
| `is_exoplanet` | boolean | optional | null | 외계행성 여부 필터 (true/false) |

#### Response (200 OK)
```json
{
  "predictions": [
    {
      "id": "5ef0383f-5520-4642-ad95-83d74ed1feb3",
      "is_exoplanet": true,
      "classification": "CONFIRMED",
      "planet_probability": 0.901032,
      "candidate_probability": 0.0694371,
      "confidence_score": 0.901032,
      "confidence_level": "VERY_HIGH",
      "created_at": "2025-10-14T16:16:30",
      "light_curve_data": null
    },
    {
      "id": "19264170-5e0d-4ee2-88f4-92cb4f306190",
      "is_exoplanet": true,
      "classification": "CONFIRMED",
      "planet_probability": 0.901032,
      "candidate_probability": 0.0694371,
      "confidence_score": 0.901032,
      "confidence_level": "VERY_HIGH",
      "created_at": "2025-10-14T16:02:17",
      "light_curve_data": null
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 100
}
```

#### Example curl
```bash
# 전체 조회
curl -X GET "http://127.0.0.1:8000/api/v1/predictions/"

# 외계행성만 조회
curl -X GET "http://127.0.0.1:8000/api/v1/predictions/?is_exoplanet=true"

# 페이지네이션 (10개씩, 2번째 페이지)
curl -X GET "http://127.0.0.1:8000/api/v1/predictions/?skip=10&limit=10"
```

---

### 5. Get Single Prediction
**GET** `/api/v1/predictions/{prediction_id}`

ID로 특정 예측 결과를 조회합니다.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prediction_id` | string | required | 예측 ID (UUID) |

#### Response (200 OK)
```json
{
  "id": "5ef0383f-5520-4642-ad95-83d74ed1feb3",
  "is_exoplanet": true,
  "classification": "CONFIRMED",
  "planet_probability": 0.901032,
  "candidate_probability": 0.0694371,
  "confidence_score": 0.901032,
  "confidence_level": "VERY_HIGH",
  "created_at": "2025-10-14T16:16:30",
  "light_curve_data": null
}
```

#### Example curl
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/predictions/5ef0383f-5520-4642-ad95-83d74ed1feb3"
```

---

### 6. Delete Prediction
**DELETE** `/api/v1/predictions/{prediction_id}`

ID로 특정 예측 결과를 삭제합니다.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prediction_id` | string | required | 삭제할 예측 ID (UUID) |

#### Response (200 OK)
```json
{
  "message": "Successfully deleted prediction 5ef0383f-5520-4642-ad95-83d74ed1feb3",
  "deleted_count": 1
}
```

#### Example curl
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/predictions/5ef0383f-5520-4642-ad95-83d74ed1feb3"
```

---

### 7. Delete All Predictions
**DELETE** `/api/v1/predictions/`

모든 예측 결과를 삭제합니다. 필터를 사용하여 특정 결과만 삭제할 수 있습니다.

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_exoplanet` | boolean | optional | 외계행성 여부 필터 (true: 외계행성만 삭제, false: 비외계행성만 삭제, null: 전체 삭제) |

#### Response (200 OK)
```json
{
  "message": "Successfully deleted 5 predictions",
  "deleted_count": 5
}
```

#### Example curl
```bash
# 전체 삭제
curl -X DELETE "http://127.0.0.1:8000/api/v1/predictions/"

# 외계행성으로 예측된 결과만 삭제
curl -X DELETE "http://127.0.0.1:8000/api/v1/predictions/?is_exoplanet=true"

# 비외계행성 결과만 삭제
curl -X DELETE "http://127.0.0.1:8000/api/v1/predictions/?is_exoplanet=false"
```

---

## Error Responses

### 400 Bad Request
요청 데이터가 유효하지 않은 경우

```json
{
  "detail": "광도 곡선 데이터 또는 특징값이 필요합니다"
}
```

### 404 Not Found
리소스를 찾을 수 없는 경우

```json
{
  "detail": "예측 ID 5ef0383f-5520-4642-ad95-83d74ed1feb3를 찾을 수 없습니다"
}
```

### 500 Internal Server Error
서버 내부 오류

```json
{
  "detail": "예측 중 오류 발생: [error message]"
}
```

---

## Interactive Documentation

FastAPI는 자동으로 생성되는 대화형 API 문서를 제공합니다:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI Schema:** http://127.0.0.1:8000/openapi.json

---

## Test Examples

### Example 1: Typical Exoplanet (CONFIRMED)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predictions/" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "orbital_period": 3.5,
      "transit_duration": 2.5,
      "transit_depth": 500.0,
      "planet_radius": 2.0,
      "equilibrium_temp": 1200.0,
      "insolation": 100.0,
      "signal_to_noise": 50.0,
      "stellar_temp": 5800.0,
      "stellar_logg": 4.5,
      "stellar_radius": 1.0
    },
    "save_result": false
  }'
```
**Expected Result:** CONFIRMED (90.1% planet probability)

### Example 2: Hot Jupiter (FALSE_POSITIVE)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predictions/" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "orbital_period": 0.5,
      "transit_duration": 1.0,
      "transit_depth": 1000.0,
      "planet_radius": 12.0,
      "equilibrium_temp": 2000.0,
      "insolation": 1000.0,
      "signal_to_noise": 80.0,
      "stellar_temp": 6500.0,
      "stellar_logg": 4.0,
      "stellar_radius": 1.2
    },
    "save_result": false
  }'
```
**Expected Result:** FALSE_POSITIVE (66.7% false positive probability)

### Example 3: Earth Analog (FALSE_POSITIVE)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predictions/" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "orbital_period": 365.0,
      "transit_duration": 13.0,
      "transit_depth": 84.0,
      "planet_radius": 1.0,
      "equilibrium_temp": 288.0,
      "insolation": 1.0,
      "signal_to_noise": 15.0,
      "stellar_temp": 5778.0,
      "stellar_logg": 4.44,
      "stellar_radius": 1.0
    },
    "save_result": false
  }'
```
**Expected Result:** FALSE_POSITIVE (88.9% false positive probability)

### Example 4: Clear False Positive
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predictions/" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "orbital_period": 10.0,
      "transit_duration": 8.0,
      "transit_depth": 200.0,
      "planet_radius": 0.5,
      "equilibrium_temp": 800.0,
      "insolation": 50.0,
      "signal_to_noise": 5.0,
      "stellar_temp": 4500.0,
      "stellar_logg": 4.2,
      "stellar_radius": 0.8
    },
    "save_result": false
  }'
```
**Expected Result:** FALSE_POSITIVE (77.1% false positive probability)

---

## CORS Configuration

API는 CORS를 지원하며, 현재 모든 origin에서의 접근을 허용합니다:
```python
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

**Note:** 프로덕션 환경에서는 특정 도메인으로 제한하는 것을 권장합니다.

---

## Running the Server

### Development Mode
```bash
cd C:\Users\user\PycharmProjects\exovisions2\backend
python -m uvicorn app.presentation.main:app --host 127.0.0.1 --port 8000 --reload
```

### Production Mode
```bash
python -m uvicorn app.presentation.main:app --host 0.0.0.0 --port 8000
```

---

## Database

- **Type:** MySQL
- **Database Name:** `exoplanet_db`
- **Connection:**
  - Host: localhost
  - User: root
  - Password: 12345
  - Charset: utf8mb4

---

## Architecture

### Domain-Driven Design (DDD)
```
backend/
├── app/
│   ├── domain/              # 도메인 계층
│   │   ├── entities/        # 엔티티
│   │   ├── repositories/    # 리포지토리 인터페이스
│   │   ├── services/        # 도메인 서비스
│   │   └── value_objects/   # 값 객체
│   ├── application/         # 애플리케이션 계층
│   │   ├── dto/            # 데이터 전송 객체
│   │   └── use_cases/      # 유스케이스
│   ├── infrastructure/      # 인프라 계층
│   │   ├── database/       # 데이터베이스 구현
│   │   ├── ml/             # ML 모델 구현
│   │   └── repositories/   # 리포지토리 구현
│   └── presentation/        # 프레젠테이션 계층
│       ├── api/            # API 라우터
│       └── schemas/        # Pydantic 스키마
└── models/                  # 학습된 ML 모델 파일
```

---

## License
NASA Space Apps Challenge Project
