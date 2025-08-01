<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- 지도 결과 -->
      <div class="map-container">
        <!-- 예: <MapComponent :points="data.points" /> -->
        <slot :data="data"></slot>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from './Loading.vue';

export default {
  name: 'ModalMap',
  components: { Loading },
  props: {
    data: { type: Object, required: true },
    functionNo: { type: Number, required: true }
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6); /* 뒤를 어둡게 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 90vw;            /* 화면 가로의 90% */
  height: 90vh;           /* 화면 세로의 90% */
  background: #ffffff;    /* 흰색 배경 */
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  overflow-y: auto;       /* 내용이 길면 스크롤 */
}
</style>