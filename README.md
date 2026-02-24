# 소담 (소방 업무를 담다)

AI 기반 소방 안전 통합 플랫폼

---

**소담**은 AI를 활용해 복잡한 소방 업무 데이터를 쉽게 분석하고 시각화하는 통합 플랫폼입니다. 자연어 질의를 통해 데이터 조회, 화재 위험도 예측, 업무 문서 자동 생성이 가능합니다.

## 🎯 핵심 기능

### 1. 📊 데이터 시각화
자연어 질의를 통해 소방 데이터를 조회하고 차트로 시각화합니다.
- **한글 컬럼명 DB**: `사망자수`, `재산피해액` 등 직관적인 한글 컬럼으로 구성
- **자연어 to SQL**: "2024년 사망자가 발생한 화재"를 자동으로 SQL로 변환
- **차트 메타데이터**: 데이터와 함께 차트 추천 정보 자동 생성
- **통합 데이터**: 서울 화재출동, 임야화재, 차량화재, 구조출동, 전국 화재 통계 관리

### 2. 📄 문서 생성
AI 기반 소방 공문서 자동 작성 및 PDF 다운로드

### 3. 🗺️ 화재 위험 예측
건물별 화재 위험도를 지도에 시각화하고 AI로 분석

### 4. 💬 대화형 AI
RAG 기술을 활용한 소방 업무 관련 질의응답

## 🏗️ 아키텍처

```
firesafety-platform/
├── frontend/              # Vue.js 3 + Vite 기반 SPA
│   ├── src/
│   │   ├── components/    # 페이지 및 UI 컴포넌트
│   │   ├── router/        # Vue Router 설정
│   │   └── store/         # 상태 관리
│   └── package.json
│
├── backend/               # FastAPI 기반 REST API
│   ├── app/
│   │   ├── api/           # API 엔드포인트
│   │   ├── services/      # 비즈니스 로직 (AI, 데이터 처리)
│   │   ├── core/          # 핵심 설정 및 DB 연결
│   │   └── schemas/       # Pydantic 모델
│   ├── migrations/        # PostgreSQL 스키마
│   ├── data_loader.py     # CSV → DB 데이터 로더
│   └── requirements.txt
│
├── README.md              # 프로젝트 전체 가이드
└── CLAUDE.md              # 개발자 가이드
```

### 기술 스택

**Backend**
- FastAPI, PostgreSQL (한글 컬럼명), OpenAI GPT-4o
- LangChain + FAISS (RAG), SQLAlchemy, Pandas

**Frontend**
- Vue.js 3 (Composition API), Vite, Chart.js
- Axios, Vue Router, Kakao Maps API

## 🧩 시스템 아키텍처

![시스템 아키텍처](doc/System%20Architecture.png)

- **Client Layer**: 사용자가 Vue.js 기반 프론트엔드를 통해 서비스에 접근
- **Backend Server**: FastAPI가 모든 요청을 처리하고 기능별 서비스로 라우팅
- **Data Layer**: PostgreSQL(소방안전 데이터), FAISS Vector Store(RAG용), Local File Storage(문서 저장)
- **External Services**: OpenAI GPT-4o(자연어 처리 및 AI 기능), VWorld 지리정보(지도 데이터)

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- OpenAI API Key

### 1. 저장소 클론
```bash
git clone https://github.com/team-firesafety/firesafety-platform.git
cd firesafety-platform
```

### 2. 데이터베이스 설정
```bash
# PostgreSQL 데이터베이스 생성
psql -U YOUR_USERNAME -c "CREATE DATABASE fire_safety_db;"

# 스키마 마이그레이션 (한글 컬럼명 테이블 생성)
psql -U YOUR_USERNAME -d fire_safety_db -f backend/migrations/visualization_schema.sql
```

### 3. 백엔드 설정
```bash
cd backend

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (backend/.env 파일 생성)
cat > .env << EOF
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/fire_safety_db
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
VWORLD_KEY=your_vworld_api_key_here
EOF

# 초기 데이터 로드 (data_loader.py에서 사용자명 수정 필요)
python data_loader.py

# RAG 벡터스토어 구축
python -m backend.scripts.build_vectorstore

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 프론트엔드 설정
```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 5. 접속
- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Backend ReDoc**: http://localhost:8000/redoc

## 📖 상세 문서

- **[Frontend 개발 가이드](./frontend/README.md)** - Vue.js 프론트엔드 구조 및 개발 가이드
- **[Backend 개발 가이드](./backend/README.md)** - FastAPI 백엔드 아키텍처 및 API 명세
- **[개발자 가이드 (CLAUDE.md)](./CLAUDE.md)** - 프로젝트 전체 구조 및 개발 노트

## 🔑 주요 특징

### 1. 한글 데이터베이스 시스템
모든 데이터베이스 테이블이 한글 컬럼명을 사용하여 가독성과 직관성을 극대화했습니다.

```sql
-- 예시: seoul_fire_dispatch 테이블
사망자수, 부상자수, 재산피해액, 발생장소, 화재원인, 소방서명 ...
```

### 2. AI 기반 통합 라우팅
하나의 채팅 인터페이스로 모든 기능에 접근 가능합니다. GPT-4o가 자동으로 질의를 분석하여 적절한 기능을 호출합니다.

```
사용자: "2023년 강남구 화재 건수를 그래프로 보여줘"
  ↓
GPT-4o 분석 → functionNo: 1 (데이터 시각화)
  ↓
SQL 생성 → PostgreSQL 조회 → Chart.js 시각화
```

### 3. 자연어 기반 다기능 처리

**데이터 조회 & 시각화**
- "2024년 사망자가 발생한 화재사고를 보여줘"
- "소방서별 화재 발생 건수를 막대 그래프로"

**문서 자동 생성**
- "화재 예방 점검 공문을 작성해줘"
- "안전 교육 자료 문서 만들어줘"

**위험도 예측 & 지도 시각화**
- "강남구 건물들의 화재 위험도를 지도에 표시해줘"
- "우리 소방서 관할 고위험 건물을 알려줘"

**지식 기반 질의응답 (RAG)**
- "소화기 종류별 사용법을 알려줘"
- "화재 안전 기준에 대해 설명해줘"

### 4. 실시간 차트 메타데이터
데이터 조회 시 자동으로 차트 추천 정보를 생성하여 프론트엔드에서 즉시 시각화 가능합니다.

## 🗂️ 데이터 구조

### 필수 데이터 디렉토리
```
backend/data/fire_safety_data/
├── seoul_fire_dispatch/         # 서울시 화재 출동 데이터
├── seoul_forest_fire_dispatch/  # 서울시 산불 출동 데이터
├── seoul_vehicle_fire_dispatch/ # 서울시 차량 화재 출동 데이터
├── seoul_rescue_dispatch/       # 서울시 구조 출동 데이터
└── national_fire_status/        # 전국 화재 통계 데이터
```

## 🛠️ API 테스트

### /chat 엔드포인트
모든 기능은 `/chat` 엔드포인트를 통해 자연어로 접근 가능합니다.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "2023년 화재 발생 건수를 알려줘"}'
```

### 기타 엔드포인트
- `GET /pdf/download` - PDF 문서 다운로드
- `POST /patrol/*` - 화재 위험 예측 순찰 데이터

## ⚠️ 주의사항

- `backend/data_loader.py`의 데이터베이스 사용자명은 'suhong'으로 하드코딩되어 있습니다. 환경에 맞게 수정하세요.
- RAG 기능을 사용하려면 반드시 `python -m backend.scripts.build_vectorstore`를 먼저 실행하여 벡터스토어를 구축해야 합니다.
- 프론트엔드는 기본적으로 `localhost:8000`에서 백엔드가 실행 중이라고 가정합니다.

## 🔧 문제 해결

### 데이터베이스 연결 오류
- PostgreSQL 서비스 실행 상태 확인
- `.env` 파일의 DATABASE_URL 검증
- 사용자명과 비밀번호 확인

### OpenAI API 오류
- OPENAI_API_KEY 설정 확인
- API 키 유효성 및 크레딧 확인

### 데이터 파일 없음
- `backend/data/fire_safety_data/` 경로에 CSV 파일 배치 확인
- 데이터 로더 실행 전 파일 준비 확인

### 벡터스토어 오류
- `backend/data/상세정보_화재안전기술_상세정보.csv` 파일 존재 확인
- `build_vectorstore` 스크립트 실행 여부 확인

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 개발되었습니다.

## 👥 기여

이슈 및 풀 리퀘스트를 환영합니다!

---

## 🔄 Git 히스토리 마이그레이션 안내

**업데이트 날짜**: 2026년 2월 24일

### 문제 발생
- **발생일**: 2026년 2월 4일 develop-merged 브랜치 병합 시
- **내용**: 대용량 AI vectorstore 파일(47.3MB)이 의도치 않게 커밋됨
  - `backend/vectorstore_FAISS/index.faiss` (32.1MB)
  - `backend/vectorstore_FAISS/index.pkl` (15.2MB)

### 처리 내용
- Git 히스토리에서 vectorstore 파일 완전 제거 (git filter-repo 사용)
- `.gitignore`에 `backend/vectorstore_FAISS/` 추가
- 저장소 크기 47MB 감소

### ⚠️ 기존 로컬 작업자 필수 작업

**2026년 2월 24일 이전에 main 브랜치를 pull 받은 경우:**

```bash
# 1. 로컬 변경사항 백업 (작업 중인 내용이 있다면)
git stash

# 2. 원격 히스토리 동기화
git fetch origin
git reset --hard origin/main

# 3. Vectorstore 재생성 (RAG 기능 사용 시 필수)
cd backend
python -m backend.scripts.build_vectorstore

# 4. 백업한 작업 복원
git stash pop
```

**주의사항:**
- `git reset --hard`는 로컬 커밋을 삭제하므로, 미푸시 작업은 백업 필수
- vectorstore는 로컬에서만 생성하고 Git에 커밋하지 마세요
- 소스 코드와 폴더 구조는 변경 없음 (커밋 해시만 변경됨)

---

**소담** - 소방 업무를 담다
