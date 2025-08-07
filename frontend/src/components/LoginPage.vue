<template>
  <div class="login-container">
    <div class="login-form">
      <img src="@/assets/login-title.png" alt="로그인" class="login-title-image" />
      
      <form @submit.prevent="handleLogin" class="form">
        <div class="input-group">
          <input
            v-model="credentials.id"
            type="text"
            placeholder="아이디"
            class="input-field"
            required
          />
        </div>
        
        <div class="input-group">
          <input
            v-model="credentials.password"
            type="password"
            placeholder="비밀번호"
            class="input-field"
            required
          />
        </div>
        
        <button type="submit" class="login-button">
          로그인
        </button>
      </form>
      
      <div class="links">
        <a href="#" class="link">아이디 찾기</a>
        <a href="#" class="link">비밀번호 찾기</a>
        <router-link to="/signup" class="link">회원가입</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import authStore from '@/store/auth.js'

export default {
  name: 'LoginPage',
  data() {
    return {
      credentials: {
        id: '',
        password: ''
      }
    }
  },
  methods: {
    handleLogin() {
      if (this.credentials.id && this.credentials.password) {
        authStore.login(this.credentials.id)
        this.$router.push({ name: 'Main' })
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #F5F6FA;
}

.login-form {
  width: 100%;
  max-width: 400px;
  padding: 0 20px;
}

.login-title-image {
  height: 40px;
  width: auto;
  display: block;
  margin: 0 auto 40px auto;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-field {
  padding: 16px;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  font-size: 16px;
  background-color: #F8F9FA;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: #2744FF;
}

.login-button {
  background-color: #2744FF;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.login-button:hover {
  background-color: #1e36cc;
}

.links {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.link {
  color: #777777;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.link:hover {
  color: #2744FF;
}
</style>