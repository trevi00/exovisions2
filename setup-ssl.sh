#!/bin/bash
# SSL/HTTPS 자동 설정 스크립트 (Let's Encrypt)

set -e

echo "=================================="
echo "SSL/HTTPS 설정 시작"
echo "=================================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Nginx 설치
echo -e "${GREEN}[1/5] Nginx 설치 중...${NC}"
apt update
apt install -y nginx

# Certbot 설치
echo -e "${GREEN}[2/5] Certbot 설치 중...${NC}"
apt install -y certbot python3-certbot-nginx

# Nginx 설정
echo -e "${GREEN}[3/5] Nginx 리버스 프록시 설정 중...${NC}"
cat > /etc/nginx/sites-available/exovisions2 << 'EOF'
server {
    listen 80;
    server_name exovisions2.shop www.exovisions2.shop;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Metrics
    location /metrics {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Nginx 설정 활성화
ln -sf /etc/nginx/sites-available/exovisions2 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Nginx 설정 테스트
nginx -t

# Nginx 재시작
systemctl restart nginx

# SSL 인증서 발급
echo -e "${GREEN}[4/5] SSL 인증서 발급 중...${NC}"
echo -e "${YELLOW}이메일 주소를 입력하세요:${NC}"
read EMAIL

certbot --nginx -d exovisions2.shop -d www.exovisions2.shop \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    --redirect

# 자동 갱신 설정
echo -e "${GREEN}[5/5] 자동 갱신 설정 중...${NC}"
systemctl enable certbot.timer
systemctl start certbot.timer

echo ""
echo "=================================="
echo -e "${GREEN}SSL 설정 완료!${NC}"
echo "=================================="
echo ""
echo "접속 주소:"
echo "  https://exovisions2.shop (자동으로 HTTPS로 리다이렉트됨)"
echo ""
echo "SSL 인증서는 자동으로 갱신됩니다."
echo "갱신 테스트: certbot renew --dry-run"
echo ""
