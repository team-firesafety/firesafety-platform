<template>
  <div class="chat-page">
    <AppHeader />

    <div class="messages">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.from]"
      >
        <!-- 로딩 메시지 -->
        <template v-if="msg.loading">
          <Loading />
        </template>

        <!-- PDF 다운로드 메시지 -->
        <template v-if="msg.pdf">
          <div class="pdf-download">
            <a :href="msg.url" :download="msg.filename">
              <button class="pdf-btn">⬇ {{ msg.filename }}</button>
            </a>
          </div>
        </template>
        <!-- 일반 텍스트 메시지 -->
        <template v-else>
          <p>{{ msg.text }}</p>
        </template>
      </div>
    </div>

    <!-- 입력창 -->
    <ChatInput @send="sendMessage" bottom="40px"/>

    <!-- 기능 별 모달 -->
    <ModalVis
      v-if="showVisModal"
      :data="visResult"
      :functionNo="currentFunctionNo"
      @close="onVisModalClose"
    />
    <ModalPdf
      v-if="showPdfModal"
      :data="pdfResult"
      :functionNo="currentFunctionNo"
      @close="onPdfModalClose"
    />
    <ModalMap
      v-if="showMapModal"
      :data="mapResult"
      :functionNo="currentFunctionNo"
      @close="onMapModalClose"
    />
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue'
import ChatInput from './ChatInput.vue'
import ModalVis from './Modal1.vue'   // 데이터 시각화 모달
import ModalPdf from './Modal2.vue'     // 공문서 PDF 모달
import ModalMap from './Modal3.vue'     // 화재 예측 지도 모달
import Loading from './Loading.vue'

export default {
  name: 'ChatPage',
  components: { AppHeader, ChatInput, ModalVis, ModalPdf, ModalMap, Loading },
  data() {
    return {
      messages: [],              // 채팅 내역
      currentFunctionNo: null,
      // 모달 표시 상태 및 결과 데이터
      showVisModal: false,
      visResult: {},
      showPdfModal: false,
      pdfResult: {},
      showMapModal: false,
      mapResult: {},
      isLoading: false,
      loadingMessageIndex: -1,  // 로딩 메시지의 인덱스를 추적
    }
  },
  methods: {
    async sendMessage(text) {
      // 1) 사용자 메시지 추가
      this.messages.push({ from: 'user', text })

      // 2) 로딩 메시지 추가
      this.isLoading = true
      this.loadingMessageIndex = this.messages.length
      this.messages.push({ from: 'bot', loading: true })

      // 3) 모든 모달 초기화
      this.currentFunctionNo = null;
      this.showVisModal = false;  this.visResult = {}
      this.showMapModal = false;  this.mapResult = {}
      this.showPdfModal = false;   this.pdfResult = {}

      try {
        // 4) 챗봇 호출
        const res = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: text }),
        })
        const { functionNo, data } = await res.json()
        this.currentFunctionNo = functionNo

        // 5) 로딩 메시지 제거
        this.removeLoadingMessage()

        // 6) 기능별 처리
        switch (functionNo) {
          case 1:
            // 데이터 시각화: 메시지 추가 후 모달 오픈
            this.messages.push({ from: 'bot', text: '📊 데이터 시각화를 생성했습니다.' })
            this.visResult = {}
            this.showVisModal = true
            this.$nextTick(()=>{
                this.visResult = data;
            });
            break

          case 2:
            // PDF 생성: 메시지 추가 후 모달 오픈
            this.pdfResult = {}
            this.showPdfModal = true
            this.$nextTick(()=>{
                this.pdfResult = data;
            });
            break

          case 3:
            // 지도: 메시지 추가 후 모달 오픈
            this.messages.push({ from: 'bot', text: '🗺️ 화재 예측 지도를 생성했습니다.' })
            this.mapResult = {}
            this.showMapModal = true
            this.$nextTick(()=>{
                this.mapResult = data;
            });
            break

          case 4:
            // 일반 대화: 메시지 추가
            const reply = data.message || data.text || '🤖 응답이 없습니다.'
            this.messages.push({ from: 'bot', text: reply })
            break

          default:
            // 알 수 없는 기능: 오류 메시지
            this.messages.push({ from: 'bot', text: '알 수 없는 기능입니다.' })
        }
      } catch (err) {
        console.error(err)
        this.removeLoadingMessage()
        this.messages.push({ from: 'bot', text: '서버 호출 실패' })
      } finally {
        this.isLoading = false
      }
    },

    // 로딩 메시지 제거
    removeLoadingMessage() {
      if (this.loadingMessageIndex >= 0 && this.loadingMessageIndex < this.messages.length) {
        this.messages.splice(this.loadingMessageIndex, 1)
        this.loadingMessageIndex = -1
      }
    },

    // 모달 종료 핸들러: 기록 남기기
    onVisModalClose() {
      this.showVisModal = false
      // 모달 닫을 때는 추가 메시지 없음 (이미 생성 완료 메시지가 있음)
    },
    onPdfModalClose() {
      this.showPdfModal = false
      if (this.currentFunctionNo === 2 && this.pdfResult.download_url) {
        this.messages.push({
          from: 'bot',
          pdf: true,
          filename: this.pdfResult.pdf_filename,
          url: this.pdfResult.download_url,
        })
      }
    },
    onMapModalClose() {
      this.showMapModal = false
      // 모달 닫을 때는 추가 메시지 없음 (이미 생성 완료 메시지가 있음)
    },
  },
  created() {
    const init = this.$route.query.q
    if (init) this.sendMessage(init)
  },
}
</script>

<style scoped>
.loading-overlay{
  position:fixed;
  inset:0;                        /* 화면 전체 */
  display:flex;
  align-items:center;
  justify-content:center;
  background:rgba(255,255,255,.45);/* 살짝 흐린 배경 */
  z-index:1100;                   /* 모달(1000)보다 살짝 높게 */
}

.chat-page {
  position: relative;
  height: 100vh;
  background: #F5F6FA;
  overflow: hidden;
}
.messages {
  position: absolute;
  top: 144px;       /* 헤더 아래 */
  bottom: 0;        /* 컨테이너 하단을 채우되 */
  left: 0;
  right: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 0;
  padding-bottom: 220px; /* 입력창 영역 확보 */
}
.message {
  max-width: 70%;
  padding: 20px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #E6E8EC;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}
.message.bot {
  margin-left: 500px;
  margin-right: auto;
}
.message.user {
  margin-right: 500px;
  margin-left: auto;
}
.pdf-download {
  display: flex;
  justify-content: flex-start;
}
.pdf-btn {
  background: none;
  border: none;
  font-size: 14px;
  cursor: pointer;
}
.message p {
  margin: 0;
}
</style>