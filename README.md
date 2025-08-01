# 소담 (소방 업무를 담다) - Fire Safety Platform

종합 소방 업무 지원 플랫폼으로 4가지 핵심 기능을 제공합니다.

## 주요 기능

### 1. 화재 위험 예측 지도 및 경로 추천
- 실시간 화재 위험도 분석 및 시각화
- 소방서별 관할 구역 및 최적 경로 제안

### 2. 공문서 작성
- AI 기반 공문서 자동 생성
- PDF 다운로드 기능

### 3. 데이터 시각화 (Data Visualization)
- **자연어 쿼리**: GPT-4o를 활용한 지능형 SQL 생성
- **하이브리드 구조**: PostgreSQL 전용 테이블로 최적화된 성능
- **통합 관리**: 서울 화재출동, 임야화재, 차량화재, 구조출동, 전국화재현황 데이터
- **고성능 검색**: 400,000+ 레코드 실시간 조회
- **자동 데이터셋 추론**: dataset_type 자동 선택 지원

### 4. 일반 대화 (RAG)
- 소방 관련 지식 기반 대화형 AI

## 기술 스택

- **Backend**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 13+ (하이브리드 테이블 구조)
- **AI**: OpenAI GPT-4o API
- **ORM**: SQLAlchemy 2.0
- **Data Processing**: Pandas, Geopy
- **Additional**: VWorld API, Shapely

## 프로젝트 구조

```
firesafety-platform/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI 메인 애플리케이션
│   │   ├── config.py                   # 통합 설정 관리
│   │   ├── api/
│   │   │   ├── router.py               # API 라우터 통합
│   │   │   └── endpoints/              # 각 기능별 엔드포인트
│   │   ├── core/
│   │   │   ├── constants.py            # 상수 정의
│   │   │   ├── function_setup.py       # LLM Function Calling 설정
│   │   │   └── visualization_database.py # 데이터 시각화 DB 연결
│   │   ├── models/
│   │   │   └── visualization_models.py  # 데이터 시각화 모델
│   │   ├── schemas/                    # Pydantic 스키마
│   │   │   ├── building.py
│   │   │   ├── chat_request.py
│   │   │   ├── chat_response.py
│   │   │   └── visualization_schemas.py
│   │   └── services/
│   │       ├── features.py             # 4개 기능 구현
│   │       ├── function_caller.py      # LLM Function Calling
│   │       ├── building_service.py     # 건물 정보 서비스
│   │       ├── fire_risk.py           # 화재 위험도 계산
│   │       ├── patrol_service.py      # 순찰 서비스
│   │       └── visualization_*.py     # 데이터 시각화 서비스들
│   ├── data_loader.py                 # 소방 데이터 로더
│   └── requirements.txt
└── README.md
```

## 빠른 시작

### 1. 환경 설정

```bash
# 1. 저장소 클론
git clone <repository-url>
cd firesafety-platform/backend

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows

# 3. 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 설정을 추가하세요:

```env
# PostgreSQL 데이터베이스 (데이터 시각화용)
DATABASE_URL=postgresql://username:password@localhost:5432/fire_safety_db

# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# VWorld API 키 (지도 기능용)
VWORLD_KEY=your_vworld_api_key_here
```

### 3. 데이터베이스 설정

```bash
# PostgreSQL 데이터베이스 생성
createdb fire_safety_db

# 데이터 로더를 사용하여 소방 데이터 import (선택사항)
python data_loader.py --data-dir /path/to/csv/files
```

### 4. 서버 실행

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

서버가 실행되면 다음 URL에서 확인할 수 있습니다:
- **Swagger UI**: http://localhost:8080/docs (대화형 API 테스트)
- **ReDoc**: http://localhost:8080/redoc (깔끔한 문서 뷰)
- **헬스체크**: http://localhost:8080/ping

## API 사용법

### 통합 채팅 엔드포인트
모든 기능은 `/chat` 엔드포인트를 통해 자연어로 접근 가능합니다. OpenAI Function Calling이 자동으로 적절한 기능을 선택합니다.

### 1. 데이터 시각화 기능 (functionNo: 1)

```bash
# 예시 질문들
curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "화재 데이터를 보여줘"}'

curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "2021년 화재 발생 건수를 알려줘"}'

curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "강남구에서 발생한 화재 현황"}'
```

### 2. 공문서 작성 기능 (functionNo: 2)

```bash
curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "화재 예방 점검 공문서 작성해줘"}'

curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "소방시설 점검 결과 보고서 만들어줘"}'
```

### 3. 화재 위험 예측 기능 (functionNo: 3)

```bash
curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "종로 소방서 화재 예측 지도 그려줘"}'

curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "강남소방서 관할 위험 건물 보여줘"}'
```

### 4. 일반 대화 기능 (functionNo: 4)

```bash
curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "소방 안전 관리에 대해 알려줘"}'

curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "화재 예방 방법은 뭐가 있을까?"}'
```

**응답 예시:**
```json
{
  "functionNo": 1,
  "data": {
    "success": true,
    "generated_sql": "SELECT * FROM seoul_fire_dispatch WHERE dth_cnt > 0 OR injpsn_cnt > 0 LIMIT 100",
    "data": [...],
    "total_count": 45,
    "execution_time": 0.234
  }
}
```

### 기능별 동작

- **"화재 예측 지도 그려줘"** → 기능 3 (지도 예측)
- **"공문서 작성해줘"** → 기능 2 (PDF 생성)
- **"화재 데이터 분석해줘"** → 기능 1 (데이터 시각화)
- **"소방 관련 질문"** → 기능 4 (일반 대화)

## 데이터 시각화 기능 상세

### 지원 데이터셋
- **서울 화재출동 현황** (28,266+ records)
- **서울 임야화재 출동** 
- **서울 차량화재 출동**
- **서울 구조출동 현황** (193,951+ records)
- **전국 화재현황 통계**

### 데이터 시각화 자연어 쿼리 예시
- "2024년 사상자가 발생한 화재사고를 보여줘"
- "강남소방서 관할 화재 출동 현황은?"
- "아파트 화재 중 재산피해가 가장 큰 사건은?"
- "최근 한 달간 구조출동 통계를 알려줘"