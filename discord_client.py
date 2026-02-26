import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def build_message(items: list) -> str:
    # 파싱된 NOTION 데이터를 DISCORD 메시지 문자열로 전환
    # DISCORD MARKDOWN
    # **텍스트** : 굵게
    # > 텍스트 : 인용 블록 (들여쓰기)
    # ----- : 구분선

    today_str = datetime.now().strftime("%Y년 %m월 %d일")
    lines = [
        f"📢 **마감 임박 공고 알림** | {today_str}",
        f"━━━━━━━━━━━━━━━━━━━━━━",
        f"**총 {len(items)}건**\n",
    ]

    for item in items:
        d = item["D_day"]

        # D-day 기준 색상 이모지 구분
        if d == 0:
            d_label = "🔴 **오늘 마감!**"
        elif d == 1:
            d_label = "🟠 **D-1**"
        elif d == 2:
            d_label = "🟡 **D-2**"
        else:
            d_label = f"🟢 **D-{d}**"

        link_line = f"\n> 🔗 {item['링크']}" if item["링크"] else ""

        block = (
            f"{d_label} | {item['마감일']}\n"
            f"> 🏢 **{item['기업명']}** ({item['기업형태']} / {item['산업구분']})\n"
            f"> 💼 직무: {item['직무']}\n"
            f"> 👤 경력: {item['경력']}\n"
            f"> 🖥️ 플랫폼: {item['플랫폼']}"
            f"{link_line}\n"
            f"────────────────────"
        )
        lines.append(block)
    
    return "\n".join(lines)

def send_discord(items: list):
    if not items:
        print("마감 임박 항목 없음 -> 디스코드 알림 생략")
        return
    
    # DISCORD 메시지 최대 길이 = 2000자
    # 2000자 초과 시 분할 처리
    full_message = build_message(items)

    chunks, current = [], ""
    for line in full_message.split("\n"):
        if len(current) + len(line) + 1 > 1900:
            chunks.append(current)
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current)
    
    for i, chunk in enumerate(chunks, 1):
        payload = {"content": chunk}
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        # 성공: 200 또는 204
        if res.status_code not in (200, 204):
            raise Exception(f"디스코드 전송 실패 [{res.status_code}]\n{res.text}")

        print(f"✅ 디스코드 전송 완료 (파트 {i}/{len(chunks)}, {len(chunk)}자)")

# 테스트용 더미 데이터
if __name__ == "__main__":
    dummy_items = [
            {
                "기업명":   "테스트 기업 A",
                "직무":     "백엔드 개발자",
                "산업구분": "IT",
                "기업형태": "스타트업",
                "경력":     "신입, 경력",
                "마감일":   "2025-01-15",
                "D_day":    0,
                "플랫폼":   "원티드",
                "링크":     "https://wanted.co.kr",
            },
            {
                "기업명":   "테스트 기업 B",
                "직무":     "프론트엔드 개발자",
                "산업구분": "IT",
                "기업형태": "대기업",
                "경력":     "경력",
                "마감일":   "2025-01-17",
                "D_day":    2,
                "플랫폼":   "잡코리아",
                "링크":     None,
            },
        ]

    send_discord(dummy_items)