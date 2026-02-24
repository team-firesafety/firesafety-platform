<template>
  <!-- overlay 자체가 배경(본문)을 어둡게 함 -->
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- KakaoMap 이 소방서 좌표를 받아 자동센터링 -->
      <KakaoMap :buildings="data.buildings" :station="data.station" />
    </div>
  </div>
</template>

<script>
import KakaoMap from '@/components/KakaoMap.vue';

export default {
  name       : 'ModalMap',
  components : { KakaoMap },
  props      : { data: { type: Object, required: true } }
};
</script>

<style scoped>
.modal-overlay{
  position:fixed;inset:0;z-index:1000;
  background:rgba(0,0,0,.6);
  display:flex;align-items:center;justify-content:center;
}
.modal-content{
  width:90vw;height:90vh;max-width:1400px;
  background:#fff;border-radius:12px;
  overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.25);
}
</style>
