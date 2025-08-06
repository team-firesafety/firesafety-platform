<template>
  <div class="layout">
    <Sidebar @show-intro="showIntroPage" @new-chat="hideIntroPage" />
    <div class="page">
      <!-- 소개페이지가 표시될 때 -->
      <IntroPage v-if="isIntroVisible" />
      
      <!-- 기본 메인 컨텐츠 -->
      <main v-else class="main-content">
        <!-- 떠다니는 캐릭터 + 그림자 (종전 그대로) -->
        <div class="character-wrapper">
          <img
            class="character"
            src="@/assets/character.png"
            alt="Animated Character"
          />
          <div class="shadow"></div>
        </div>

        <!-- 그라데이션 텍스트 -->
        <p class="subtitle">필요하신 게 있을까요?</p>

        <!-- 공통 ChatInput 컴포넌트 사용 -->
        <ChatInput @send="goToChat" bottom="160px"/>
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
    goToChat(query) {
      // 입력된 텍스트를 쿼리파라미터로 전달하며 /chat 으로 이동
      console.log('MainPage goToChat 받은 텍스트:', query)
      this.$router.push({ name: 'Chat', query: { q: query } })
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
  margin-top: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* ── 캐릭터 + 그림자 ── */
.character-wrapper {
  position: relative;
  display: inline-block;
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
  margin-top: 60px;
  font-size: 32px;
  font-weight: 500;
  background: linear-gradient(90deg, #0022FF 0%, #5664FF 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
