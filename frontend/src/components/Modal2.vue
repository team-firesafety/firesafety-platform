<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- 완료 후 다운로드 버튼 -->
      <button class="download-btn" @click="onDownload">
        <span class="icon-wrapper">
          <span class="arrow">↓</span>
          <span class="underline"></span>
        </span>
        <span class="label">{{ filename }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import Loading from './Loading.vue';

export default {
  name: 'Modal2',
  components: { Loading },
  props: {
    data: { type: Object, required: true },
    functionNo: { type: Number, required: true }
  },
  computed: {
    filename() {
      return this.data.pdf_filename || '문서.pdf';
    }
  },
  methods: {
    onDownload() {
      if (this.data.download_url) {
        let downloadUrl = this.data.download_url;
        if (downloadUrl.startsWith('/pdf/')) {
          downloadUrl = `http://localhost:8000${downloadUrl}`;
        }

        // 방법 1: a 태그를 동적으로 생성해서 다운로드 강제
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = this.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // 방법 2: 만약 위 방법이 안되면 이걸 사용하세요
        // window.location.href = this.data.download_url;
      }
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}

.modal-content {
  /* 자동 크기 + 중앙 정렬 */
  background: #fff;
  border-radius: 24px;
  display: flex; align-items: center; justify-content: center;
  padding: 0; overflow: hidden;
}

/* 다운로드 버튼 */
.download-btn {
  width: 174px; height: 80px;
  background: #ffffff; border: none;
  border-radius: 24px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  display: inline-flex; align-items: center;
  justify-content: center;
  font-size: 20px; font-weight: 500;
  color: #000; cursor: pointer;
}
.download-btn .icon-wrapper { display: flex; flex-direction: column; align-items: center; margin-right: 8px; }
.download-btn .underline { width: 16px; height: 2px; background: currentColor; margin-top: 4px; display: block; }
</style>