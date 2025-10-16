# 필요한 키/토큰 목록

## 필수 항목

### 1. 데이터베이스 비밀번호
**설정 위치:** `.env` 파일
```bash
POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD_HERE
```
**생성 방법:**
```bash
# 강력한 비밀번호 생성 (Linux/Mac)
openssl rand -base64 32

# Windows PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

### 2. Grafana Admin 비밀번호
**설정 위치:** `.env` 파일
```bash
GRAFANA_ADMIN_PASSWORD=YOUR_ADMIN_PASSWORD_HERE
```
**기본값:** admin123 (반드시 변경 필요!)

---

## 선택 항목 (GitHub Actions 사용 시)

### 3. GitHub Personal Access Token (선택)
**사용 목적:** Private 저장소에서 Docker 이미지를 빌드할 때만 필요
**기본 설정:** GitHub Actions는 `GITHUB_TOKEN`을 자동 제공하므로 추가 설정 불필요

**Public 저장소 사용 시:**
- 추가 설정 불필요 (자동 처리됨)

**Private 저장소 사용 시:**
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Scopes 선택:
   - `repo` (전체 저장소 접근)
   - `write:packages` (GHCR 푸시)
   - `read:packages` (GHCR 읽기)
4. 생성된 토큰 복사
5. Repository Settings → Secrets → New repository secret
   - Name: `GH_PAT`
   - Value: 복사한 토큰

---

## 선택 항목 (프로덕션 권장)

### 4. SSL/TLS 인증서 (Let's Encrypt 자동 발급)
**사용 목적:** HTTPS 적용
**설정 방법:** 가비아 배포 가이드의 "SSL/HTTPS 설정" 섹션 참조

**필요 정보:**
- 도메인 이름
- 이메일 주소

### 5. 도메인
**사용 목적:** 사용자 친화적 접속 주소
**구매처:** 가비아 또는 다른 도메인 등록 업체
**설정:** DNS A 레코드로 서버 IP 연결

---

## 향후 확장 시 필요할 수 있는 것들

### 6. Sentry DSN (에러 모니터링 - 선택)
**사용 목적:** 프로덕션 에러 추적
**설정 위치:** `.env` 파일
```bash
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

**발급 방법:**
1. [Sentry](https://sentry.io) 회원가입
2. 프로젝트 생성
3. DSN 복사
4. `.env`에 추가

### 7. Email SMTP 설정 (알림 발송 - 선택)
**사용 목적:** 시스템 알림, 비밀번호 재설정 등
**설정 위치:** `.env` 파일
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Gmail 사용 시:**
1. Google 계정 → 보안 → 2단계 인증 활성화
2. 앱 비밀번호 생성
3. 생성된 비밀번호를 `SMTP_PASSWORD`에 입력

### 8. NASA API Key (선택)
**사용 목적:** NASA 데이터 가져오기 (현재 미사용)
**설정 위치:** `.env` 파일
```bash
NASA_API_KEY=your-nasa-api-key
```

**발급 방법:**
1. [NASA API](https://api.nasa.gov) 접속
2. API Key 신청
3. 이메일로 받은 키 입력

---

## 가비아클라우드 배포 시 설정 순서

### 1단계: 필수 환경 변수 설정

```bash
# 서버에 접속 후
cd /opt/exovisions2
cp .env.example .env
nano .env
```

**.env 파일 최소 설정:**
```bash
# Database
POSTGRES_DB=exoplanet_db
POSTGRES_USER=exoplanet
POSTGRES_PASSWORD=CHANGE_ME_TO_STRONG_PASSWORD  # 강력한 비밀번호로 변경

# Backend
DEBUG=False
ALLOWED_ORIGINS=http://YOUR_DOMAIN.com,http://YOUR_SERVER_IP

# Monitoring
GRAFANA_ADMIN_PASSWORD=CHANGE_ME_TO_STRONG_PASSWORD  # 강력한 비밀번호로 변경
```

### 2단계: Docker Compose 시작
```bash
docker-compose up -d
```

### 3단계: 서비스 확인
```bash
# 로그 확인
docker-compose logs -f

# 서비스 상태 확인
docker-compose ps
```

---

## 보안 체크리스트

- [ ] DB 비밀번호를 강력하게 설정했는가?
- [ ] Grafana admin 비밀번호를 변경했는가?
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는가?
- [ ] 프로덕션에서 `DEBUG=False`로 설정했는가?
- [ ] HTTPS (SSL/TLS)를 적용했는가?
- [ ] 방화벽 (UFW)을 활성화했는가?
- [ ] 정기 백업을 설정했는가?

---

## 현재 프로젝트에서 사용하는 환경 변수 전체 목록

### Backend
```bash
# 데이터베이스
DATABASE_URL=postgresql://user:password@host:port/dbname

# 애플리케이션
DEBUG=False
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000

# ML 모델 (자동 설정)
MODEL_PATH=/app/models/exoplanet_multiclass_model.pkl
SCALER_PATH=/app/models/scaler.pkl
```

### Frontend
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Monitoring
```bash
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin123
```

---

## 요약

**필수 설정 (배포 전):**
1. ✅ DB 비밀번호
2. ✅ Grafana Admin 비밀번호

**선택 설정 (권장):**
1. ⭐ 도메인 (사용자 경험 향상)
2. ⭐ SSL/TLS (보안 강화)

**향후 확장 시:**
1. Sentry (에러 모니터링)
2. Email SMTP (알림)
3. NASA API (데이터 확장)

**현재 프로젝트는 외부 API 키 없이도 정상 작동합니다!**
