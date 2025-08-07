<template>
  <div
    class="chat-input"
    :class="{ 'has-preview': previewUrl }"
    :style="{ bottom }"
    @dragover.prevent
    @dragenter.prevent
    @drop.prevent="onDrop"
  >
    <!-- 이미지 미리보기 -->
    <div v-if="previewUrl" class="preview-wrapper">
      <img :src="previewUrl" alt="Preview" class="image-preview" />
      <button class="remove-btn" @click="removeImage">✕</button>
    </div>

    <textarea
      v-model="text"
      @keydown.enter="handleEnter"
      :placeholder="previewUrl ? '' : '소담에게 물어보세요.'"
      :class="{ 'with-preview': previewUrl }"
    />
    <div class="icon-group">
      <img src="@/assets/image-icon.png" alt="이미지 첨부" class="icon" />
      <img src="@/assets/doc-icon.png"   alt="문서 첨부" class="icon" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatInput',
  emits: ['send'],
  props: {
    /** CSS distance from the viewport bottom (e.g. "24px" or "160px") */
    bottom: {
      type: String,
      default: '24px'
    }
  },
  data() {
    return { 
      text: '',
      previewUrl: null,
      imageFile: null
    }
  },
  methods: {
    handleEnter(event) {
      // Shift + Enter는 줄바꿈을 허용
      if (event.shiftKey) {
        return; // 기본 동작(줄바꿈) 허용
      }
      // 일반 Enter는 전송
      event.preventDefault();
      this.onSend();
    },
    onSend() {
      const t = this.text.trim()
      console.log('ChatInput onSend - text:', JSON.stringify(t), 'length:', t.length)
      
      // 텍스트가 없으면 전송하지 않음
      if (!t) return
      
      // 텍스트와 이미지 정보를 함께 emit
      const messageData = {
        text: t,
        image: this.previewUrl ? {
          url: this.previewUrl,
          file: this.imageFile
        } : null
      }
      this.$emit('send', messageData)
      
      // 입력 초기화
      this.text = ''
      this.removeImage()
    },
    onDrop(event) {
      const file = event.dataTransfer.files[0]
      if (!file || !file.type.startsWith('image/')) return

      this.imageFile = file

      const reader = new FileReader()
      reader.onload = e => {
        this.previewUrl = e.target.result
      }
      reader.readAsDataURL(file)
    },
    removeImage() {
      this.previewUrl = null
      this.imageFile = null
    }
  }
}
</script>

<style scoped>
.chat-input {
  /* 위치는 부모에서 관리 */
  height: 160px;
  background: #fff;
  border: 1px solid #E6E8EC;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: height 0.2s ease;
}

/* 이미지 있는 경우 채팅창 높이 확장 */
.chat-input.has-preview {
  height: 180px; /* 200px에서 180px로 줄임 */
}

.chat-input textarea {
  position: absolute;
  top: 16px;
  left: 16px;
  right: 16px;
  bottom: 56px; /* 아이콘 영역(40px) + 여백(16px) 확보 */
  border: none;
  outline: none;
  resize: none;
  padding: 0;
  font-size: 16px;
  line-height: 1.5;
  color: #555;
  background: transparent;
  font-family: inherit;
  box-sizing: border-box;
}

.chat-input textarea.with-preview {
  top: 80px; /* 이미지 미리보기(60px) + 상단여백(16px) + 약간의 간격(4px) */
  bottom: 56px; /* 하단 아이콘 영역은 동일하게 유지 */
}

.chat-input textarea::placeholder {
  color: #999;
}

.icon-group {
  position: absolute;
  bottom: 16px; /* 하단 위치를 조금 더 올려서 패딩과 균형 맞춤 */
  left: 16px;
  display: flex;
  gap: 12px;
  z-index: 10; /* 텍스트 위에 표시되도록 z-index 추가 */
}

.icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

/* 이미지 미리보기 스타일 */
.preview-wrapper {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 60px;
  height: 60px;
}

.preview-wrapper .image-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.preview-wrapper .remove-btn {
  position: absolute;
  top: 0;
  right: 0;
  width: 20px;
  height: 20px;
  border: none;
  background: rgba(255,255,255,0.9);
  border-radius: 50%;
  font-size: 14px;
  line-height: 20px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
  z-index: 20;
}
</style>
