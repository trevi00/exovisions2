#!/bin/bash
# Ubuntu 서버에 Claude Code 설치 스크립트

set -e

echo "=================================="
echo "Claude Code 설치 시작"
echo "=================================="

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 시스템 업데이트
echo -e "${GREEN}[1/5] 시스템 업데이트 중...${NC}"
sudo apt update

# curl 설치 확인
echo -e "${GREEN}[2/5] 필수 패키지 확인 중...${NC}"
sudo apt install -y curl ca-certificates

# Claude Code 설치
echo -e "${GREEN}[3/5] Claude Code 설치 중...${NC}"
curl -fsSL https://desktop-assets.static.getclaudeai.com/claude-code/install.sh | sudo bash

# 설치 확인
echo -e "${GREEN}[4/5] 설치 확인 중...${NC}"
if command -v claude &> /dev/null; then
    echo -e "${GREEN}Claude Code 버전: $(claude --version)${NC}"
else
    echo -e "${YELLOW}경고: claude 명령어를 찾을 수 없습니다. PATH를 확인하세요.${NC}"
    echo "다음 명령어를 실행해주세요:"
    echo "export PATH=\"\$HOME/.claude/bin:\$PATH\""
fi

# 프로젝트 디렉토리로 이동 가이드
echo -e "${GREEN}[5/5] 설정 완료${NC}"
echo ""
echo "=================================="
echo -e "${GREEN}Claude Code 설치 완료!${NC}"
echo "=================================="
echo ""
echo "다음 단계:"
echo "  1. 새 터미널을 열거나 다음 명령어 실행:"
echo "     export PATH=\"\$HOME/.claude/bin:\$PATH\""
echo ""
echo "  2. 프로젝트 디렉토리로 이동:"
echo "     cd /opt/exovisions2"
echo ""
echo "  3. Claude Code 시작:"
echo "     claude"
echo ""
echo "  4. Claude에게 배포 작업 요청:"
echo "     - deploy.sh 실행"
echo "     - Docker 상태 확인"
echo "     - 서비스 시작"
echo ""
