<template>
  <div class="chat-page">
    <!-- 헤더 -->
    <AppHeader />

    <!-- 메시지 영역 -->
    <div class="messages" ref="messages">
      <div
          v-for="(msg, idx) in messages"
          :key="idx"
          :class="['message-wrapper', msg.from]"
      >
        <div :class="['message', msg.from]">
          <!-- ① 로딩 -->
          <template v-if="msg.loading">
            <Loading />
          </template>

          <!-- ② PDF -->
          <template v-else-if="msg.pdf">
            <div class="pdf-download">
              <a :href="msg.url" :download="msg.filename">
                <button class="pdf-btn">⬇ {{ msg.filename }}</button>
              </a>
            </div>
          </template>

          <!-- ③ Markdown / Plain -->
          <template v-else>
            <div
                v-if="msg.html"
                class="markdown-content"
                v-html="msg.html"
            />
            <p v-else class="plain-text">{{ msg.text }}</p>
          </template>
        </div>
      </div>
    </div>

    <!-- 입력창 -->
    <ChatInput
        @send="sendMessage"
        bottom="40px"
        class="chat-input"
    />

    <!-- 모달들 -->
    <ModalVis v-if="showVisModal" :data="visResult" @close="onVisModalClose" />
    <ModalPdf v-if="showPdfModal" :data="pdfResult" @close="onPdfModalClose" />
    <ModalMap v-if="showMapModal" :data="mapResult" @close="onMapModalClose" />
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue';
import ChatInput from './ChatInput.vue';
import ModalVis from './Modal1.vue';
import ModalPdf from './Modal2.vue';
import ModalMap from './Modal3.vue';
import Loading from './Loading.vue';
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
  breaks: true,
  linkify: true,
  typographer: true,
  html: true
});

const STEP_MS = 50;           // 타자기 속도 더 빠르게
const MAX_W = 900;            // 메시지/입력창 최대 폭 증가

export default {
  name: 'ChatPage',
  components: {
    AppHeader, ChatInput, ModalVis, ModalPdf, ModalMap, Loading,
  },

  data() {
    return {
      messages: [],

      showVisModal: false, visResult: {},
      showPdfModal: false, pdfResult: {},
      showMapModal: false, mapResult: {},

      loadingMessageIndex: -1,
    };
  },

  methods: {
    /* ---------------------------------------------------------- */
    /* 메인 송신                                                   */
    /* ---------------------------------------------------------- */
    async sendMessage(text) {
      /* ─── 사용자 메시지 ─── */
      this.messages.push({from: 'user', text});
      this.scrollToBottom();

      /* ─── 로딩 메시지 ─── */
      this.loadingMessageIndex = this.messages.length;
      this.messages.push({from: 'bot', loading: true});
      this.scrollToBottom();

      /* ─── 모달 초기화 ─── */
      this.showVisModal = this.showPdfModal = this.showMapModal = false;
      this.visResult = this.pdfResult = this.mapResult = {};

      try {
        const res = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({query: text}),
        });

        const ctype = res.headers.get('content-type') || '';

        /* ───────── ① SSE (실시간) ───────── */
        if (ctype.includes('text/event-stream')) {
          this.removeLoadingMessage();
          await this.consumeSSE(res);
          return;
        }

        /* ───────── ② JSON(완결형 또는 기능 반환) ───────── */
        const {functionNo, data} = await res.json();
        this.removeLoadingMessage();

        switch (Number(functionNo)) {
          case 1:   // 시각화
            this.messages.push({from: 'bot', text: '📊 데이터 시각화를 생성했습니다.'});
            this.showVisModal = true;
            this.$nextTick(() => (this.visResult = data));
            break;

          case 2:   // PDF
            this.showPdfModal = true;
            this.$nextTick(() => (this.pdfResult = data));
            break;

          case 3:   // 지도
            this.messages.push({from: 'bot', text: '🗺️ 화재 예측 지도를 생성했습니다.'});
            this.showMapModal = true;
            this.$nextTick(() => (this.mapResult = data));
            break;

          case 4:   // 마크다운 문자열
            this.pushTypewriterMarkdown(data.message || data.text || '');
            break;

          default:
            this.messages.push({from: 'bot', text: `알 수 없는 기능번호(${functionNo})`});
        }
      } catch (err) {
        console.error(err);
        this.removeLoadingMessage();
        this.messages.push({from: 'bot', text: '서버 호출 실패'});
      }

      this.scrollToBottom();
    },

    /* ---------------------------------------------------------- */
    /* JSON 완결형 → 타자기 출력                                   */
    /* ---------------------------------------------------------- */
    pushTypewriterMarkdown(raw) {
      const idx = this.messages.push({from: 'bot', html: ''}) - 1;
      let i = 0;
      const step = () => {
        if (i <= raw.length) {
          this.messages[idx].html = md.render(raw.slice(0, i++));
          this.scrollToBottom();
          setTimeout(step, STEP_MS);
        }
      };
      step();
    },

    /* ---------------------------------------------------------- */
    /*  SSE 실시간 소비 (줄바꿈 복원)                              */
    /* ---------------------------------------------------------- */
    async consumeSSE(res) {
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let idx = null;   // 메시지 버블 인덱스
      let raw = '';     // 누적 텍스트
      let buffer = '';  // 청크 버퍼

      while (true) {
        const {value, done} = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, {stream: true});

        /* SSE 프로토콜은 \n\n 로 메시지를 구분 */
        let lines = buffer.split('\n\n');
        buffer = lines.pop();       // 남은 찌꺼기

        for (const line of lines) {
          if (!line.startsWith('data:')) continue;
          const payload = line.replace(/^data:\s*/, '');

          if (payload === '[DONE]') {
            this.scrollToBottom();
            return;
          }

          /* --- 핵심: 빈 data: 는 실제 개행으로 바꿔 줌 --- */
          raw += payload === '' ? '\n' : payload;

          /* 버블이 아직 없으면 생성 */
          if (idx === null) {
            idx = this.messages.push({from: 'bot', html: ''}) - 1;
          }
          this.messages[idx].html = md.render(raw);

          // 실시간으로 스크롤
          this.$nextTick(() => this.scrollToBottom());
        }
      }
    },

    /* ---------------------------------------------------------- */
    /* util                                                       */
    /* ---------------------------------------------------------- */
    removeLoadingMessage() {
      if (
          this.loadingMessageIndex >= 0 &&
          this.loadingMessageIndex < this.messages.length
      ) {
        this.messages.splice(this.loadingMessageIndex, 1);
      }
      this.loadingMessageIndex = -1;
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const messagesEl = this.$refs.messages;
        if (messagesEl) {
          messagesEl.scrollTop = messagesEl.scrollHeight;
        }
      });
    },

    /* 모달 close */
    onVisModalClose() {
      this.showVisModal = false;
    },
    onPdfModalClose() {
      this.showPdfModal = false;
      if (this.pdfResult.download_url) {
        this.messages.push({
          from: 'bot',
          pdf: true,
          filename: this.pdfResult.pdf_filename,
          url: this.pdfResult.download_url,
        });
      }
    },
    onMapModalClose() {
      this.showMapModal = false;
    },
  },

  /* 초기 쿼리 */
  created() {
    const init = this.$route.query.q;
    if (init) this.sendMessage(init);
  },
};
</script>

<style scoped>
/* 전체 레이아웃 -------------------------------------------------- */
.chat-page {
  position: relative;
  height: 100vh;
  background: #F8F9FA;
  overflow: hidden;
}

/* 메시지 리스트 -------------------------------------------------- */
.messages {
  position: absolute;
  top: 144px;
  bottom: 0;
  left: 0;
  right: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  padding-bottom: 280px; /* 입력창과 겹치지 않도록 충분한 여백 */
  max-width: 900px; /* 전체 폭 증가 */
  margin: 0 auto;
}

/* 메시지 래퍼 (정렬용) -------------------------------------------- */
.message-wrapper {
  display: flex;
  width: 100%;
}

.message-wrapper.user {
  justify-content: flex-end; /* 사용자 메시지는 오른쪽 */
}

.message-wrapper.bot {
  justify-content: flex-start; /* 봇 메시지는 왼쪽 */
}

/* 메시지 버블 --------------------------------------------------- */
.message {
  max-width: 70%; /* 화면의 70%까지 차지 가능 */
  min-width: 120px;
  padding: 16px 20px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.message.user {
  background: #007AFF;
  color: white;
  border-bottom-right-radius: 6px; /* 말풍선 효과 */
}

.message.bot {
  background: #FFFFFF;
  color: #333333;
  border: 1px solid #E1E5E9;
  border-bottom-left-radius: 6px; /* 말풍선 효과 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

/* 플레인 텍스트 스타일 ------------------------------------------ */
.plain-text {
  margin: 0;
  white-space: pre-wrap;
}

/* 마크다운 스타일 개선 ------------------------------------------ */
.markdown-content {
  /* 기본 스타일 리셋 */
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin: 0 0 12px 0;
  font-weight: 600;
  color: #1a1a1a;
}

.markdown-content h1 {
  font-size: 24px;
  border-bottom: 2px solid #e1e5e9;
  padding-bottom: 8px;
}

.markdown-content h2 {
  font-size: 20px;
  border-bottom: 1px solid #e1e5e9;
  padding-bottom: 6px;
}

.markdown-content h3 {
  font-size: 18px;
}

.markdown-content h4 {
  font-size: 16px;
}

.markdown-content p {
  margin: 0 0 12px 0;
  white-space: pre-wrap;
}

.markdown-content ul,
.markdown-content ol {
  margin: 8px 0 12px 0;
  padding-left: 20px;
}

.markdown-content li {
  margin: 4px 0;
}

.markdown-content strong {
  font-weight: 600;
  color: #1a1a1a;
}

.markdown-content em {
  font-style: italic;
}

.markdown-content code {
  background: #f6f8fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 85%;
}

.markdown-content pre {
  background: #f6f8fa;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-content pre code {
  background: none;
  padding: 0;
}

.markdown-content blockquote {
  border-left: 4px solid #d1d9e0;
  padding-left: 16px;
  margin: 12px 0;
  color: #656d76;
  font-style: italic;
}

.markdown-content a {
  color: #0969da;
  text-decoration: none;
}

.markdown-content a:hover {
  text-decoration: underline;
}

.markdown-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #d1d9e0;
  padding: 8px 12px;
  text-align: left;
}

.markdown-content th {
  background: #f6f8fa;
  font-weight: 600;
}

/* PDF 다운로드 버튼 ---------------------------------------------- */
.pdf-download {
  display: flex;
}

.pdf-btn {
  background: #f6f8fa;
  border: 1px solid #d1d9e0;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pdf-btn:hover {
  background: #e1e5e9;
}

/* 입력창 폭/위치 ------------------------------------------------ */
.chat-input {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 40px;
  max-width: 900px; /* 메시지와 동일한 폭 */
  margin: 0 auto;
  z-index: 10;
}

/* 스크롤바 스타일 (선택사항) ------------------------------------- */
.messages::-webkit-scrollbar {
  width: 6px;
}

.messages::-webkit-scrollbar-track {
  background: transparent;
}

.messages::-webkit-scrollbar-thumb {
  background: #d1d9e0;
  border-radius: 3px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background: #b8c2cc;
}

/* 반응형 대응 --------------------------------------------------- */
@media (max-width: 768px) {
  .messages {
    padding: 16px 12px;
    padding-bottom: 280px;
  }

  .message {
    max-width: 85%;
    font-size: 14px;
    padding: 12px 16px;
  }

  .markdown-content h1 {
    font-size: 20px;
  }

  .markdown-content h2 {
    font-size: 18px;
  }

  .markdown-content h3 {
    font-size: 16px;
  }
}
</style>