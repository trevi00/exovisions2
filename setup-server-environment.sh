#!/bin/bash
# Exoplanet Detection 서버 환경 설정 스크립트
# Ubuntu 22.04/20.04 기준

set -e

echo "=================================="
echo "서버 환경 설정 시작"
echo "=================================="

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 루트 권한 확인
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}이 스크립트는 root 권한으로 실행해야 합니다.${NC}"
    echo "sudo ./setup-server-environment.sh 로 실행해주세요."
    exit 1
fi

# 1. 시스템 업데이트
echo -e "${GREEN}[1/10] 시스템 업데이트 중...${NC}"
apt update && apt upgrade -y

# 2. 필수 패키지 설치
echo -e "${GREEN}[2/10] 필수 패키지 설치 중...${NC}"
apt install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    net-tools \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https \
    build-essential

# 3. Docker 설치
echo -e "${GREEN}[3/10] Docker 설치 중...${NC}"
if ! command -v docker &> /dev/null; then
    # Docker 공식 GPG 키 추가
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Docker 리포지토리 추가
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Docker 설치
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Docker 서비스 시작
    systemctl start docker
    systemctl enable docker

    echo -e "${GREEN}Docker 설치 완료: $(docker --version)${NC}"
else
    echo -e "${YELLOW}Docker가 이미 설치되어 있습니다: $(docker --version)${NC}"
fi

# 4. Docker Compose 설치 (standalone)
echo -e "${GREEN}[4/10] Docker Compose 설치 중...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}Docker Compose 설치 완료: $(docker-compose --version)${NC}"
else
    echo -e "${YELLOW}Docker Compose가 이미 설치되어 있습니다: $(docker-compose --version)${NC}"
fi

# 5. Python 3.11 설치
echo -e "${GREEN}[5/10] Python 설치 중...${NC}"
apt install -y python3.11 python3.11-venv python3-pip

# pip 업그레이드
python3 -m pip install --upgrade pip

echo -e "${GREEN}Python 설치 완료: $(python3 --version)${NC}"

# 6. Node.js 20 LTS 설치
echo -e "${GREEN}[6/10] Node.js 설치 중...${NC}"
if ! command -v node &> /dev/null; then
    # NodeSource 리포지토리 추가
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs

    echo -e "${GREEN}Node.js 설치 완료: $(node --version)${NC}"
    echo -e "${GREEN}npm 설치 완료: $(npm --version)${NC}"
else
    echo -e "${YELLOW}Node.js가 이미 설치되어 있습니다: $(node --version)${NC}"
fi

# 7. PostgreSQL 클라이언트 설치 (백업용)
echo -e "${GREEN}[7/10] PostgreSQL 클라이언트 설치 중...${NC}"
apt install -y postgresql-client

# 8. 방화벽 설정 (UFW)
echo -e "${GREEN}[8/10] 방화벽 설정 중...${NC}"
apt install -y ufw

# 기본 정책 설정
ufw default deny incoming
ufw default allow outgoing

# 필수 포트 열기
ufw allow 12345/tcp  # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS

# 방화벽 활성화
echo "y" | ufw enable

echo -e "${GREEN}방화벽 설정 완료${NC}"
ufw status

# 9. fail2ban 설치 (보안 강화)
echo -e "${GREEN}[9/10] fail2ban 설치 중...${NC}"
apt install -y fail2ban

# fail2ban 설정
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 12345
EOF

systemctl enable fail2ban
systemctl start fail2ban

# 10. 디렉토리 생성
echo -e "${GREEN}[10/10] 프로젝트 디렉토리 생성 중...${NC}"
mkdir -p /opt
mkdir -p /opt/backups

echo ""
echo "=================================="
echo -e "${GREEN}서버 환경 설정 완료!${NC}"
echo "=================================="
echo ""
echo "설치된 소프트웨어 버전:"
echo "  - Docker: $(docker --version)"
echo "  - Docker Compose: $(docker-compose --version)"
echo "  - Python: $(python3 --version)"
echo "  - Node.js: $(node --version)"
echo "  - npm: $(npm --version)"
echo "  - PostgreSQL Client: $(psql --version)"
echo ""
echo "방화벽 상태:"
ufw status
echo ""
echo "다음 단계:"
echo "  1. 프로젝트 클론:"
echo "     cd /opt"
echo "     git clone https://github.com/trevi00/exovisions2.git"
echo ""
echo "  2. 배포 스크립트 실행:"
echo "     cd /opt/exovisions2"
echo "     ./deploy.sh"
echo ""
echo "  3. SSL 설정:"
echo "     ./setup-ssl.sh"
echo ""
echo "  4. 백업 설정:"
echo "     ./setup-backup.sh"
echo ""
