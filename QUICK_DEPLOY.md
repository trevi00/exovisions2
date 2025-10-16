# 가비아클라우드 빠른 배포 가이드

## 서버 정보
- **IP**: 1.201.19.192
- **SSH 포트**: 12345
- **도메인**: exovisions2.shop

---

## 1단계: 도메인 DNS 설정 (먼저 해야 함!)

### 가비아 도메인 관리 페이지에서:

1. [가비아 로그인](https://www.gabia.com) → My가비아 → 서비스 관리
2. exovisions2.shop 선택 → DNS 정보 → DNS 설정
3. **A 레코드 추가/수정**:
   ```
   호스트명: @
   타입: A
   값/위치: 1.201.19.192
   TTL: 3600
   ```
4. **www A 레코드 추가**:
   ```
   호스트명: www
   타입: A
   값/위치: 1.201.19.192
   TTL: 3600
   ```
5. 저장

**DNS 전파 대기 (5-30분):**
```bash
# Windows에서 확인
nslookup exovisions2.shop

# 1.201.19.192가 표시되면 완료
```

---

## 2단계: 서버 접속

### Windows에서 PuTTY 또는 PowerShell 사용:

```powershell
# PowerShell (Windows 10/11)
ssh root@1.201.19.192 -p 12345

# 비밀번호 입력
```

### Mac/Linux에서:
```bash
ssh root@1.201.19.192 -p 12345
```

---

## 3단계: 자동 배포 스크립트 실행

서버에 접속한 후:

```bash
# 배포 스크립트 다운로드 및 실행
curl -fsSL https://raw.githubusercontent.com/trevi00/exovisions2/master/deploy.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
```

**스크립트 실행 중 입력 사항:**
1. GitHub Repository URL: `https://github.com/trevi00/exovisions2.git`
2. 데이터베이스 비밀번호: (강력한 비밀번호 입력)
3. Grafana 관리자 비밀번호: (강력한 비밀번호 입력)

---

## 4단계: SSL/HTTPS 설정

```bash
chmod +x /opt/exovisions2/setup-ssl.sh
/opt/exovisions2/setup-ssl.sh
```

**입력 사항:**
- 이메일 주소: (SSL 인증서 관리용)

---

## 5단계: 자동 백업 설정

```bash
chmod +x /opt/exovisions2/setup-backup.sh
/opt/exovisions2/setup-backup.sh
```

---

## 6단계: 배포 확인

### 웹 브라우저에서 접속:

- **Frontend**: https://exovisions2.shop
- **API Docs**: https://exovisions2.shop/docs
- **Grafana**: http://1.201.19.192:3001

### 서버에서 확인:
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f

# 서비스 응답 테스트
curl http://localhost:8000/
curl http://localhost:3000/
```

---

## 수동 배포 (자동 스크립트 없이)

### 1. 시스템 준비
```bash
# 서버 접속
ssh root@1.201.19.192 -p 12345

# 시스템 업데이트
apt update && apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com | sh

# Docker Compose 설치
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 방화벽 설정
ufw allow 12345/tcp  # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw --force enable
```

### 2. 프로젝트 설치
```bash
# 프로젝트 클론
cd /opt
git clone https://github.com/trevi00/exovisions2.git
cd exovisions2

# 환경 변수 설정
cp .env.example .env
nano .env
```

**.env 파일 수정:**
```bash
POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD
GRAFANA_ADMIN_PASSWORD=YOUR_ADMIN_PASSWORD
DEBUG=False
ALLOWED_ORIGINS=https://exovisions2.shop,http://exovisions2.shop,http://1.201.19.192
```

### 3. 서비스 시작
```bash
docker-compose up -d
```

### 4. SSL 설정 (Nginx + Let's Encrypt)
```bash
# Nginx 설치
apt install -y nginx certbot python3-certbot-nginx

# Nginx 설정
cat > /etc/nginx/sites-available/exovisions2 << 'EOF'
server {
    listen 80;
    server_name exovisions2.shop www.exovisions2.shop;

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

    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
EOF

# 설정 활성화
ln -s /etc/nginx/sites-available/exovisions2 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# SSL 인증서 발급
certbot --nginx -d exovisions2.shop -d www.exovisions2.shop --email YOUR_EMAIL --agree-tos --redirect
```

---

## 관리 명령어

### 서비스 관리
```bash
# 서비스 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart backend

# 서비스 중지
docker-compose stop

# 서비스 시작
docker-compose start

# 전체 중지 및 삭제
docker-compose down
```

### 로그 확인
```bash
# 전체 로그
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### 업데이트 배포
```bash
cd /opt/exovisions2
git pull origin main
docker-compose pull
docker-compose up -d
```

### 백업
```bash
# 수동 백업
/opt/exovisions2/scripts/backup.sh

# 백업 파일 확인
ls -lh /opt/backups/
```

### 리소스 모니터링
```bash
# 시스템 리소스
htop
df -h

# Docker 컨테이너 리소스
docker stats
```

---

## 트러블슈팅

### 컨테이너가 시작되지 않을 때
```bash
# 로그 확인
docker-compose logs backend

# 컨테이너 재빌드
docker-compose build --no-cache
docker-compose up -d
```

### 포트 충돌
```bash
# 포트 사용 확인
netstat -tulpn | grep :8000

# 프로세스 종료
kill -9 PID
```

### SSL 인증서 갱신
```bash
# 갱신 테스트
certbot renew --dry-run

# 강제 갱신
certbot renew
```

### 디스크 공간 부족
```bash
# Docker 정리
docker system prune -a --volumes

# 로그 정리
journalctl --vacuum-time=7d
```

---

## 성능 최적화

### Docker Compose 리소스 제한
`docker-compose.yml`에 추가:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
```

### Nginx 캐싱
`/etc/nginx/sites-available/exovisions2`에 추가:
```nginx
# 정적 파일 캐싱
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

## 보안 강화

### SSH 키 인증 설정
```bash
# 로컬에서 SSH 키 생성 (이미 있다면 skip)
ssh-keygen -t rsa -b 4096

# 공개 키를 서버에 복사
ssh-copy-id -p 12345 root@1.201.19.192

# 서버에서 비밀번호 인증 비활성화
nano /etc/ssh/sshd_config
# PasswordAuthentication no 로 변경
systemctl restart sshd
```

### fail2ban 설치
```bash
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

---

## 접속 정보 요약

| 서비스 | URL | 계정 정보 |
|--------|-----|-----------|
| Frontend | https://exovisions2.shop | - |
| Backend API | https://exovisions2.shop/api/v1 | - |
| API Docs | https://exovisions2.shop/docs | - |
| Grafana | http://1.201.19.192:3001 | admin / (설정한 비밀번호) |
| Prometheus | http://1.201.19.192:9090 | - |
| SSH | ssh root@1.201.19.192 -p 12345 | root 비밀번호 |

---

## 다음 단계

- [ ] DNS 설정 완료
- [ ] 서버 접속 확인
- [ ] 자동 배포 스크립트 실행
- [ ] SSL/HTTPS 설정
- [ ] 백업 설정
- [ ] 서비스 동작 확인
- [ ] Grafana 대시보드 확인
- [ ] 부하 테스트
- [ ] 모니터링 알림 설정

배포 완료 후 문제가 있으면 로그를 확인하고 필요시 지원 요청하세요!
