<template>
  <div class="chat-input" :style="{ bottom }">
    <textarea
      v-model="text"
      @keydown.enter.prevent="onSend"
      placeholder="소담에게 물어보세요."
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
    return { text: '' }
  },
  methods: {
    onSend() {
      const t = this.text.trim()
      if (!t) return
      this.$emit('send', t)
      this.text = ''
    }
  }
}
</script>

<style scoped>
.chat-input {
  position: absolute;
  left: 510px;
  right: 510px;
  /* bottom comes from the inline style binding */
  height: 160px;
  background: #fff;
  border: 1px solid #E6E8EC;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.chat-input textarea {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  resize: none;
  padding: 16px;
  font-size: 16px;
  line-height: 1.5;
  color: #555;
  background: transparent;
  font-family: inherit;
}

.chat-input textarea::placeholder {
  color: #999;
}

.icon-group {
  position: absolute;
  bottom: 12px;
  left: 16px;
  display: flex;
  gap: 12px;
}

.icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}
</style>
