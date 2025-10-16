# Exoplanet Detection API - 배포 가이드

NASA Space Apps Challenge 외계행성 탐지 ML 애플리케이션 배포 가이드입니다.

## 📋 목차

- [시스템 요구사항](#시스템-요구사항)
- [로컬 개발 환경](#로컬-개발-환경)
- [Docker Compose 배포](#docker-compose-배포)
- [프로덕션 배포](#프로덕션-배포)
- [CI/CD 파이프라인](#cicd-파이프라인)
- [모니터링 설정](#모니터링-설정)
- [트러블슈팅](#트러블슈팅)

---

## 시스템 요구사항

### 최소 사양
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 10GB
- **OS**: Linux, macOS, Windows (with WSL2)

### 권장 사양
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 20GB

### 필수 소프트웨어
- Docker 24.0+
- Docker Compose 2.20+
- Git 2.30+
- (선택) Node.js 18+ (로컬 개발)
- (선택) Python 3.11+ (로컬 개발)

---

## 로컬 개발 환경

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/exovisions2.git
cd exovisions2
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (필요한 값 설정)
# nano .env 또는 vim .env
```

### 3. 백엔드 로컬 실행

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화
python -c "from app.infrastructure.database import init_db; init_db()"

# 서버 실행
python -m uvicorn app.presentation.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 프론트엔드 로컬 실행

```bash
cd frontend

# 의존성 설치
npm install --legacy-peer-deps

# 개발 서버 실행
npm start
```

---

## Docker Compose 배포

### 전체 스택 배포 (추천)

```bash
# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 프로덕션 값 설정

# 전체 스택 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 상태 확인
docker-compose ps
```

### 개별 서비스 관리

```bash
# 특정 서비스만 시작
docker-compose up -d backend frontend

# 특정 서비스 재시작
docker-compose restart backend

# 특정 서비스 중지
docker-compose stop grafana

# 전체 스택 중지 및 삭제
docker-compose down

# 볼륨까지 삭제 (데이터 완전 삭제)
docker-compose down -v
```

### 서비스 접속 정보

| 서비스 | URL | 설명 |
|--------|-----|------|
| Frontend | http://localhost:3000 | React Native Web UI |
| Backend API | http://localhost:8000 | FastAPI REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Prometheus | http://localhost:9090 | 메트릭 수집 |
| Grafana | http://localhost:3001 | 모니터링 대시보드 |
| PostgreSQL | localhost:5432 | 데이터베이스 |

---

## 프로덕션 배포

### AWS ECS 배포 예시

#### 1. Docker 이미지 빌드 및 푸시

```bash
# AWS ECR 로그인
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# 백엔드 이미지 빌드 및 푸시
docker build -t exoplanet-backend:latest ./backend
docker tag exoplanet-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/exoplanet-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/exoplanet-backend:latest

# 프론트엔드 이미지 빌드 및 푸시
docker build -t exoplanet-frontend:latest ./frontend
docker tag exoplanet-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/exoplanet-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/exoplanet-frontend:latest
```

#### 2. ECS Task Definition 예시

```json
{
  "family": "exoplanet-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/exoplanet-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:pass@rds-endpoint:5432/exoplanet_db"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/ || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

### Google Cloud Run 배포 예시

```bash
# gcloud CLI로 배포
gcloud run deploy exoplanet-backend \
  --image gcr.io/PROJECT_ID/exoplanet-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="postgresql://..."

gcloud run deploy exoplanet-frontend \
  --image gcr.io/PROJECT_ID/exoplanet-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Kubernetes + ArgoCD 배포 (권장)

GitOps 기반 자동 배포를 위한 ArgoCD 사용:

#### 1. ArgoCD 설치

```bash
# ArgoCD 설치
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# ArgoCD 접속 (포트포워드)
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 초기 비밀번호 확인
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

#### 2. Nginx Ingress Controller 설치

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

#### 3. ArgoCD Application 배포

```bash
# argocd/application.yaml에서 GitHub username 수정
sed -i 's/YOUR_GITHUB_USERNAME/your-username/g' argocd/application.yaml

# ArgoCD Application 생성
kubectl apply -f argocd/application.yaml

# 배포 확인
kubectl get application -n argocd
kubectl get all -n exoplanet
```

자세한 내용은 `argocd/README.md` 참조

### kubectl로 직접 배포 (개발용)

```bash
# Kubernetes 매니페스트 적용
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/database-statefulset.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# 상태 확인
kubectl get pods -n exoplanet
kubectl get ingress -n exoplanet
```

자세한 내용은 `k8s/README.md` 참조

---

## CI/CD 파이프라인

### GitHub Actions + ArgoCD GitOps

자동화된 CI/CD 파이프라인:
1. GitHub Actions: 빌드, 테스트, Docker 이미지 생성
2. ArgoCD: Kubernetes 배포 자동화

#### 1. GitHub Secrets 설정

Repository Settings → Secrets and variables → Actions:

- `GITHUB_TOKEN`: 자동 제공 (추가 설정 불필요)
- Docker 이미지는 GitHub Container Registry (GHCR)에 자동 푸시

#### 2. CI/CD 워크플로우

```bash
# main 브랜치에 푸시하면 자동 실행
git add .
git commit -m "feat: new feature"
git push origin main

# GitHub Actions 자동 실행:
# 1. Backend/Frontend 테스트
# 2. Security 스캔 (Trivy)
# 3. Docker 이미지 빌드 및 GHCR 푸시
# 4. K8s 매니페스트 업데이트 (image tag)
# 5. 변경사항 Git 커밋

# ArgoCD 자동 실행:
# 1. Git 변경사항 감지
# 2. Kubernetes 클러스터에 배포
# 3. Health check 및 동기화
```

#### 3. 배포 모니터링

**GitHub Actions:**
- GitHub → Actions 탭에서 워크플로우 확인
- 빌드, 테스트, 이미지 푸시 상태 확인

**ArgoCD:**
```bash
# ArgoCD UI 접속
kubectl port-forward svc/argocd-server -n argocd 8080:443
# https://localhost:8080

# CLI로 확인
argocd app get exoplanet-detection
argocd app sync exoplanet-detection --watch
```

#### 4. 롤백

```bash
# Git을 통한 롤백 (GitOps)
git revert HEAD
git push origin main
# ArgoCD가 자동으로 이전 상태로 복구

# ArgoCD를 통한 즉시 롤백
argocd app rollback exoplanet-detection
```

---

## 모니터링 설정

### Prometheus + Grafana

모니터링 스택은 기본 docker-compose에 포함되어 있습니다.

```bash
# 모니터링만 시작
docker-compose -f docker-compose.monitoring.yml up -d

# Grafana 접속
# URL: http://localhost:3001
# Username: admin
# Password: admin123 (변경 권장)
```

### 커스텀 메트릭 추가

```python
# backend/app/presentation/main.py
from prometheus_client import Counter, Histogram

# 커스텀 카운터
prediction_counter = Counter(
    'exoplanet_predictions_total',
    'Total number of predictions made',
    ['classification']
)

# 사용 예시
prediction_counter.labels(classification='CONFIRMED').inc()
```

### 알림 설정

```yaml
# monitoring/prometheus/alerts.yml
groups:
  - name: exoplanet_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
```

---

## 트러블슈팅

### 문제: 컨테이너가 시작되지 않음

```bash
# 로그 확인
docker-compose logs backend

# 컨테이너 상태 확인
docker ps -a

# 이미지 재빌드
docker-compose build --no-cache backend
docker-compose up -d backend
```

### 문제: 데이터베이스 연결 실패

```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose ps database

# PostgreSQL 로그 확인
docker-compose logs database

# 수동 연결 테스트
docker-compose exec database psql -U exoplanet -d exoplanet_db
```

### 문제: 프론트엔드가 백엔드 API에 연결 못함

1. `.env` 파일에서 `REACT_APP_API_URL` 확인
2. 백엔드의 CORS 설정 확인 (`ALLOWED_ORIGINS`)
3. 네트워크 연결 확인:
   ```bash
   docker network inspect exovisions2_exoplanet-network
   ```

### 문제: ML 모델 로딩 실패

```bash
# 모델 파일 존재 확인
docker-compose exec backend ls -la /app/models/

# 모델 파일 권한 확인
docker-compose exec backend stat /app/models/exoplanet_multiclass_model.pkl

# 모델 파일 복사 (호스트 → 컨테이너)
docker cp backend/models/exoplanet_multiclass_model.pkl exoplanet-backend:/app/models/
```

### 문제: 메모리 부족

```bash
# Docker 메모리 한도 증가
# docker-compose.yml에 추가:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 4G
```

---

## 백업 및 복구

### 데이터베이스 백업

```bash
# 백업 생성
docker-compose exec database pg_dump -U exoplanet exoplanet_db > backup_$(date +%Y%m%d).sql

# 백업 복원
cat backup_20241016.sql | docker-compose exec -T database psql -U exoplanet -d exoplanet_db
```

### 볼륨 백업

```bash
# 전체 볼륨 백업
docker run --rm -v exovisions2_postgres-data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz /data

# 복원
docker run --rm -v exovisions2_postgres-data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres-backup.tar.gz -C /
```

---

## 성능 최적화

### 1. 데이터베이스 최적화

```sql
-- PostgreSQL 인덱스 추가
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
CREATE INDEX idx_predictions_classification ON predictions(classification);
```

### 2. API 캐싱

```python
# Redis 캐싱 추가
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="exoplanet-cache")
```

### 3. 프론트엔드 빌드 최적화

```bash
# Production 빌드 최적화
npm run build -- --prod --optimization
```

---

## 보안 권장사항

1. **환경 변수 보호**: `.env` 파일을 Git에 커밋하지 마세요
2. **비밀번호 변경**: 기본 비밀번호 (admin123, change_me_in_production) 변경
3. **HTTPS 사용**: 프로덕션에서는 반드시 SSL/TLS 인증서 설정
4. **방화벽 설정**: 필요한 포트만 열기
5. **정기 업데이트**: Docker 이미지 및 의존성 정기 업데이트

---

## 지원 및 문의

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/exovisions2/issues)
- **문서**: [README.md](./README.md)
- **모니터링 가이드**: [monitoring/README.md](./monitoring/README.md)

---

## 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
