<template>
  <header class="header">
    <img src="@/assets/logo.png" alt="LOGO" class="logo" />
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
}
</script>

<style scoped>
.header {
  /* 절대 위치로 화면 최상단에 고정 */
  position: absolute;
  top: 80px;      /* 상단에서 80px */
  left: 0;
  width: 100%;
  height: 64px;
  display: flex;
  align-items: center;
  background: transparent;
  z-index: 10;
}
.logo {
  /* 절대 위치 헤더의 왼쪽에서 340px */
  margin-left: 340px;
  height: 48px;
  width: auto;
}
</style>
