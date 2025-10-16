#!/bin/bash
# Exoplanet Detection - 가비아클라우드 자동 배포 스크립트

set -e  # 에러 발생 시 중단

echo "=================================="
echo "Exoplanet Detection 배포 시작"
echo "=================================="

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 시스템 업데이트
echo -e "${GREEN}[1/10] 시스템 업데이트 중...${NC}"
apt update && apt upgrade -y

# 필수 패키지 설치
echo -e "${GREEN}[2/10] 필수 패키지 설치 중...${NC}"
apt install -y git curl wget vim ufw fail2ban

# Docker 설치
echo -e "${GREEN}[3/10] Docker 설치 중...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "Docker가 이미 설치되어 있습니다."
fi

# Docker Compose 설치
echo -e "${GREEN}[4/10] Docker Compose 설치 중...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose가 이미 설치되어 있습니다."
fi

# 방화벽 설정
echo -e "${GREEN}[5/10] 방화벽 설정 중...${NC}"
ufw --force enable
ufw allow 12345/tcp  # SSH 포트
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw reload

# 프로젝트 디렉토리 생성 및 이동
echo -e "${GREEN}[6/10] 프로젝트 준비 중...${NC}"
mkdir -p /opt
cd /opt

# 기존 프로젝트 백업 (있다면)
if [ -d "exovisions2" ]; then
    echo -e "${YELLOW}기존 프로젝트 발견. 백업 중...${NC}"
    mv exovisions2 exovisions2_backup_$(date +%Y%m%d_%H%M%S)
fi

# 프로젝트 클론
echo -e "${GREEN}[7/10] GitHub에서 프로젝트 다운로드 중...${NC}"
REPO_URL="https://github.com/trevi00/exovisions2.git"
echo "Repository: $REPO_URL"
git clone $REPO_URL

cd exovisions2

# 환경 변수 설정
echo -e "${GREEN}[8/10] 환경 변수 설정 중...${NC}"
cp .env.example .env

echo -e "${YELLOW}데이터베이스 비밀번호를 입력하세요:${NC}"
read -s DB_PASSWORD
echo ""

echo -e "${YELLOW}Grafana 관리자 비밀번호를 입력하세요:${NC}"
read -s GRAFANA_PASSWORD
echo ""

# .env 파일 업데이트
sed -i "s/POSTGRES_PASSWORD=change_me_in_production/POSTGRES_PASSWORD=$DB_PASSWORD/g" .env
sed -i "s/GRAFANA_ADMIN_PASSWORD=admin123/GRAFANA_ADMIN_PASSWORD=$GRAFANA_PASSWORD/g" .env
sed -i "s/DEBUG=False/DEBUG=False/g" .env
sed -i "s/ALLOWED_ORIGINS=.*/ALLOWED_ORIGINS=https:\/\/exovisions2.shop,http:\/\/exovisions2.shop,http:\/\/1.201.19.192/g" .env

# Docker Compose 시작
echo -e "${GREEN}[9/10] Docker 컨테이너 시작 중...${NC}"
docker-compose up -d

# 서비스 상태 확인
echo -e "${GREEN}[10/10] 서비스 상태 확인 중...${NC}"
sleep 10
docker-compose ps

echo ""
echo "=================================="
echo -e "${GREEN}배포 완료!${NC}"
echo "=================================="
echo ""
echo "접속 정보:"
echo "  Frontend: http://exovisions2.shop"
echo "  Backend API: http://exovisions2.shop:8000"
echo "  API Docs: http://exovisions2.shop:8000/docs"
echo "  Grafana: http://1.201.19.192:3001"
echo ""
echo "다음 단계:"
echo "  1. 도메인 DNS 설정 (A 레코드: 1.201.19.192)"
echo "  2. SSL 인증서 설치 (./setup-ssl.sh 실행)"
echo "  3. 백업 설정 (./setup-backup.sh 실행)"
echo ""
echo "로그 확인: docker-compose logs -f"
echo "서비스 재시작: docker-compose restart"
echo "서비스 중지: docker-compose down"
echo ""
