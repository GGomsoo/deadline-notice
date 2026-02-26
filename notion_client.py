import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# .env에 작성한 key value 호출
load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DEADLINE_DATABASE_ID = os.getenv("NOTION_DEADLINE_DATABASE_ID")
DAYS_BEFORE = int(os.getenv("DAYS_BEFORE", 3))

# NOTION DB에서 오늘 ~ D+3 이내 마감인 항목 조회
def get_upcoming_deadlines():
    url = f'https://api.notion.com/v1/databases/{NOTION_DEADLINE_DATABASE_ID}/query'

    # headers 양식은 notion api 레퍼런스에서 제공
    # notion 버전은 고정값이다. 2022-06-28
    # 2025-09-03 version에선 error가 발생한다.
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    today = datetime.now(timezone.utc).date()
    deadline = today + timedelta(days=DAYS_BEFORE)

    payload = {
        "filter": {
            "and": [
                {
                    "property": "마감일",
                    "date": { "on_or_after": today.isoformat()}
                },
                {
                    "property": "마감일",
                    "date": { "on_or_before": deadline.isoformat()}
                }
            ]
        },
        "sorts": [
            {
                "property": "마감일",
                "direction": "ascending"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"노션 api 오류 [{response.status_code}]\n{response.text}")
    return response.json().get("results", [])

def parse_item(item):
    props = item["properties"]
    
    def get_title(key):
        arr = props.get(key, {}).get("title", [])
        return arr[0]["plain_text"] if arr else "없음"
    
    def get_rich_text(key):
        arr = props.get(key, {}).get("rich_text", [])
        return arr[0]["plain_text"] if arr else "없음"

    def get_select(key):
        sel = props.get(key, {}).get("select")
        return sel["name"] if sel else "없음"

    def get_date(key):
        date_val = props.get(key, {}).get("date")
        return date_val["start"] if date_val else None

    def get_url(key):
        return props.get(key, {}).get("url")
    
    # 마감일까지 남은 날 계산
    deadline_str = get_date("마감일")
    if deadline_str:
        deadline_dt = datetime.fromisoformat(deadline_str)
        deadline_date = deadline_dt.date()
        days_left = (deadline_date - datetime.now(timezone.utc).date()).days
        display_deadline = deadline_dt.strftime("%Y-%m-%d %H:%M")
    else:
        days_left = None
        display_deadline = "없음"

    return {
        "기업명": get_title("기업명"),
        "직무": get_rich_text("직무"),
        "산업구분": get_select("산업 구분"),
        "기업형태": get_select("기업형태"),
        "경력": get_select("경력"),
        "마감일": display_deadline or "없음",
        "D_day": days_left,
        "플랫폼": get_select("플랫폼"),
        "링크": get_url("링크"),
    }

if __name__ == "__main__":
    print(f"노션 DB 조회중... (마감 D-{DAYS_BEFORE} 이내)")

    items = get_upcoming_deadlines()
    print(f"총 {len(items)}건 조회됨")

    for item in items:
        parsed = parse_item(item)
        print("-" * 40)
        for key, value in parsed.items():
            print(f"{key:8} : {value}")
    print("-" * 40)