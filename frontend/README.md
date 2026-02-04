# Frontend - 소담 플랫폼

Vue.js 3 기반 소방 안전 플랫폼 프론트엔드

## 📋 개요

소담 플랫폼의 프론트엔드는 Vue.js 3와 Vite를 사용하여 구축된 SPA(Single Page Application)입니다. 사용자가 자연어로 소방 데이터를 조회하고, 차트로 시각화하며, AI 기반 문서를 생성하고, 화재 위험도를 지도에서 확인할 수 있는 인터페이스를 제공합니다.

## 🏗️ 프로젝트 구조

```
frontend/
├── index.html              # HTML 진입점
├── package.json            # 프로젝트 메타데이터 및 의존성
├── vite.config.js          # Vite 빌드 설정
└── src/
    ├── main.js             # Vue 앱 진입점
    ├── App.vue             # 루트 컴포넌트
    ├── style.css           # 전역 스타일
    ├── router/
    │   └── index.js        # Vue Router 라우팅 설정
    ├── store/
    │   └── auth.js         # 인증 상태 관리
    ├── utils/
    │   └── loadKakao.js    # Kakao Maps SDK 로더
    ├── assets/             # 이미지 및 정적 리소스
    └── components/
        ├── LoginPage.vue       # 로그인 페이지
        ├── SignupPage.vue      # 회원가입 페이지
        ├── IntroPage.vue       # 소개 페이지
        ├── MainPage.vue        # 메인 대시보드
        ├── ChatPage.vue        # AI 챗봇 페이지
        ├── Header.vue          # 헤더 컴포넌트
        ├── Sidebar.vue         # 사이드바 네비게이션
        ├── ChatInput.vue       # 채팅 입력 컴포넌트
        ├── Modal1.vue          # 데이터 시각화 모달
        ├── Modal2.vue          # 문서 생성 모달
        ├── Modal3.vue          # 화재 위험 예측 모달
        ├── KakaoMap.vue        # 카카오 지도 컴포넌트
        └── Loading.vue         # 로딩 인디케이터
```

## 🛠️ 기술 스택

- **Vue.js 3.5** - Composition API 사용
- **Vite 7.0** - 빠른 개발 서버 및 빌드 도구
- **Vue Router 4.5** - SPA 라우팅
- **Chart.js 4.5** - 데이터 시각화 (막대, 선, 파이 차트)
- **Axios 1.11** - HTTP 클라이언트
- **Kakao Maps API** - 지도 표시 및 마커
- **markdown-it 14.1** - 마크다운 렌더링

## 🚀 시작하기

### 설치

```bash
# 의존성 설치
npm install
```

### 개발 서버 실행

```bash
# 개발 서버 시작 (http://localhost:5173)
npm run dev
```

### 프로덕션 빌드

```bash
# 프로덕션 빌드 생성
npm run build

# 빌드 결과 미리보기
npm run preview
```

## 🗺️ 라우팅

| 경로 | 컴포넌트 | 설명 | 인증 필요 |
|------|----------|------|-----------|
| `/` | LoginPage | 로그인 페이지 | ❌ |
| `/login` | LoginPage | 로그인 리디렉션 | ❌ |
| `/signup` | SignupPage | 회원가입 페이지 | ❌ |
| `/main` | MainPage | 메인 대시보드 | ✅ |
| `/chat` | ChatPage | AI 챗봇 페이지 | ✅ |

### 라우터 가드

`router/index.js`에 구현된 `beforeEach` 가드:
- 로그인하지 않은 사용자는 자동으로 로그인 페이지로 이동
- 로그인한 사용자가 로그인 페이지 접근 시 메인 페이지로 리디렉션
- 인증 상태는 `localStorage.getItem('isLoggedIn')`로 확인

## 🎨 주요 컴포넌트

### 1. LoginPage.vue & SignupPage.vue
- 사용자 인증 UI
- localStorage 기반 인증 상태 관리
- 프로필 정보 저장 (이름, 소방서, 계급)

### 2. MainPage.vue
- 소담 플랫폼 소개
- 4가지 핵심 기능 설명 (데이터 시각화, 문서 생성, 화재 위험 예측, 대화형 AI)
- 챗봇 페이지로 이동 버튼

### 3. ChatPage.vue
- AI 챗봇 메인 인터페이스
- 메시지 히스토리 표시
- 기능별 모달 관리 (Modal1, Modal2, Modal3)
- 백엔드 `/chat` API 연동

### 4. ChatInput.vue
- 채팅 입력창 (textarea)
- 전송 버튼 및 엔터 키 이벤트 처리
- 부모 컴포넌트로 메시지 emit

### 5. Modal1.vue (데이터 시각화)
- Chart.js를 사용한 차트 렌더링
- 백엔드에서 받은 데이터 및 메타데이터 기반 시각화
- 차트 타입: 막대, 선, 파이, 도넛
- X축/Y축 동적 선택 기능
- 그룹화 옵션 (일별, 월별, 계절별, 연도별)

### 6. Modal2.vue (문서 생성)
- AI 생성 문서 표시
- PDF 다운로드 버튼 (`/pdf/download` API 호출)

### 7. Modal3.vue & KakaoMap.vue (화재 위험 예측)
- Kakao Maps API를 사용한 지도 표시
- 건물 마커 표시 및 위험도 색상 구분
- 마커 클릭 시 건물 정보 및 AI 분석 결과 표시
- 소방서 위치 마커

### 8. Sidebar.vue
- 네비게이션 메뉴
- 사용자 프로필 정보 표시
- 페이지 이동 및 로그아웃 기능

### 9. Header.vue
- 페이지 제목 및 브랜딩

### 10. Loading.vue
- API 호출 중 로딩 애니메이션

## 🔌 API 연동

### 백엔드 엔드포인트
기본 URL: `http://localhost:8000`

#### POST /chat
모든 AI 기능의 진입점

**요청:**
```javascript
{
  "query": "사용자의 자연어 질의"
}
```

**응답:**
```javascript
{
  "functionNo": 1,  // 1: 시각화, 2: 문서, 3: 위험예측, 4: 대화
  "data": {
    // functionNo에 따라 다른 데이터 구조
  }
}
```

#### GET /pdf/download
문서 PDF 다운로드

**응답:** PDF 파일 (application/pdf)

### Axios 사용 예시

```javascript
import axios from 'axios'

// 채팅 메시지 전송
const sendMessage = async (query) => {
  try {
    const response = await axios.post('http://localhost:8000/chat', { query })
    return response.data
  } catch (error) {
    console.error('API 오류:', error)
  }
}

// PDF 다운로드
const downloadPDF = async () => {
  const response = await axios.get('http://localhost:8000/pdf/download', {
    responseType: 'blob'
  })
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'document.pdf')
  document.body.appendChild(link)
  link.click()
}
```

## 📊 Chart.js 통합

Modal1.vue에서 Chart.js를 사용하여 다양한 차트를 렌더링합니다.

### 지원 차트 타입
- **막대 차트** (Bar)
- **선 차트** (Line)
- **파이 차트** (Pie)
- **도넛 차트** (Doughnut)

### 동적 차트 생성
백엔드에서 받은 `columns_metadata`와 `chart_recommendations`를 기반으로 사용자가 X축/Y축을 선택하여 차트를 동적으로 생성할 수 있습니다.

```javascript
// 차트 생성 예시
import { Chart } from 'chart.js/auto'

const createChart = (ctx, type, labels, data) => {
  new Chart(ctx, {
    type: type,  // 'bar', 'line', 'pie', 'doughnut'
    data: {
      labels: labels,
      datasets: [{
        label: 'Dataset',
        data: data,
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}
```

## 🗺️ Kakao Maps 통합

KakaoMap.vue에서 Kakao Maps JavaScript API를 사용합니다.

### 설정
- `loadKakao.js`를 통해 SDK 동적 로드
- 지도 중심: 서울 (37.5665, 126.9780)
- 줌 레벨: 10

### 마커 표시
```javascript
// 건물 마커 추가 (위험도에 따라 색상 다름)
const addBuildingMarker = (map, building) => {
  const marker = new kakao.maps.Marker({
    position: new kakao.maps.LatLng(building.lat, building.lng),
    map: map
  })

  // 마커 클릭 이벤트
  kakao.maps.event.addListener(marker, 'click', () => {
    showBuildingInfo(building)
  })
}
```

## 🎨 스타일링

### 전역 스타일
`src/style.css`에 전역 CSS 정의

### 컴포넌트 스코프 스타일
각 `.vue` 파일 내부에 `<style scoped>` 섹션으로 컴포넌트별 스타일 정의

```vue
<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
</style>
```

## 🔐 인증 및 상태 관리

### localStorage 기반 인증
- `isLoggedIn`: 로그인 상태 (true/false)
- `userName`: 사용자 이름
- `userFireStation`: 소속 소방서
- `userRank`: 계급

### store/auth.js
간단한 인증 헬퍼 함수 제공

```javascript
export const login = (name, fireStation, rank) => {
  localStorage.setItem('isLoggedIn', 'true')
  localStorage.setItem('userName', name)
  localStorage.setItem('userFireStation', fireStation)
  localStorage.setItem('userRank', rank)
}

export const logout = () => {
  localStorage.clear()
}
```

## 🧪 개발 가이드

### 새 컴포넌트 추가
1. `src/components/` 폴더에 `.vue` 파일 생성
2. 템플릿, 스크립트, 스타일 작성
3. 필요시 `router/index.js`에 라우트 추가

### API 엔드포인트 변경
백엔드 서버 주소가 변경되면 각 컴포넌트의 axios 호출에서 URL 수정 필요

```javascript
// 현재: http://localhost:8000
// 변경 예시: http://api.sodam.com
axios.post('http://api.sodam.com/chat', ...)
```

### 환경 변수 사용 (선택사항)
Vite에서 환경 변수를 사용하려면 `.env` 파일 생성:

```env
VITE_API_BASE_URL=http://localhost:8000
```

코드에서 사용:
```javascript
const API_URL = import.meta.env.VITE_API_BASE_URL
```

## 📦 빌드 및 배포

### 프로덕션 빌드
```bash
npm run build
```

`dist/` 폴더에 정적 파일 생성됨

### 배포
생성된 `dist/` 폴더를 정적 파일 서버에 배포:
- Nginx
- Apache
- Netlify
- Vercel
- GitHub Pages

### Nginx 설정 예시
```nginx
server {
    listen 80;
    server_name sodam.com;

    root /var/www/firesafety-platform/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 🐛 문제 해결

### CORS 오류
백엔드 서버에서 CORS 설정이 올바른지 확인:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 차트가 표시되지 않음
1. Chart.js가 설치되어 있는지 확인: `npm list chart.js`
2. canvas 요소가 DOM에 존재하는지 확인
3. 데이터 형식이 올바른지 확인

### 카카오 지도 로드 실패
1. Kakao JavaScript SDK가 로드되었는지 확인
2. 브라우저 콘솔에서 에러 메시지 확인
3. `loadKakao.js`가 올바르게 import되었는지 확인

### 라우터 가드 문제
`localStorage`의 `isLoggedIn` 값이 문자열 `'true'`인지 확인 (불리언 `true`가 아님)

## 📝 추가 정보

- Vue.js 공식 문서: https://vuejs.org/
- Vite 공식 문서: https://vitejs.dev/
- Chart.js 공식 문서: https://www.chartjs.org/
- Kakao Maps API: https://apis.map.kakao.com/

---

**소담 Frontend** - Vue.js 3로 구축된 현대적인 소방 안전 플랫폼 UI
