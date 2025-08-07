<template>
  <div class="layout">
    <Sidebar @show-intro="showIntroPage" @new-chat="hideIntroPage" />
    <div class="page">
      <!-- 소개페이지가 표시될 때 -->
      <IntroPage v-if="isIntroVisible" />
      
      <!-- 기본 메인 컨텐츠 -->
      <main v-else class="main-content">
        <!-- 떠다니는 소방관 캐릭터 + 그림자 -->
        <div class="character-wrapper">
          <img
            class="character"
            src="@/assets/character.png"
            alt="소방관 캐릭터"
          />
          <div class="shadow"></div>
        </div>

        <!-- 텍스트 -->
        <p class="subtitle">필요한게 있으실까요?</p>

        <!-- 공통 ChatInput 컴포넌트 사용 -->
        <div class="chat-input-wrapper">
          <ChatInput @send="goToChat" class="main-page-input" ref="chatInput"/>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import ChatInput from '@/components/ChatInput.vue'
import Sidebar from '@/components/Sidebar.vue'
import IntroPage from '@/components/IntroPage.vue'

export default {
  name: 'MainPage',
  components: { Sidebar, ChatInput, IntroPage },
  data() {
    return {
      isIntroVisible: false
    }
  },
  methods: {
    goToChat(messageData) {
      // ChatInput에서 받은 데이터가 객체인 경우 텍스트만 추출
      const queryText = typeof messageData === 'string' ? messageData : messageData.text;
      console.log('MainPage goToChat 받은 데이터:', messageData, '→ 쿼리 텍스트:', queryText)
      
      // 이미지가 첨부된 경우 경고 메시지 (MainPage에서는 이미지 지원 안함)
      if (typeof messageData === 'object' && messageData.image) {
        console.warn('MainPage에서는 이미지 첨부를 지원하지 않습니다. 텍스트만 전송됩니다.');
      }
      
      this.$router.push({ name: 'Chat', query: { q: queryText } })
    },
    showIntroPage() {
      this.isIntroVisible = true
    },
    hideIntroPage() {
      this.isIntroVisible = false
    }
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.page {
  flex: 1;
  position: relative; 
  margin-left: 340px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F5F6FA;
}

.header {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

.logo {
  height: 48px;
  width: auto;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 80px 40px 40px 40px; /* 하단 패딩 원래대로 */
  position: relative;
  min-height: 0;
}

/* ── 캐릭터 + 그림자 ── */
.character-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 40px;
  z-index: 1;
}

.character {
  width: 400px;
  animation: floatY 3s ease-in-out infinite;
  will-change: transform;
}

@keyframes floatY {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-60px); /* 최고점에서 60px 위로 띄워, top과의 간격이 180px - 60px = 120px 가 되도록 */
  }
}

.shadow {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%) scale(1);
  width: 400px;
  height: 80px;
  background: radial-gradient(
    ellipse at center,
    rgba(0, 0, 0, 0.6) 0%,
    transparent 70%
  );
  border-radius: 50%;
  opacity: 0.7;
  animation: shadowPulse 3s ease-in-out infinite;
  will-change: transform, opacity;
}

@keyframes shadowPulse {
  0%, 100% {
    transform: translateX(-50%) scale(1);
    opacity: 0.7;
  }
  50% {
    transform: translateX(-50%) scale(0.6);
    opacity: 0.35;
  }
}

/* 그라데이션 텍스트 */
.subtitle {
  margin-bottom: 20px; /* 간격을 줄여서 채팅창을 더 위로 */
  font-size: 32px;
  font-weight: 500;
  color: #0022FF !important;
  text-align: center;
  white-space: nowrap;
  display: block;
  visibility: visible;
}

/* MainPage 전용 ChatInput 스타일 */
.chat-input-wrapper {
  width: 100%;
  max-width: 600px;
  margin: 0 auto; /* 하단 여백 제거 */
}

.main-page-input {
  position: relative !important;
  width: 100% !important;
  margin: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

/* 이미지 미리보기 있을 때 추가 여백 */
.main-page-input.has-preview {
  margin-bottom: 30px !important; /* 하단 여백을 더 늘림 */
}
</style>
