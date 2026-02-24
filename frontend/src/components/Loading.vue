# Loading.vue
<template>
  <div class="loading-dots">
    <div class="dot dot1"></div>
    <div class="dot dot2"></div>
    <div class="dot dot3"></div>
  </div>
</template>

<script>
export default {
  name: 'Loading',
};
</script>

<style scoped>
.loading-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin: 0;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: dotPulse 1.4s ease-in-out infinite both;
}

.dot1 {
  background-color: #0022FF;
  animation-delay: -0.32s;
}

.dot2 {
  background-color: #3248FF;
  animation-delay: -0.16s;
}

.dot3 {
  background-color: #5664FF;
  animation-delay: 0s;
}

@keyframes dotPulse {
  0%, 80%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>