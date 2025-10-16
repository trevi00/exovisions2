#!/bin/bash
# 자동 백업 설정 스크립트

set -e

echo "=================================="
echo "자동 백업 설정 시작"
echo "=================================="

GREEN='\033[0;32m'
NC='\033[0m'

# 백업 디렉토리 생성
echo -e "${GREEN}[1/3] 백업 디렉토리 생성 중...${NC}"
mkdir -p /opt/backups
mkdir -p /opt/exovisions2/scripts

# 백업 스크립트 생성
echo -e "${GREEN}[2/3] 백업 스크립트 생성 중...${NC}"
cat > /opt/exovisions2/scripts/backup.sh << 'EOF'
#!/bin/bash
# 데이터베이스 백업 스크립트

BACKUP_DIR=/opt/backups
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR=/opt/exovisions2

# 백업 디렉토리 확인
mkdir -p $BACKUP_DIR

# 데이터베이스 백업
echo "데이터베이스 백업 중..."
cd $PROJECT_DIR
docker-compose exec -T database pg_dump -U exoplanet exoplanet_db > $BACKUP_DIR/db_$DATE.sql

# 압축
gzip $BACKUP_DIR/db_$DATE.sql

# 7일 이상 된 백업 삭제
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete

echo "백업 완료: db_$DATE.sql.gz"
echo "저장 위치: $BACKUP_DIR"
EOF

chmod +x /opt/exovisions2/scripts/backup.sh

# 크론탭 설정
echo -e "${GREEN}[3/3] 자동 백업 스케줄 설정 중...${NC}"
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/exovisions2/scripts/backup.sh >> /var/log/exoplanet-backup.log 2>&1") | crontab -

echo ""
echo "=================================="
echo -e "${GREEN}자동 백업 설정 완료!${NC}"
echo "=================================="
echo ""
echo "백업 정보:"
echo "  백업 시간: 매일 새벽 3시"
echo "  백업 위치: /opt/backups"
echo "  보관 기간: 7일"
echo "  로그 파일: /var/log/exoplanet-backup.log"
echo ""
echo "수동 백업 실행:"
echo "  /opt/exovisions2/scripts/backup.sh"
echo ""
echo "백업 파일 복원:"
echo "  gunzip /opt/backups/db_YYYYMMDD_HHMMSS.sql.gz"
echo "  docker-compose exec -T database psql -U exoplanet exoplanet_db < db_YYYYMMDD_HHMMSS.sql"
echo ""
