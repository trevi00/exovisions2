"""
MySQL 데이터베이스 생성 스크립트
"""
import pymysql
import sys

try:
    # MySQL 연결 (root 계정)
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='12345',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    print("MySQL에 성공적으로 연결되었습니다.")

    with connection.cursor() as cursor:
        # 데이터베이스 생성
        cursor.execute("CREATE DATABASE IF NOT EXISTS exoplanet_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("exoplanet_db 데이터베이스가 생성되었습니다.")

        # 데이터베이스 목록 확인
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("\n현재 데이터베이스 목록:")
        for db in databases:
            print(f"  - {db['Database']}")

    connection.close()
    print("\n데이터베이스 생성 완료!")

except pymysql.err.OperationalError as e:
    print(f"MySQL 연결 실패: {e}")
    print("\n가능한 원인:")
    print("  1. MySQL 서버가 실행 중이 아닙니다")
    print("  2. root 비밀번호가 '12345'가 아닙니다")
    print("  3. 네트워크/방화벽 설정 문제")
    sys.exit(1)

except Exception as e:
    print(f"오류 발생: {e}")
    sys.exit(1)
