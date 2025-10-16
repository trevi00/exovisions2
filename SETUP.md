# Exovisions 프로젝트 설정 가이드

이 문서는 Exovisions 프로젝트의 환경 설정 방법을 설명합니다.

## 📋 목차
- [백엔드 설정](#백엔드-설정)
- [프론트엔드 설정](#프론트엔드-설정)
- [환경변수 설명](#환경변수-설명)

---

## 🔧 백엔드 설정

### 1. 환경변수 파일 생성

백엔드 디렉토리에서 `.env` 파일을 생성합니다:

```bash
cd backend
cp .env.example .env
```

### 2. `.env` 파일 수정

필요에 따라 데이터베이스 및 서버 설정을 수정합니다:

```env
# 데이터베이스 설정
DATABASE_URL=mysql+pymysql://root:12345@localhost:3306/exoplanet_db?charset=utf8mb4
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=exoplanet_db

# 서버 설정
HOST=0.0.0.0
PORT=8000

# CORS 설정 (콤마로 구분된 도메인 목록)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19006,http://127.0.0.1:3000

# 애플리케이션 설정
DEBUG=True  # 개발 모드에서는 True, 프로덕션에서는 False
LOG_LEVEL=INFO

# ML 모델 설정
MODEL_PATH=./exoplanet_multiclass_model.pkl
```

### 3. 데이터베이스 준비

MySQL 데이터베이스를 생성합니다:

```sql
CREATE DATABASE exoplanet_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 백엔드 실행

```bash
# 가상환경 활성화 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
cd app/presentation
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.
- API 문서: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📱 프론트엔드 설정

### 1. 환경 설정 확인

프론트엔드는 `src/config/environment.js` 파일에서 환경 설정을 관리합니다.

개발 환경과 프로덕션 환경이 자동으로 구분됩니다:

```javascript
const ENV = {
  development: {
    apiUrl: 'http://127.0.0.1:8000/api/v1',  // 개발 서버 URL
    apiTimeout: 30000,
    debug: true,
  },
  production: {
    apiUrl: process.env.API_URL || 'https://api.exovisions.com/api/v1',  // 프로덕션 서버 URL
    apiTimeout: 30000,
    debug: false,
  },
};
```

### 2. 프로덕션 환경 설정 (선택사항)

프로덕션 빌드 시 API URL을 변경하려면 환경변수를 설정합니다:

```bash
# Linux/Mac
export API_URL=https://your-production-api.com/api/v1

# Windows
set API_URL=https://your-production-api.com/api/v1
```

### 3. 프론트엔드 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

Expo 개발 서버가 실행되고, 다음 옵션으로 앱을 실행할 수 있습니다:
- `w`: 웹 브라우저에서 실행
- `a`: Android 에뮬레이터/디바이스에서 실행
- `i`: iOS 시뮬레이터에서 실행

---

## 📖 환경변수 설명

### 백엔드 환경변수

| 변수명 | 설명 | 기본값 | 필수 |
|--------|------|--------|------|
| `DATABASE_URL` | 전체 데이터베이스 연결 URL | - | 선택 |
| `DB_HOST` | 데이터베이스 호스트 | localhost | 선택 |
| `DB_PORT` | 데이터베이스 포트 | 3306 | 선택 |
| `DB_USER` | 데이터베이스 사용자 | root | 선택 |
| `DB_PASSWORD` | 데이터베이스 비밀번호 | 12345 | **필수** |
| `DB_NAME` | 데이터베이스 이름 | exoplanet_db | 선택 |
| `HOST` | 서버 호스트 | 0.0.0.0 | 선택 |
| `PORT` | 서버 포트 | 8000 | 선택 |
| `ALLOWED_ORIGINS` | CORS 허용 도메인 (콤마 구분) | localhost:3000,localhost:19006 | 선택 |
| `DEBUG` | 디버그 모드 (True/False) | False | 선택 |
| `LOG_LEVEL` | 로그 레벨 | INFO | 선택 |
| `MODEL_PATH` | ML 모델 파일 경로 | ./exoplanet_multiclass_model.pkl | 선택 |

### 프론트엔드 환경변수

| 변수명 | 설명 | 기본값 | 적용 환경 |
|--------|------|--------|----------|
| `API_URL` | API 서버 URL | http://127.0.0.1:8000/api/v1 (dev)<br>https://api.exovisions.com/api/v1 (prod) | 프로덕션 |

---

## 🔐 보안 주의사항

1. **절대로 `.env` 파일을 Git에 커밋하지 마세요!**
   - `.env` 파일은 `.gitignore`에 포함되어 있습니다.
   - 대신 `.env.example` 파일을 템플릿으로 사용하세요.

2. **프로덕션 환경에서는 반드시 강력한 비밀번호를 사용하세요.**

3. **CORS 설정을 프로덕션에서는 특정 도메인으로 제한하세요.**

4. **DEBUG 모드를 프로덕션에서는 False로 설정하세요.**

---

## 🚀 빠른 시작

### 전체 프로젝트 실행 (개발 모드)

```bash
# 1. 백엔드 실행 (터미널 1)
cd backend
python app/presentation/main.py

# 2. 프론트엔드 실행 (터미널 2)
cd frontend
npm start
```

### 테스트 확인

1. 브라우저에서 http://localhost:19006 접속
2. API 문서 확인: http://localhost:8000/docs
3. 앱에서 예측 기능 테스트

---

## 📝 추가 정보

- **API 문서**: 백엔드 서버 실행 후 `/docs` 엔드포인트 참조
- **문제 해결**: 이슈가 발생하면 GitHub Issues에 보고해주세요
- **기여**: Pull Request를 환영합니다!

