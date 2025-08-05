<template>
  <aside class="sidebar">
    <!-- 1) 로고 + 서비스명 -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="소담 로고" class="logo" />
    </div>

    <!-- 2) 메인 네비게이션 -->
    <nav class="nav-menu">
      <ul>
        <li class="menu-item">
          <img src="@/assets/chat.png" alt="" class="menu-icon" />
          <span class="menu-text">새 채팅</span>
        </li>
        <li class="menu-item">
          <img src="@/assets/info.png" alt="" class="menu-icon" />
          <span class="menu-text">소담에 대해서</span>
        </li>
        <li class="menu-item menu-history">
          <img src="@/assets/history.png" alt="" class="menu-icon" />
          <span class="menu-text">채팅 기록</span>
        </li>
      </ul>
    </nav>

    <!-- 3) 채팅 기록 히스토리 -->
    <section class="history-list">
      <ul>
        <li
          v-for="(item, idx) in historyItems"
          :key="idx"
          class="history-item"
        >
          {{ item }}
        </li>
      </ul>
    </section>

    <!-- 4) 푸터 -->
    <div class="sidebar-footer">
      소방 업무 지원 챗봇 v1.0
    </div>
  </aside>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      historyItems: [
        '화재 예방 점검 절차',
        '화재 신고 접수 절차',
        '화재 예방 점검 절차',
        '화재 신고 접수 절차',
        '화재 예방 점검 절차'
      ]
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 340px;    /* 사이드바 폭 */
  height: 100vh;   /* 뷰포트 전체 높이 */
  background: #fff;
  display: flex;
  flex-direction: column;
  z-index: 100;    /* (필요 시) 다른 요소 위로 띄우려면 추가 */
}

/* -------------------------------------------------- */
/* 1) 로고 영역                                        */
/* -------------------------------------------------- */
.logo-container {
  display: flex;
  align-items: center;
  margin-left: 15px;   /* ← 로고 왼쪽 여백 */
  margin-top: 40px;    /* ← 로고 상단 여백 */
  margin-bottom: 30px; /* ← 로고와 첫 메뉴 간격 */
}
.logo {
  height: 50px;
  width: auto;
}
.service-name {
  margin-left: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #0022ff;
}

/* -------------------------------------------------- */
/* 2) 네비게이션 메뉴                                 */
/*    - 텍스트 크기 모두 16px                          */
/*    - 아이콘(chat.png, logo.png, history.png) 배치  */
/* -------------------------------------------------- */
.nav-menu ul {
  list-style: none;
  margin: 0;
  padding: 0 0 0 20px;   /* ← 메뉴 왼쪽 들여쓰기 */
  margin-bottom: var(--nav-history-gap, 0px);
}

.menu-item {
  display: flex;
  align-items: center;
  font-size: 16px;        /* ← 메뉴 글자 크기 */
  color: #333333;
  cursor: pointer;
  margin-bottom: var(--menu-item-gap, 20px);  /* ← 메뉴 항목 간 간격 */
  margin-left: 20px;
}

.menu-history {
  margin-top: 50px;    /* records 항목만 아래로 추가 밀기 */
  margin-bottom: 10;    /* 필요시 조정 */
}

.menu-icon {
  width: 20px;
  height: 20px;
  margin-right: var(--icon-text-gap, 8px);   /* ← 아이콘과 텍스트 간격 */
}

/* -------------------------------------------------- */
/* 3) 히스토리 리스트                                  */
/*    - 히스토리 항목 간격 16px                         */
/* -------------------------------------------------- */
.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 20px;        /* ← 히스토리 좌우 여백 */
}
.history-item {
  font-size: 16px;        /* ← 히스토리 글자 크기 */
  color: #333333;
  margin-bottom: 20px;    /* ← 히스토리 항목 간 간격 (16px 고정) */
}

/* -------------------------------------------------- */
/* 4) 푸터                                            */
/* -------------------------------------------------- */
.sidebar-footer {
  height: 60px;           /* ← 푸터 높이 (60px 고정) */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;        /* ← 푸터 글자 크기 */
  font-weight: 300;       /* ← 푸터 글자 두께 */
  color: #777777;
  border-top: 1px solid #e1e5e9;
}

.nav-menu ul,
.history-list ul {
  list-style: none;    /* 불렛 제거 */
  padding: 0;          /* 좌우 기본 패딩 제거 */
  margin: 0;           /* 기본 마진 제거 */
}
</style>
