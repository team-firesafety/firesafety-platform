<template>
  <div class="login-container">
    <div class="login-form">
      <h1 class="login-title">로그인</h1>
      
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
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('userId', this.credentials.id)
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
  background: white;
  padding: 60px 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-size: 32px;
  font-weight: 600;
  color: #2744FF;
  text-align: center;
  margin-bottom: 40px;
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