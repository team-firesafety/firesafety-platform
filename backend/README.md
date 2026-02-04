# Backend - 소담 플랫폼

FastAPI 기반 소방 안전 플랫폼 백엔드 API

## 📋 개요

소담 플랫폼의 백엔드는 FastAPI를 사용하여 구축된 RESTful API 서버입니다. OpenAI GPT-4o를 활용하여 자연어 질의를 처리하고, PostgreSQL 데이터베이스에서 한글 컬럼명으로 소방 데이터를 조회하며, RAG 기술로 지식 기반 대화를 제공합니다.

## 🏗️ 프로젝트 구조

```
backend/
├── app/
│   ├── main.py                    # FastAPI 애플리케이션 진입점
│   ├── config.py                  # 환경 변수 설정
│   ├── api/
│   │   ├── router.py              # API 라우터 통합
│   │   └── endpoints/
│   │       ├── chat.py            # /chat 엔드포인트 (메인 AI 라우팅)
│   │       ├── pdf_download.py   # PDF 다운로드 엔드포인트
│   │       └── fire_patrol.py    # 순찰 데이터 엔드포인트
│   ├── core/
│   │   ├── constants.py           # 상수 정의
│   │   ├── function_setup.py      # AI 함수 호출 설정
│   │   └── visualization_database.py  # DB 연결 관리
│   ├── services/
│   │   ├── function_caller.py     # GPT 기반 기능 라우팅
│   │   ├── features.py            # 4개 핵심 기능 구현
│   │   ├── visualization_ai_service.py       # 자연어 → SQL 변환
│   │   ├── visualization_query_service.py    # SQL 실행 및 데이터 처리
│   │   ├── visualization_metadata_service.py # 차트 메타데이터 생성
│   │   ├── column_mapping_service.py         # 한글 컬럼명 매핑
│   │   ├── rag_chat.py            # RAG 기반 대화
│   │   ├── fire_risk.py           # 화재 위험도 예측
│   │   ├── building_service.py    # 건물 정보 조회
│   │   ├── patrol_service.py      # 순찰 데이터 서비스
│   │   └── vworld.py              # VWorld API 연동
│   ├── schemas/
│   │   ├── chat_request.py        # 요청 스키마
│   │   ├── chat_response.py       # 응답 스키마
│   │   ├── building.py            # 건물 스키마
│   │   └── visualization_schemas.py  # 시각화 데이터 스키마
│   └── models/
│       └── visualization_models.py   # SQLAlchemy 모델
├── migrations/
│   └── visualization_schema.sql   # PostgreSQL 스키마 (한글 컬럼명)
├── scripts/
│   └── build_vectorstore.py       # FAISS 벡터스토어 구축 스크립트
├── data/
│   ├── fire_safety_data/          # 소방 CSV 데이터
│   └── 상세정보_화재안전기술_상세정보.csv  # RAG 지식베이스
├── data_loader.py                 # CSV → PostgreSQL 데이터 로더
├── requirements.txt               # Python 의존성
└── .env                          # 환경 변수 (gitignore)
```

## 🛠️ 기술 스택

- **FastAPI 0.116** - 고성능 비동기 웹 프레임워크
- **PostgreSQL** - 한글 컬럼명 사용 관계형 데이터베이스
- **SQLAlchemy 2.0** - Python ORM
- **OpenAI GPT-4o** - 자연어 처리 및 SQL 생성
- **LangChain 0.3** - RAG 파이프라인 구축
- **FAISS** - 벡터 검색 라이브러리
- **Pandas 2.3** - 데이터 처리 및 분석
- **Pydantic 2.11** - 데이터 검증
- **ReportLab** - PDF 생성

## 🚀 시작하기

### 사전 요구사항
- Python 3.9+
- PostgreSQL 14+
- OpenAI API Key
- VWorld API Key (지도 기능용, 선택)

### 1. 가상환경 설정

```bash
cd backend

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`backend/.env` 파일 생성:

```env
# PostgreSQL 연결 정보
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/fire_safety_db

# OpenAI API 설정
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o

# VWorld API (지도 기능용)
VWORLD_KEY=your_vworld_api_key_here
```

### 4. 데이터베이스 초기화

```bash
# 데이터베이스 생성
psql -U YOUR_USERNAME -c "CREATE DATABASE fire_safety_db;"

# 스키마 마이그레이션 (한글 컬럼명 테이블 생성)
psql -U YOUR_USERNAME -d fire_safety_db -f migrations/visualization_schema.sql
```

### 5. 데이터 로드

```bash
# CSV 데이터를 PostgreSQL로 로드
# ⚠️ data_loader.py의 DB_CONFIG에서 사용자명 수정 필요
python data_loader.py
```

### 6. RAG 벡터스토어 구축

```bash
# 프로젝트 루트에서 실행
python -m backend.scripts.build_vectorstore
```

`backend/vectorstore_FAISS/` 디렉토리에 `index.faiss`와 `index.pkl` 생성됨

### 7. 서버 실행

```bash
# 개발 서버 (자동 재시작)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 서버
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. API 문서 접속

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/ping

## 📡 API 엔드포인트

### POST /chat
모든 AI 기능의 통합 엔드포인트. GPT-4o가 사용자 질의를 분석하여 자동으로 적절한 기능을 호출합니다.

**요청:**
```json
{
  "query": "2024년 강남구 화재 건수를 그래프로 보여줘"
}
```

**응답:**
```json
{
  "functionNo": 1,
  "data": {
    "success": true,
    "generated_sql": "SELECT ...",
    "data": [...],
    "columns_metadata": {...},
    "chart_recommendations": [...]
  }
}
```

#### functionNo 매핑
- **1**: 데이터 시각화
- **2**: 문서 생성
- **3**: 화재 위험 예측
- **4**: 일반 대화 (RAG)

### GET /pdf/download
생성된 문서를 PDF로 다운로드

**응답:** `application/pdf`

### POST /patrol/*
화재 위험 예측 관련 순찰 데이터 조회

## 🧠 핵심 아키텍처

### 1. Function Routing System

`services/function_caller.py`에서 구현된 AI 기반 라우팅:

```python
async def call_function_by_query(query: str) -> dict:
    """
    GPT-4o가 사용자 질의를 분석하여 functionNo를 결정
    """
    # GPT-4o에게 질의 분류 요청
    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": FUNCTION_ROUTING_PROMPT},
            {"role": "user", "content": query}
        ],
        tools=[...]  # 4개 기능 정의
    )

    # functionNo에 따라 적절한 서비스 호출
    if function_no == 1:
        return await visualization_service(query)
    elif function_no == 2:
        return await document_service(query)
    # ...
```

### 2. 한글 컬럼명 시스템

`services/column_mapping_service.py`에서 관리:

```python
COLUMN_MAPPINGS = {
    "seoul_fire_dispatch": {
        "사망자수": {"english": "deaths", "type": "numeric"},
        "부상자수": {"english": "injuries", "type": "numeric"},
        "재산피해액": {"english": "property_damage", "type": "numeric"},
        "발생장소": {"english": "location", "type": "categorical"},
        # ...
    }
}
```

### 3. 자연어 to SQL

`services/visualization_ai_service.py`:

```python
async def generate_sql_from_query(query: str, table_name: str) -> str:
    """
    자연어 질의를 한글 컬럼명 기반 SQL로 변환
    """
    # 테이블 스키마 정보 가져오기
    schema_info = get_table_schema(table_name)

    # GPT-4o에게 SQL 생성 요청
    prompt = f"""
    한글 컬럼명을 사용하는 PostgreSQL 테이블입니다.
    테이블: {table_name}
    컬럼: {schema_info}

    질의: {query}

    SQL을 생성하세요.
    """

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return extract_sql(response)
```

### 4. 차트 메타데이터 생성

`services/visualization_metadata_service.py`:

```python
def generate_chart_metadata(data: List[dict], table_name: str) -> dict:
    """
    데이터와 컬럼 정보를 분석하여 차트 추천 정보 생성
    """
    columns_metadata = {}

    for column in data[0].keys():
        column_info = get_column_info(table_name, column)
        columns_metadata[column] = {
            "type": column_info["type"],  # numeric, categorical, date
            "chart_usage": get_chart_usage(column_info["type"]),
            "unit": column_info.get("unit", "")
        }

    chart_recommendations = generate_recommendations(columns_metadata)

    return {
        "columns_metadata": columns_metadata,
        "chart_recommendations": chart_recommendations
    }
```

### 5. RAG (Retrieval-Augmented Generation)

`services/rag_chat.py`:

```python
async def rag_chat(query: str) -> str:
    """
    FAISS 벡터스토어에서 관련 문서 검색 후 GPT-4o로 답변 생성
    """
    # 벡터스토어 로드
    vectorstore = FAISS.load_local("vectorstore_FAISS/", embeddings)

    # 관련 문서 검색
    docs = vectorstore.similarity_search(query, k=3)

    # 컨텍스트와 함께 GPT-4o에게 답변 요청
    context = "\n\n".join([doc.page_content for doc in docs])
    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "소방 안전 전문가로 답변하세요."},
            {"role": "user", "content": f"컨텍스트:\n{context}\n\n질문: {query}"}
        ]
    )

    return response.choices[0].message.content
```

## 🗃️ 데이터베이스 스키마

### 주요 테이블 (한글 컬럼명)

#### seoul_fire_dispatch (서울시 화재 출동)
```sql
CREATE TABLE seoul_fire_dispatch (
    id SERIAL PRIMARY KEY,
    접수번호 VARCHAR(50),
    발생일자 VARCHAR(8),
    발생시간 VARCHAR(6),
    소방서명 VARCHAR(100),
    사망자수 INTEGER,
    부상자수 INTEGER,
    재산피해액 BIGINT,
    발생장소 VARCHAR(200),
    화재원인 VARCHAR(200),
    -- ...
);
```

#### national_fire_status (전국 화재 현황)
```sql
CREATE TABLE national_fire_status (
    id SERIAL PRIMARY KEY,
    연도 INTEGER,
    시도명 VARCHAR(50),
    발생건수 INTEGER,
    사망자수 INTEGER,
    부상자수 INTEGER,
    재산피해액 BIGINT,
    -- ...
);
```

### 데이터 로드

`data_loader.py`는 CSV 파일의 영어 컬럼명을 한글로 자동 변환:

```python
# 컬럼명 매핑
COLUMN_MAPPINGS = {
    "incident_number": "접수번호",
    "date": "발생일자",
    "deaths": "사망자수",
    # ...
}

# CSV 로드 및 변환
df = pd.read_csv("fire_safety_data/seoul_fire_dispatch/2024.csv")
df = df.rename(columns=COLUMN_MAPPINGS)
df.to_sql("seoul_fire_dispatch", engine, if_exists="append", index=False)
```

## 🔧 개발 가이드

### 새 엔드포인트 추가

1. `app/api/endpoints/` 에 새 파일 생성
2. FastAPI 라우터 정의
3. `app/api/router.py`에 라우터 포함

```python
# app/api/endpoints/new_feature.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/new-feature")
async def new_feature(data: dict):
    return {"result": "success"}

# app/api/router.py
from .endpoints.new_feature import router as new_router
api_router.include_router(new_router, prefix="/new", tags=["New"])
```

### 새 기능 추가 (functionNo 5 예시)

1. `app/core/function_setup.py`에 함수 정의 추가
2. `app/services/features.py`에 기능 구현
3. `app/services/function_caller.py`에 라우팅 로직 추가

```python
# core/function_setup.py
FUNCTIONS = [
    # ... 기존 4개
    {
        "type": "function",
        "function": {
            "name": "feature_5",
            "description": "새 기능 설명",
            "parameters": {...}
        }
    }
]

# services/features.py
async def feature_5(query: str) -> dict:
    # 구현
    return {"functionNo": 5, "data": {...}}

# services/function_caller.py
if function_no == 5:
    return await feature_5(query)
```

### 환경 변수 추가

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    NEW_API_KEY: str  # 새 환경 변수

    class Config:
        env_file = ".env"

settings = Settings()
```

## 📊 데이터 처리 파이프라인

### 데이터 시각화 플로우

```
사용자 질의
    ↓
function_caller.py (GPT-4o 분석)
    ↓
visualization_ai_service.py (자연어 → SQL)
    ↓
visualization_query_service.py (SQL 실행)
    ↓
visualization_metadata_service.py (차트 메타데이터 생성)
    ↓
JSON 응답 (data + metadata)
```

### 문서 생성 플로우

```
사용자 질의
    ↓
function_caller.py
    ↓
features.py (document_service)
    ↓
GPT-4o (문서 내용 생성)
    ↓
ReportLab (PDF 생성)
    ↓
파일 저장 (backend/tmp/document.pdf)
```

## 🧪 테스트

### 수동 테스트

```bash
# 헬스 체크
curl http://localhost:8000/ping

# 채팅 테스트
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "2024년 화재 건수"}'

# PDF 다운로드
curl http://localhost:8000/pdf/download --output document.pdf
```

### Swagger UI 사용
http://localhost:8000/docs 에서 인터랙티브 테스트 가능

## 🔐 보안 고려사항

### CORS 설정
현재 모든 origin 허용. 프로덕션에서는 제한 필요:

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sodam.com"],  # 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API 키 보안
- `.env` 파일을 `.gitignore`에 추가
- 프로덕션에서는 환경 변수나 시크릿 관리 서비스 사용

### SQL Injection 방지
- SQLAlchemy ORM 사용
- 사용자 입력 검증
- GPT 생성 SQL에 대한 화이트리스트 검증

## 🚀 배포

### Docker 배포 (선택)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 빌드 및 실행
docker build -t sodam-backend .
docker run -p 8000:8000 --env-file .env sodam-backend
```

### Systemd 서비스 (Linux)

```ini
# /etc/systemd/system/sodam-backend.service
[Unit]
Description=Sodam Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/firesafety-platform/backend
Environment="PATH=/var/www/firesafety-platform/backend/venv/bin"
ExecStart=/var/www/firesafety-platform/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🐛 문제 해결

### PostgreSQL 연결 오류
```bash
# PostgreSQL 서비스 확인
sudo systemctl status postgresql

# 데이터베이스 존재 확인
psql -U YOUR_USERNAME -l | grep fire_safety_db

# 연결 테스트
psql -U YOUR_USERNAME -d fire_safety_db -c "SELECT 1;"
```

### OpenAI API 오류
- API 키 유효성 확인
- API 사용량 및 크레딧 확인
- 모델 이름 확인 (`gpt-4o`)

### 데이터 로더 오류
```python
# data_loader.py의 DB_CONFIG 수정
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "fire_safety_db",
    "user": "YOUR_USERNAME",  # ← 여기 수정
    "password": "YOUR_PASSWORD"
}
```

### FAISS 벡터스토어 오류
```bash
# 벡터스토어 재구축
rm -rf backend/vectorstore_FAISS/
python -m backend.scripts.build_vectorstore
```

## 📝 추가 정보

- FastAPI 공식 문서: https://fastapi.tiangolo.com/
- SQLAlchemy 문서: https://docs.sqlalchemy.org/
- LangChain 문서: https://python.langchain.com/
- OpenAI API 문서: https://platform.openai.com/docs/

---

**소담 Backend** - AI 기반 소방 안전 플랫폼의 핵심 엔진
