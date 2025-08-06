# 소담 (소방 업무를 담다) - AI 기반 소방 안전 통합 플랫폼

AI 기반 소방 안전 통합 플랫폼으로, 4개의 핵심 기능을 제공합니다.

## 주요 기능

### 1. 데이터 시각화 (AI-Powered Data Visualization)
- **완전 한글 컬럼명**: 모든 데이터베이스 테이블이 `사망자수`, `재산피해액` 등 직관적인 한글 컬럼명으로 구성되어 있어 최고의 가독성과 개발 편의성을 제공합니다.
- **자연어 쿼리**: GPT-4o를 활용해 "2024년 사망자가 발생한 화재"와 같은 자연어를 정확한 한글 컬럼 기반 SQL로 자동 변환합니다.
- **차트 메타데이터 자동 생성**: 프론트엔드에서 즉시 차트를 그릴 수 있도록, 데이터와 함께 컬럼별 타입, 단위, 추천 차트 정보가 포함된 메타데이터를 자동으로 생성하여 반환합니다.
- **통합 데이터 관리**: 서울 화재출동, 임야화재, 차량화재, 구조출동, 전국화재현황 등 다양한 소방 데이터를 통합 관리합니다.

### 2. 공문서 작성 (AI Document Generation)
- AI 기반 소방 공문서 자동 생성
- PDF 다운로드 기능

### 3. 화재 위험 예측 (Fire Risk Prediction)
- 소방서별 관할 건물의 화재 위험도 예측
- 지도 데이터 제공

### 4. 일반 대화 (Conversational AI)
- RAG(Retrieval-Augmented Generation) 기술을 활용한 소방 관련 지식 기반 질의응답

## 기술 스택

- **Backend**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 13+ (한글 컬럼명 전용 테이블 구조)
- **AI**: OpenAI GPT-4o API
- **Data Processing**: Pandas
- **ORM**: SQLAlchemy 2.0 (일부 사용)

## 빠른 시작

### 1. 환경 설정

```bash
# 1. 저장소 클론
git clone <repository-url>
cd firesafety-platform/backend

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`backend` 폴더에 `.env` 파일을 생성하고 다음 설정을 추가하세요:

```env
# PostgreSQL 데이터베이스
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/fire_safety_db

# OpenAI API 키
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# VWorld API 키 (지도 기능용)
VWORLD_KEY=your_vworld_api_key_here
```

### 3. 데이터베이스 초기 설정

#### 3.1 PostgreSQL 데이터베이스 생성
```bash
# YOUR_USERNAME을 실제 PostgreSQL 사용자명으로 변경하여 실행하세요.
psql -U YOUR_USERNAME -c "CREATE DATABASE fire_safety_db;"
```

#### 3.2 테이블 스키마 생성
한글 컬럼명으로 구성된 테이블들을 생성합니다.
```bash
cd backend

# YOUR_USERNAME을 실제 PostgreSQL 사용자명으로 변경하여 실행하세요.
psql -U YOUR_USERNAME -d fire_safety_db -f migrations/visualization_schema.sql
```

#### 3.3 초기 데이터 로드 (필수)
데이터 시각화 기능을 사용하려면 반드시 초기 데이터를 로드해야 합니다. `data_loader.py`는 원본 CSV의 영어 컬럼명을 한글로 자동 변환하여 DB에 저장합니다.

**1) 데이터 파일 준비**
소방 데이터는 용량이 크기 때문에(259MB) Git 저장소에 포함되지 않습니다. 별도로 데이터를 다운로드하여 다음 구조로 배치해야 합니다.

```bash
# backend/data 폴더가 없다면 생성
mkdir -p backend/data

# 다운로드한 데이터 폴더를 backend/data/fire_safety_data 로 이동
# 최종 경로는 다음과 같아야 합니다: backend/data/fire_safety_data/seoul_fire_dispatch/...
```

**2) 데이터 로더 실행**
`data_loader.py`는 `main` 함수에 설정된 `DB_CONFIG`의 사용자명(`suhong`)을 기반으로 실행됩니다. **스크립트 내 사용자명을 본인의 PostgreSQL 사용자명으로 수정하거나, 아래와 같이 `psql` 명령어와 동일한 사용자로 실행할 수 있도록 권한을 맞춰주세요.**

```bash
# backend 폴더에서 실행
python data_loader.py
```

#### 3.4 RAG 벡터스토어 생성 (일반 대화 기능용)
```bash
# 프로젝트 루트 디렉토리에서 실행
python -m backend.scripts.build_vectorstore
```
- `backend/vectorstore_FAISS/` 폴더와 `index.faiss`, `index.pkl` 파일이 생성됩니다.
- `backend/data/상세정보_화재안전기술_상세정보.csv` 파일이 필요합니다.

### 4. 서버 실행

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 사용법

모든 기능은 `/chat` 엔드포인트를 통해 자연어로 접근 가능합니다.

### 데이터 시각화 기능 (functionNo: 1)

**요청 예시:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "강남소방서에서 발생한 화재 중 사망자가 있었던 사건들을 보여줘"}'
```

**응답 예시 (한글 컬럼명 및 차트 메타데이터 포함):**
```json
{
  "functionNo": 1,
  "data": {
    "success": true,
    "generated_sql": "SELECT 소방서명, 발생일자, 사망자수, 부상자수, 재산피해액 FROM seoul_fire_dispatch WHERE 소방서명 = '강남소방서' AND 사망자수 > 0 LIMIT 100",
    "data": [
      {
        "소방서명": "강남소방서",
        "발생일자": "20240115",
        "사망자수": 1,
        "부상자수": 2,
        "재산피해액": 85000
      }
    ],
    "total_count": 1,
    "columns_metadata": {
      "소방서명": {"type": "categorical", "chart_usage": ["groupby", "filter"]},
      "발생일자": {"type": "date", "chart_usage": ["x_axis"], "format": "YYYYMMDD"},
      "사망자수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "명"},
      "부상자수": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "명"},
      "재산피해액": {"type": "numeric", "chart_usage": ["y_axis"], "unit": "천원"}
    },
    "chart_recommendations": [
      {
        "type": "bar_chart",
        "name": "지역별/원인별 분석",
        "available_x_axis": ["소방서명"],
        "available_y_axis": ["사망자수", "부상자수", "재산피해액"],
        "description": "카테고리별 화재 발생 현황 비교"
      }
    ]
  }
}
```

### 데이터 시각화 자연어 쿼리 예시
- "2024년 사망자가 발생한 화재사고를 보여줘"
- "소방서별 화재 발생 건수"
- "아파트 화재 중 재산피해가 가장 큰 사건은?"
- "전기적 요인으로 발생한 화재 통계"
