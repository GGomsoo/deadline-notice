# 📢 Notion Deadline Bot

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-API-000000?logo=notion&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-Webhook-5865F2?logo=discord&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?logo=githubactions&logoColor=white)

> 노션 채용 DB의 마감일 임박 공고를 디스코드로 자동 알림하는 봇

---

## 📌 목차

- [소개](#-소개)
- [프로젝트 구조](#-프로젝트-구조)
- [노션 DB 속성 구조](#-노션-db-속성-구조)
- [사전 준비](#-사전-준비)
- [설치 방법](#-설치-방법)
- [환경변수 설정](#-환경변수-설정)
- [실행 방법](#%EF%B8%8F-실행-방법)
- [자동화 설정](#%EF%B8%8F-자동화-설정-github-actions)
- [디스코드 알림 예시](#-디스코드-알림-예시)

---

## 🧩 소개

노션 데이터베이스에서 **마감일이 D-7 이내인 채용 공고**를 조회하여
매일 오전 9시에 디스코드 채널로 자동 알림을 전송합니다.

- 📅 마감일 기준 D-7 이내 공고 자동 감지
- 🎨 D-day 기준 색상 이모지 구분 (🔴 오늘 / 🟠 D-3 / 🟡 D-5 / 🟢 D-7)
- 🤖 GitHub Actions 으로 서버 없이 무료 자동화
- 🔗 기업명, 직무, 경력, 플랫폼, 링크 정보 포함

---

## 📁 프로젝트 구조

```
notion-deadline-bot/
├── .github/
│   └── workflows/
│       └── notify.yml        ← GitHub Actions 자동화
├── .venv/                    ← 가상환경 (git 제외)
├── .env                      ← API 키 (git 제외)
├── .gitignore
├── notion_client.py          ← 노션 API 연동 (DB 조회 + 파싱)
├── discord_client.py         ← 디스코드 Webhook 연동
├── notify.py                 ← 메인 실행 파일
├── requirements.txt          ← 패키지 목록
└── README.md
```

---

## 🗂 노션 DB 속성 구조

| 속성명 | 타입 |
|---|---|
| 기업명 | title |
| 직무 | text |
| 산업 구분 | select |
| 기업형태 | select |
| 경력 | select |
| 마감일 | date |
| 서류 | select |
| 면접 | select |
| 플랫폼 | select |
| 링크 | url |

---

## 🛠 사전 준비

### 1. 노션 API 키 발급

1. [노션 개발자 콘솔](https://www.notion.so/my-integrations) 접속
2. **"+ New integration"** 클릭 → 이름 입력 → Submit
3. **"Internal Integration Secret"** 복사
4. 노션 DB 우측 상단 `...` → **"연결(Connections)"** → 생성한 integration 추가

> ⚠️ 4번 연결 단계를 빠뜨리면 API 호출 시 `invalid_request_url` 에러 발생

### 2. 노션 DB ID 확인

노션 DB를 전체 화면으로 열었을 때 브라우저 URL에서 확인합니다.

```
https://www.notion.so/워크스페이스명/[DATABASE_ID]?v=...
                                     ↑ 이 부분
```

### 3. 디스코드 Webhook URL 발급

1. 알림 받을 채널 우클릭 → **"채널 편집"**
2. **"연동"** 탭 → **"웹후크 만들기"**
3. **"웹후크 URL 복사"**

> 📌 참고: [디스코드 Webhook 공식 가이드](https://support.discord.com/hc/ko/articles/228383668)

---

## 💻 설치 방법

**사전 요구사항:** Python 3.8 이상

```bash
# 저장소 클론
git clone https://github.com/본인아이디/notion-deadline-bot.git
cd notion-deadline-bot

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\Activate.ps1

# 패키지 설치
pip install -r requirements.txt

# 가상환경 비활성화
deactivate
```

---

## 🔑 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 입력합니다.

```
NOTION_API_KEY=secret_xxxxxxxxxxxx
NOTION_DEADLINE_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy
DAYS_BEFORE=7
```

| 변수명 | 설명 | 발급 방법 |
|---|---|---|
| `NOTION_API_KEY` | 노션 Integration 키 | [노션 개발자 콘솔](https://www.notion.so/my-integrations) |
| `NOTION_DEADLINE_DATABASE_ID` | 대상 DB ID | 노션 DB URL에서 추출 |
| `DISCORD_WEBHOOK_URL` | 디스코드 Webhook URL | 채널 설정 → 연동 |
| `DAYS_BEFORE` | 알림 기준 D-N (기본값: 7) | 직접 설정 |

---

## ▶️ 실행 방법

```bash
# 로컬에서 직접 실행
python notify.py
```

**실행 결과:**

```
[1/3] 노션 DB 조회 중... (마감 D-7 이내)
      → 2건 조회됨

[2/3] 데이터 파싱 중...
      → 파싱 완료

[3/3] 디스코드 알림 전송 중...
✅ 디스코드 전송 완료 (파트 1/1, 348자)

✅ 모든 작업 완료!
```

---

## ⚙️ 자동화 설정 (GitHub Actions)

### 1. GitHub Secrets 등록

GitHub 저장소 **Settings → Secrets and variables → Actions → New repository secret** 에서 아래 4개 등록합니다.

| Name | Value |
|---|---|
| `NOTION_API_KEY` | 노션 API 키 |
| `NOTION_DEADLINE_DATABASE_ID` | 노션 DB ID |
| `DISCORD_WEBHOOK_URL` | 디스코드 Webhook URL |
| `DAYS_BEFORE` | `7` |

### 2. workflow 파일 구조

`.github/workflows/notify.yml` 파일이 아래 흐름으로 실행됩니다.

```
매일 오전 8시 (KST)
      ↓
GitHub 서버 (ubuntu-latest) 실행
      ↓
Python 3.11 설치
      ↓
pip install -r requirements.txt
      ↓
python notify.py
      ↓
디스코드 알림 전송 완료
```

### 3. 수동 실행

**Actions 탭 → Notion Deadline Notifier → Run workflow** 버튼으로 즉시 테스트 가능합니다.

> 💡 **cron 표현식 참고:** https://crontab.guru

---

## 💬 디스코드 알림 예시

```
📢 마감 임박 공고 알림 | 2026년 02월 22일
━━━━━━━━━━━━━━━━━━━━━━
총 3건

🔴 오늘 마감! | 2026-02-22
> 🏢 테스트기업 A (스타트업 / IT)
> 💼 직무: 백엔드 개발자
> 👤 경력: 신입
> 🖥️ 플랫폼: 원티드
> 🔗 https://www.wanted.co.kr/...
────────────────────
🟠 D-5 | 2026-02-27
> 🏢 테스트기업 B (중소기업 / 금융)
> 💼 직무: 프론트엔드 개발자
> 👤 경력: 경력
> 🖥️ 플랫폼: 사람인
> 🔗 https://www.saramin.co.kr/...
────────────────────
🟢 D-7 | 2026-03-01
> 🏢 테스트기업 C (대기업 / 제조)
> 💼 직무: 데이터 엔지니어
> 👤 경력: 신입
> 🖥️ 플랫폼: 자사 홈페이지
> 🔗 https://careers.testcompany.com/...
────────────────────
```

---

## 📚 참고 문서

| 문서 | 링크 |
|---|---|
| 노션 API 공식 문서 | https://developers.notion.com/reference/intro |
| 노션 Database Query | https://developers.notion.com/reference/post-database-query |
| 노션 Date Filter | https://developers.notion.com/reference/database-query-filter#date |
| 디스코드 Webhook 공식 문서 | https://discord.com/developers/docs/resources/webhook#execute-webhook |
| 디스코드 Webhook 한국어 가이드 | https://support.discord.com/hc/ko/articles/228383668 |
| GitHub Actions 공식 문서 | https://docs.github.com/ko/actions |
| cron 표현식 생성기 | https://crontab.guru |
