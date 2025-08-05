<template>
  <div class="intro-page-container">
    <div class="intro-page">
      <!-- 상단 로고 영역 (20%) -->
      <div class="top-section">
        <div class="logo-section">
          <img src="@/assets/character-logo.png" alt="캐릭터 로고" class="character-logo" />
          <div class="logo-text-container">
            <img src="@/assets/sodam-logo.png" alt="소담 로고" class="sodam-logo" />
            <p class="service-description">소방 업무 지원 AI 어시스턴트</p>
          </div>
        </div>
        
        <!-- 첫 페이지 소개 멘트만 상단에 -->
        <div v-if="currentPage === 1" class="intro-message">
          <p class="main-message">소방관들의 일상 업무를 더욱 효율적으로 처리할 수 있도록 AI 기술을 활용한 지능형 업무 지원 시스템입니다.</p>
        </div>
      </div>
      
      <!-- 중앙 콘텐츠 영역 (45%) -->
      <div class="content-area">
        <!-- 첫 번째 페이지 내용 -->
        <div v-if="currentPage === 1" class="page-content">
          <div class="usage-section">
            <h2 class="usage-title">소담 사용방법</h2>
            <div class="usage-steps">
              <div class="step">
                <div class="step-number">1</div>
                <p class="step-description">업무 관련 질문이나 도움이 필요한 내용을 자연스럽게 대화로 물어보세요.</p>
              </div>
              <div class="step">
                <div class="step-number">2</div>
                <p class="step-description">AI가 소방 전문 지식을 바탕으로 정확하고 실용적인 답변을 제공합니다.</p>
              </div>
              <div class="step">
                <div class="step-number">3</div>
                <p class="step-description">제공받은 정보나 가이드라인을 활용해 효율적으로 업무를 처리하세요.</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 두 번째 페이지 내용 -->
        <div v-if="currentPage === 2" class="page-content">
          <div class="features-title">
            <h2>주요 기능</h2>
          </div>
          
          <div class="features-section">
            <div class="feature-item">
              <img src="@/assets/intro-map.png" alt="화재 위험 예측" class="feature-icon" />
              <h3>선택지역의 화재예측 지도를 제공합니다.</h3>
            </div>
            <div class="feature-item">
              <img src="@/assets/intro-doc.png" alt="공문서 작성" class="feature-icon" />
              <h3>화재 조사 보고서, 점검 결과서 등을 도와드립니다.</h3>
            </div>
            <div class="feature-item">
              <img src="@/assets/intro-graph.png" alt="데이터 시각화" class="feature-icon" />
              <h3>화재, 소방업무 관련 데이터를 시각화 시켜줍니다.</h3>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 하단 캐릭터 영역 (35%) -->
      <div class="bottom-section">
        <div class="character-container">
          <img src="@/assets/character.png" alt="소담 캐릭터" class="main-character" />
        </div>
      </div>
      
      <!-- 네비게이션 버튼 -->
      <button v-if="currentPage < 2" class="nav-arrow next" @click="nextPage">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      
      <button v-if="currentPage > 1" class="nav-arrow prev" @click="prevPage">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IntroPage',
  data() {
    return {
      currentPage: 1
    }
  },
  methods: {
    closeIntro() {
      this.$emit('close')
    },
    nextPage() {
      if (this.currentPage < 2) {
        this.currentPage++
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    }
  }
}
</script>

<style scoped>
.intro-page-container {
  width: 100%;
  height: 100vh;
  background-color: #F5F6FA;
  overflow: hidden;
}

.intro-page {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-rows: 20% 45% 35%;
  padding: 55px 80px;
  box-sizing: border-box;
  position: relative;
}

/* 상단 영역 (20%) */
.top-section {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding-top: 20px;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

/* 중앙 영역 (45%) */
.content-area {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
  padding: 0 20px;
  min-height: 0;
}

.page-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 0;
}

/* 하단 영역 (35%) */
.bottom-section {
  display: flex;
  justify-content: center;
  align-items: center;
}

.character-logo {
  width: 100px;
  height: 100px;
}

.logo-text-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.sodam-logo {
  height: 60px;
  width: auto;
}

.service-description {
  font-size: 18px;
  color: #666;
  margin: 0;
  font-weight: 400;
}

/* 첫 번째 페이지 - 소개 멘트 */
.intro-message {
  text-align: center;
  margin-top: 10px;
}

.main-message {
  font-size: 24px;
  color: #2744FF;
  line-height: 1.6;
  margin: 0;
  font-weight: 400;
}

/* 사용방법 섹션 */
.usage-section {
  width: 100%;
}

.usage-title {
  font-size: 32px;
  color: #666;
  text-align: center;
  margin: 0 0 50px 0;
  font-weight: 400;
}

.usage-steps {
  display: flex;
  justify-content: center;
  gap: 60px;
  max-width: 1000px;
  margin: 0 auto;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
  max-width: 300px;
}

.step-number {
  width: 50px;
  height: 50px;
  background: #0022FF;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 25px;
}

.step-description {
  font-size: 20px;
  color: #666;
  line-height: 1.5;
  margin: 0;
}

/* 두 번째 페이지 - 주요 기능 */
.features-title {
  text-align: center;
  margin-bottom: 40px;
  width: 100%;
}

.features-title h2 {
  font-size: 32px;
  color: #666;
  margin: 0;
  font-weight: 400;
}

.features-section {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  gap: 38px;
  max-width: 100%;
  width: 100%;
  height: 100%;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
  max-width: 410px;
  height: 320px;
  max-height: 320px;
}

.feature-icon {
  width: 100%;
  height: 80%;
  object-fit: contain;
  flex: 0 0 80%;
}

.feature-item h3 {
  font-size: 20px;
  font-weight: 500;
  color: #666;
  margin: 0;
  line-height: 1.4;
  flex: 0 0 20%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 10px;
}

/* 캐릭터 */
.character-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.main-character {
  width: 265px;
  height: auto;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

/* 네비게이션 */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #CCCCCC;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  z-index: 10;
}

.nav-arrow:hover {
  background: #999999;
}

.nav-arrow svg {
  width: 24px;
  height: 24px;
}

.nav-arrow.next {
  right: 30px;
}

.nav-arrow.prev {
  left: 30px;
}

/* 반응형 */
@media (max-height: 900px) {
  .intro-page {
    grid-template-rows: 18% 50% 32%;
    padding: 40px 60px;
  }
  
  .top-section {
    padding-top: 10px;
  }
  
  .character-logo {
    width: 80px;
    height: 80px;
  }
  
  .sodam-logo {
    height: 50px;
  }
  
  .feature-item {
    height: 280px;
    max-height: 280px;
  }
  
  .main-character {
    width: 220px;
  }
}

@media (max-height: 800px) {
  .intro-page {
    grid-template-rows: 16% 55% 29%;
    padding: 30px 50px;
  }
  
  .top-section {
    padding-top: 5px;
  }
  
  .character-logo {
    width: 70px;
    height: 70px;
  }
  
  .sodam-logo {
    height: 45px;
  }
  
  .logo-section {
    margin-bottom: 15px;
  }
  
  .main-message {
    font-size: 20px;
  }
  
  .usage-title,
  .features-title h2 {
    font-size: 28px;
    margin-bottom: 30px;
  }
  
  .feature-item {
    height: 240px;
    max-height: 240px;
  }
  
  .main-character {
    width: 180px;
  }
  
  .step-description {
    font-size: 18px;
  }
  
  .feature-item h3 {
    font-size: 16px;
  }
}

@media (max-width: 1200px) {
  .intro-page {
    padding: 30px 50px;
  }
  
  .top-section {
    padding-top: 15px;
  }
  
  .character-logo {
    width: 80px;
    height: 80px;
  }
  
  .usage-steps {
    flex-direction: column;
    gap: 35px;
  }
  
  .step {
    max-width: 400px;
  }
  
  .features-section {
    gap: 30px;
  }
  
  .feature-item {
    height: 280px;
    max-width: 350px;
  }
  
  .main-message {
    font-size: 20px;
  }
  
  .usage-title,
  .features-title h2 {
    font-size: 28px;
  }
  
  .step-description {
    font-size: 16px;
  }
  
  .feature-item h3 {
    font-size: 16px;
  }
  
  .main-character {
    width: 180px;
  }
}

@media (max-width: 768px) {
  .intro-page {
    padding: 20px 30px;
    grid-template-rows: 25% 40% 35%;
  }
  
  .top-section {
    padding-top: 10px;
  }
  
  .logo-section {
    flex-direction: column;
    gap: 15px;
    margin-bottom: 15px;
  }
  
  .character-logo {
    width: 60px;
    height: 60px;
  }
  
  .sodam-logo {
    height: 40px;
  }
  
  .usage-steps {
    gap: 25px;
  }
  
  .step {
    max-width: 300px;
  }
  
  .features-section {
    flex-direction: column;
    gap: 25px;
  }
  
  .feature-item {
    height: 220px;
    max-width: 280px;
  }
  
  .main-message {
    font-size: 18px;
  }
  
  .usage-title,
  .features-title h2 {
    font-size: 24px;
  }
  
  .usage-title {
    margin-bottom: 30px;
  }
  
  .features-title {
    margin-bottom: 30px;
  }
  
  .step-description {
    font-size: 14px;
  }
  
  .feature-item h3 {
    font-size: 14px;
    min-height: 40px;
  }
  
  .main-character {
    width: 160px;
  }
  
  .nav-arrow.next {
    right: 15px;
  }
  
  .nav-arrow.prev {
    left: 15px;
  }
}
</style>