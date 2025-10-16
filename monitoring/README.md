# Monitoring Stack (Prometheus + Grafana)

## Quick Start

```bash
# Start
docker-compose -f docker-compose.monitoring.yml up -d

# Stop
docker-compose -f docker-compose.monitoring.yml down

# Logs
docker-compose -f docker-compose.monitoring.yml logs -f
```

## Access

- **Grafana**: http://localhost:3001 (admin / admin123)
- **Prometheus**: http://localhost:9090
- **API Metrics**: http://localhost:8000/metrics

## Dashboard

Grafana에 로그인 후 `Exoplanet Detection API Dashboard` 자동 로드됨

**주요 메트릭:**
- HTTP 요청 비율 (RPS)
- 레이턴시 (P50, P95, P99)
- 에러율
- 예측 API 성능
- Python GC 메트릭

## Configuration

### Prometheus Scrape 설정

```yaml
# monitoring/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'exoplanet-api'
    static_configs:
      - targets: ['host.docker.internal:8000']
    scrape_interval: 5s
```

### Grafana Provisioning

- Datasource: `monitoring/grafana/provisioning/datasources/prometheus.yml`
- Dashboard: `monitoring/grafana/dashboards/exoplanet-api-dashboard.json`

## Troubleshooting

**Prometheus가 API 메트릭을 못 가져올 때:**
```bash
# API 서버 확인
curl http://localhost:8000/metrics

# Prometheus 타겟 확인
curl http://localhost:9090/api/v1/targets
```

**Grafana 대시보드가 안 보일 때:**
```bash
# Grafana 재시작
docker-compose -f docker-compose.monitoring.yml restart grafana

# 또는 수동 임포트: Dashboards → Import → JSON 파일 업로드
```

**Windows에서 Node Exporter 에러:**
```bash
# 정상임 - Node Exporter는 Linux 전용
# Prometheus와 Grafana는 정상 작동
```

## Custom Metrics (Optional)

FastAPI 코드에 커스텀 메트릭 추가:

```python
from prometheus_client import Counter, Histogram

prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_duration_seconds', 'Prediction latency')

@app.post("/api/v1/predictions")
async def predict():
    with prediction_latency.time():
        prediction_counter.inc()
        # ... prediction logic
```

## Retention & Storage

기본 설정:
- **Retention**: 30일
- **Storage**: Docker volume (`prometheus-data`, `grafana-data`)

변경:
```yaml
# docker-compose.monitoring.yml
command:
  - '--storage.tsdb.retention.time=90d'  # 90일로 변경
```
