# 가비아클라우드 배포 가이드

## 배포 전략

### Option 1: Docker Compose 단일 서버 배포 (권장 - 중소규모)

**장점:**
- 설정 간단, 비용 효율적
- 빠른 배포 및 관리 용이
- 중소규모 트래픽 처리 가능

**권장 서버 사양:**
- CPU: 4 vCPU 이상
- RAM: 8GB 이상
- Storage: SSD 50GB 이상
- OS: Ubuntu 22.04 LTS

### Option 2: Kubernetes 클러스터 (고급 - 대규모)

**장점:**
- 고가용성, 자동 확장
- 무중단 배포
- 대규모 트래픽 처리

**필요 서버:**
- Master Node: 2 vCPU, 4GB RAM (최소 1대, 권장 3대)
- Worker Node: 4 vCPU, 8GB RAM (최소 2대)

---

## Option 1: Docker Compose 배포 (권장)

### 1. 가비아클라우드 서버 생성

1. [가비아클라우드](https://www.gabiacloud.com) 접속
2. g클라우드 → 가상서버 선택
3. 서버 스펙 설정:
   ```
   OS: Ubuntu 22.04 LTS
   타입: SSD 서버
   CPU: 4 vCPU
   RAM: 8GB
   Storage: 50GB
   ```
4. 방화벽 설정:
   ```
   포트 80 (HTTP) 허용
   포트 443 (HTTPS) 허용
   포트 22 (SSH) 허용
   ```

### 2. 서버 초기 설정

```bash
# SSH 접속
ssh root@YOUR_SERVER_IP

# 시스템 업데이트
apt update && apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Compose 설치
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 설치 확인
docker --version
docker-compose --version

# Git 설치
apt install -y git
```

### 3. 프로젝트 배포

```bash
# 프로젝트 클론
cd /opt
git clone https://github.com/YOUR_USERNAME/exovisions2.git
cd exovisions2

# 환경 변수 설정
cp .env.example .env
nano .env
```

**`.env` 파일 수정:**
```bash
# Database
POSTGRES_PASSWORD=STRONG_PASSWORD_HERE  # 강력한 비밀번호로 변경

# Backend
DEBUG=False
ALLOWED_ORIGINS=http://YOUR_DOMAIN.com,http://YOUR_SERVER_IP

# Monitoring
GRAFANA_ADMIN_PASSWORD=STRONG_PASSWORD_HERE  # 강력한 비밀번호로 변경
```

### 4. 서비스 시작

```bash
# 전체 스택 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 상태 확인
docker-compose ps
```

### 5. 방화벽 설정 (Ubuntu UFW)

```bash
# UFW 활성화
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable

# 상태 확인
ufw status
```

### 6. 도메인 연결

1. 가비아 도메인 관리 → DNS 설정
2. A 레코드 추가:
   ```
   호스트: @
   타입: A
   값: YOUR_SERVER_IP
   TTL: 3600
   ```

### 7. SSL/HTTPS 설정 (Let's Encrypt)

```bash
# Certbot 설치
apt install -y certbot python3-certbot-nginx

# Nginx 설치 (리버스 프록시용)
apt install -y nginx

# Nginx 설정
cat > /etc/nginx/sites-available/exoplanet << 'EOF'
server {
    listen 80;
    server_name YOUR_DOMAIN.com www.YOUR_DOMAIN.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# 설정 활성화
ln -s /etc/nginx/sites-available/exoplanet /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# SSL 인증서 발급
certbot --nginx -d YOUR_DOMAIN.com -d www.YOUR_DOMAIN.com
```

### 8. 자동 백업 설정

```bash
# 백업 스크립트 생성
cat > /opt/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/opt/backups
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 데이터베이스 백업
docker-compose exec -T database pg_dump -U exoplanet exoplanet_db > $BACKUP_DIR/db_$DATE.sql

# 오래된 백업 삭제 (7일 이상)
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete

echo "Backup completed: db_$DATE.sql"
EOF

chmod +x /opt/backup.sh

# 크론탭 설정 (매일 새벽 3시 백업)
crontab -e
# 다음 라인 추가:
# 0 3 * * * /opt/backup.sh >> /var/log/backup.log 2>&1
```

### 9. 모니터링 접속

- **Frontend**: http://YOUR_DOMAIN.com
- **Backend API**: http://YOUR_DOMAIN.com/api/v1
- **API Docs**: http://YOUR_DOMAIN.com/docs
- **Grafana**: http://YOUR_SERVER_IP:3001 (admin / admin123)
- **Prometheus**: http://YOUR_SERVER_IP:9090

---

## Option 2: Kubernetes 클러스터 배포

### 1. 서버 준비

**Master Node x 1 (최소):**
- Ubuntu 22.04 LTS
- 2 vCPU, 4GB RAM, 50GB SSD

**Worker Node x 2 (최소):**
- Ubuntu 22.04 LTS
- 4 vCPU, 8GB RAM, 50GB SSD

### 2. 모든 노드에서 실행

```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Kubernetes 패키지 저장소 추가
apt-get update
apt-get install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list

# Kubernetes 설치
apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

# Swap 비활성화
swapoff -a
sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

### 3. Master Node에서 클러스터 초기화

```bash
# 클러스터 초기화
kubeadm init --pod-network-cidr=10.244.0.0/16

# kubectl 설정
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

# CNI (Calico) 설치
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml

# Join 명령어 저장 (Worker Node 조인용)
kubeadm token create --print-join-command > /root/join-command.txt
```

### 4. Worker Node에서 클러스터 조인

```bash
# Master Node의 join-command.txt 내용 실행
kubeadm join MASTER_IP:6443 --token TOKEN --discovery-token-ca-cert-hash sha256:HASH
```

### 5. Nginx Ingress Controller 설치

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml
```

### 6. 프로젝트 배포

로컬에서:
```bash
# GitHub username 수정
cd exovisions2
sed -i 's/YOUR_GITHUB_USERNAME/your-username/g' k8s/*.yaml

# Git에 커밋 및 푸시
git add k8s/
git commit -m "Update K8s manifests for Gabia Cloud"
git push origin main
```

서버에서:
```bash
# 프로젝트 클론
git clone https://github.com/YOUR_USERNAME/exovisions2.git
cd exovisions2

# Secret 설정 (DB 비밀번호)
echo -n "your-db-password" | base64
# 출력값을 k8s/secrets.yaml에 업데이트

# 배포
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/database-statefulset.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# 배포 확인
kubectl get all -n exoplanet
kubectl get ingress -n exoplanet
```

---

## 유지보수

### 로그 확인

**Docker Compose:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Kubernetes:**
```bash
kubectl logs -f deployment/backend -n exoplanet
kubectl logs -f deployment/frontend -n exoplanet
```

### 업데이트 배포

**Docker Compose:**
```bash
cd /opt/exovisions2
git pull origin main
docker-compose pull
docker-compose up -d
```

**Kubernetes:**
```bash
git pull origin main
kubectl apply -f k8s/
```

### 리소스 모니터링

```bash
# 시스템 리소스
htop
df -h

# Docker
docker stats

# Kubernetes
kubectl top nodes
kubectl top pods -n exoplanet
```

---

## 트러블슈팅

### 메모리 부족

```bash
# Swap 추가 (임시 조치)
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# 영구 적용
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### 포트 충돌

```bash
# 포트 사용 확인
netstat -tulpn | grep :8000

# 프로세스 종료
kill -9 PID
```

### 디스크 공간 부족

```bash
# Docker 정리
docker system prune -a --volumes

# 로그 파일 정리
journalctl --vacuum-time=7d
```

---

## 비용 최적화

### 가비아클라우드 요금제

**소규모 (Docker Compose):**
- 4 vCPU, 8GB RAM, 50GB SSD
- 예상 비용: 월 약 50,000원

**중규모 (Kubernetes 3노드):**
- Master 1대 + Worker 2대
- 예상 비용: 월 약 150,000원

### 절감 팁

1. **리소스 최적화**: `docker-compose.yml`에서 필요없는 서비스 제거
2. **이미지 최적화**: Multi-stage build 활용 (이미 적용됨)
3. **로그 로테이션**: 오래된 로그 자동 삭제
4. **모니터링 최적화**: Prometheus retention 기간 조정

---

## 보안 체크리스트

- [ ] 강력한 DB 비밀번호 설정
- [ ] Grafana admin 비밀번호 변경
- [ ] SSH 키 인증 사용 (비밀번호 인증 비활성화)
- [ ] UFW 방화벽 활성화
- [ ] SSL/HTTPS 적용
- [ ] 정기 백업 설정
- [ ] 시스템 업데이트 자동화
- [ ] fail2ban 설치 (무차별 대입 공격 방지)

```bash
# fail2ban 설치
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

---

## 다음 단계

1. 서버 생성 및 초기 설정
2. Docker Compose로 배포
3. 도메인 연결 및 SSL 설정
4. 모니터링 확인
5. 백업 설정
6. 부하 테스트

배포 완료 후 Grafana 대시보드에서 실시간 모니터링 가능합니다!
