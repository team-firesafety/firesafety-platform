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
                <p class="step-description">업무 관련 질문이나 도움이 필요한<br>내용을 자연스럽게 대화로 물어보세요.</p>
              </div>
              <div class="step">
                <div class="step-number">2</div>
                <p class="step-description">AI가 소방 전문 지식을 바탕으로<br>정확하고 실용적인 답변을 제공합니다.</p>
              </div>
              <div class="step">
                <div class="step-number">3</div>
                <p class="step-description">제공받은 정보나 가이드라인을<br>활용해 효율적으로 업무를 처리하세요.</p>
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
              <h3>선택지역의 화재예측<br>지도를 제공합니다.</h3>
            </div>
            <div class="feature-item">
              <img src="@/assets/intro-doc.png" alt="공문서 작성" class="feature-icon" />
              <h3>화재 조사 보고서, 점검 결과서<br>등을 도와드립니다.</h3>
            </div>
            <div class="feature-item">
              <img src="@/assets/intro-graph.png" alt="데이터 시각화" class="feature-icon" />
              <h3>화재, 소방업무 관련 데이터를<br>시각화 시켜줍니다.</h3>
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
  position: relative;
}

.intro-page-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, rgba(39, 68, 255, 0.08) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(0, 34, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.intro-page {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-rows: 22% 48% 30%;
  padding: 35px 80px;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
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
  animation: fadeInDown 0.8s ease-out;
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

/* 하단 영역 (30%) */
.bottom-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 10px;
}

.character-logo {
  width: 100px;
  height: 100px;
  transition: transform 0.3s ease;
}

.character-logo:hover {
  transform: scale(1.05);
}

.logo-text-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  margin-left: 15px;
}

.sodam-logo {
  height: 60px;
  width: auto;
}

.service-description {
  font-size: 18px;
  color: #666;
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.3px;
}

/* 첫 번째 페이지 - 소개 멘트 */
.intro-message {
  text-align: center;
  margin-top: 15px;
}

.main-message {
  font-size: 24px;
  color: #2744FF;
  line-height: 1.5;
  margin: 0 auto 40px;
  font-weight: 600;
  max-width: 1050px;
  padding: 0;
  text-align: center;
  background: none;
  border: none;
  box-shadow: none;
  backdrop-filter: none;
  animation: slideInUp 0.8s ease-out 0.3s both;
}

/* 사용방법 섹션 */
.usage-section {
  width: 100%;
  margin-top: 0;
}

.usage-title {
  font-size: 30px;
  color: #333;
  text-align: center;
  margin: 0 0 30px 0;
  font-weight: 600;
  position: relative;
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.usage-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #2744FF, #0022FF);
  border-radius: 2px;
}

.usage-steps {
  display: flex;
  justify-content: center;
  gap: 45px;
  max-width: 1150px;
  margin: 0 auto;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
  max-width: 350px;
  padding: 32px 26px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  border: 1px solid rgba(39, 68, 255, 0.08);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease-out calc(0.5s + var(--delay)) both;
}

.step:nth-child(1) { --delay: 0s; }
.step:nth-child(2) { --delay: 0.1s; }
.step:nth-child(3) { --delay: 0.2s; }

.step:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  border-color: rgba(39, 68, 255, 0.15);
}

.step-number {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #2744FF 0%, #0022FF 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 26px;
  box-shadow: 0 8px 20px rgba(39, 68, 255, 0.25);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.step-number::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  transition: left 0.6s ease;
}

.step:hover .step-number {
  transform: scale(1.06);
  box-shadow: 0 10px 24px rgba(39, 68, 255, 0.35);
}

.step:hover .step-number::before {
  left: 100%;
}

.step-description {
  font-size: 17px;
  color: #555;
  line-height: 1.5;
  margin: 0;
  font-weight: 400;
  word-break: keep-all;
  padding: 0 8px;
}

/* 두 번째 페이지 - 주요 기능 */
.features-title {
  text-align: center;
  margin-bottom: 30px;
  width: 100%;
}

.features-title h2 {
  font-size: 32px;
  color: #333;
  margin: 0;
  font-weight: 600;
  position: relative;
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.features-title h2::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #2744FF, #0022FF);
  border-radius: 2px;
}

.features-section {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  gap: 35px;
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
  max-width: 360px;
  height: 280px;
  max-height: 280px;
  padding: 20px 18px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 18px;
  border: 1px solid rgba(39, 68, 255, 0.08);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease-out calc(0.5s + var(--delay)) both;
}

.feature-item:nth-child(1) { --delay: 0s; }
.feature-item:nth-child(2) { --delay: 0.1s; }
.feature-item:nth-child(3) { --delay: 0.2s; }

.feature-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12);
  border-color: rgba(39, 68, 255, 0.15);
}

.feature-icon {
  width: 100%;
  height: 65%;
  object-fit: contain;
  flex: 0 0 65%;
  transition: all 0.3s ease;
}

.feature-item:hover .feature-icon {
  transform: scale(1.02);
}

.feature-item h3 {
  font-size: 16px;
  font-weight: 500;
  color: #555;
  margin: 0;
  line-height: 1.4;
  flex: 0 0 35%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 12px 8px 0;
  word-break: keep-all;
}

/* 캐릭터 */
.character-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.main-character {
  width: 250px;
  height: auto;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 8px 20px rgba(0, 0, 0, 0.1));
  transition: all 0.3s ease;
}

.main-character:hover {
  transform: scale(1.02);
  animation-duration: 2s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 네비게이션 */
.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  color: #2744FF;
  border: 1px solid rgba(39, 68, 255, 0.2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.nav-arrow:hover {
  background: #2744FF;
  color: white;
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 6px 20px rgba(39, 68, 255, 0.25);
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
    grid-template-rows: 20% 48% 32%;
    padding: 35px 50px;
  }

  .top-section {
    padding-top: 15px;
  }

  .character-logo {
    width: 85px;
    height: 85px;
  }

  .sodam-logo {
    height: 50px;
  }

  .main-message {
    font-size: 22px;
    padding: 20px 25px;
  }

  .step {
    padding: 25px 15px;
  }

  .feature-item {
    height: 280px;
    max-height: 280px;
    padding: 20px 15px;
  }

  .main-character {
    width: 220px;
  }

  .bottom-section {
    padding-top: 15px;
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
    padding: 35px 50px;
    grid-template-rows: 22% 43% 35%;
  }

  .top-section {
    padding-top: 10px;
  }

  .character-logo {
    width: 80px;
    height: 80px;
  }

  .logo-text-container {
    margin-left: 12px;
  }

  .usage-steps {
    flex-direction: column;
    gap: 25px;
  }

  .step {
    max-width: 450px;
    margin: 0 auto;
    padding: 22px 25px;
  }

  .features-section {
    gap: 25px;
  }

  .feature-item {
    height: 250px;
    max-width: 300px;
    padding: 18px 15px;
  }

  .main-message {
    font-size: 20px;
    max-width: 650px;
  }

  .usage-title,
  .features-title h2 {
    font-size: 30px;
  }

  .step-description {
    font-size: 15px;
  }

  .feature-item h3 {
    font-size: 15px;
  }

  .main-character {
    width: 190px;
  }

  .bottom-section {
    padding-top: 25px;
  }
}

@media (max-width: 768px) {
  .intro-page {
    padding: 20px 25px;
    grid-template-rows: 28% 42% 30%;
  }

  .top-section {
    padding-top: 8px;
  }

  .logo-section {
    flex-direction: column;
    gap: 10px;
    margin-bottom: 12px;
  }

  .character-logo {
    width: 60px;
    height: 60px;
  }

  .logo-text-container {
    margin-left: 0;
  }

  .sodam-logo {
    height: 35px;
  }

  .service-description {
    font-size: 16px;
  }

  .usage-steps {
    gap: 18px;
  }

  .step {
    max-width: 100%;
    padding: 18px 15px;
  }

  .step-number {
    width: 45px;
    height: 45px;
    font-size: 16px;
    margin-bottom: 15px;
  }

  .features-section {
    flex-direction: column;
    gap: 18px;
    align-items: center;
  }

  .feature-item {
    height: 180px;
    max-width: 260px;
    width: 100%;
    padding: 15px 12px;
  }

  .feature-icon {
    height: 60%;
  }

  .main-message {
    font-size: 17px;
    padding: 15px 18px;
    max-width: 100%;
    border-radius: 15px;
  }

  .usage-title,
  .features-title h2 {
    font-size: 24px;
  }

  .usage-title {
    margin-bottom: 25px;
  }

  .features-title {
    margin-bottom: 20px;
  }

  .usage-title::after,
  .features-title h2::after {
    bottom: -8px;
    width: 40px;
    height: 3px;
  }

  .step-description {
    font-size: 13px;
    line-height: 1.4;
  }

  .feature-item h3 {
    font-size: 13px;
    line-height: 1.3;
  }

  .main-character {
    width: 130px;
  }

  .bottom-section {
    padding-top: 15px;
  }

  .nav-arrow {
    width: 45px;
    height: 45px;
  }

  .nav-arrow.next {
    right: 15px;
  }

  .nav-arrow.prev {
    left: 15px;
  }
}
</style>