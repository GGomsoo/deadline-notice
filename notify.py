from notion_client import get_upcoming_deadlines, parse_item
from discord_client import send_discord
import os
from dotenv import load_dotenv

load_dotenv()
DAYS_BEFORE = int(os.getenv("DAYS_BEFORE", 3))

def main():
    print(f"[1/3] 노션 DB 조회 중... (마감 D-{DAYS_BEFORE} 이내)")
    raw_items = get_upcoming_deadlines()
    print(f"      → {len(raw_items)}건 조회됨\n")

    print("[2/3] 데이터 파싱 중...")
    parsed_items = [parse_item(item) for item in raw_items]
    print(f"      → 파싱 완료\n")

    print("[3/3] 디스코드 알림 전송 중...")
    send_discord(parsed_items)
    print("\n✅ 모든 작업 완료!")

if __name__ == "__main__":
    main()