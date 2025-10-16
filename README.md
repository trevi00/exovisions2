# 🌌 ExoVisions - NASA Space Apps Challenge 2024

> AI-powered Exoplanet Detection System with Real-time Monitoring

외계행성 탐지 머신러닝 시스템 - NASA Kepler, TESS, K2 데이터 기반

## 🚀 프로젝트 소개

ExoVisions는 NASA의 Kepler, TESS, K2 망원경 데이터를 활용하여 외계행성을 탐지하는 머신러닝 기반 시스템입니다.

### 핵심 특징

- **73.98% 정확도**: Optuna 최적화된 5-모델 스태킹 앙상블
- **실시간 모니터링**: Prometheus + Grafana 통합
- **프로덕션 배포 준비**: Docker Compose + CI/CD 파이프라인
- **크로스 플랫폼**: Web, iOS, Android 지원

## 🛠 기술 스택

### Backend
- FastAPI 0.104+, PostgreSQL 15
- ML: scikit-learn, XGBoost, LightGBM, CatBoost, Optuna
- Monitoring: Prometheus, Grafana

### Frontend
- React Native Web
- Recharts, React Navigation

### Infrastructure
- Docker, Docker Compose
- GitHub Actions CI/CD
- GHCR (GitHub Container Registry)

## 🚀 빠른 시작

### 1. 환경 준비

```bash
git clone https://github.com/your-username/exovisions2.git
cd exovisions2
cp .env.example .env
```

### 2. Docker Compose로 시작

```bash
docker-compose up -d
```

### 3. 서비스 접속

| 서비스 | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Grafana | http://localhost:3001 (admin/admin123) |
| Prometheus | http://localhost:9090 |

## 📦 배포

자세한 내용은 [DEPLOYMENT.md](./DEPLOYMENT.md)를 참조하세요.

## 📊 모니터링

Grafana Dashboard: http://localhost:3001
- HTTP 요청 비율, 지연시간 (P50/P95/P99)
- 에러율, Python GC 메트릭
- 12개 모니터링 패널

## 📄 라이선스

MIT License - see [LICENSE](LICENSE) file

## 🙏 감사의 말

- NASA: Kepler, TESS, K2 데이터
- Space Apps Challenge 2024

**Made with ❤️ for NASA Space Apps Challenge 2024**
