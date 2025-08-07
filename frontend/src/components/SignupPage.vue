<template>
  <div class="signup-container">
    <div class="signup-form">
      <h1 class="signup-title">회원가입</h1>
      
      <form @submit.prevent="handleSignup" class="form">
        <div class="input-group">
          <input
            v-model="signupData.id"
            type="text"
            placeholder="아이디"
            class="input-field"
            required
          />
        </div>
        
        <div class="input-group">
          <input
            v-model="signupData.password"
            type="password"
            placeholder="비밀번호"
            class="input-field"
            required
          />
        </div>
        
        <div class="input-group">
          <input
            v-model="signupData.passwordConfirm"
            type="password"
            placeholder="비밀번호 확인"
            class="input-field"
            required
            :class="{ 'error': passwordMismatch }"
          />
          <span v-if="passwordMismatch" class="error-message">
            비밀번호가 일치하지 않습니다.
          </span>
        </div>
        
        <div class="input-group">
          <input
            v-model="signupData.fireStation"
            type="text"
            placeholder="소속 소방서"
            class="input-field"
            required
          />
        </div>
        
        <button type="submit" class="signup-button" :disabled="!isFormValid">
          로그인
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignupPage',
  data() {
    return {
      signupData: {
        id: '',
        password: '',
        passwordConfirm: '',
        fireStation: ''
      }
    }
  },
  computed: {
    passwordMismatch() {
      return this.signupData.passwordConfirm && 
             this.signupData.password !== this.signupData.passwordConfirm
    },
    isFormValid() {
      return this.signupData.id && 
             this.signupData.password && 
             this.signupData.passwordConfirm && 
             this.signupData.fireStation &&
             !this.passwordMismatch
    }
  },
  methods: {
    handleSignup() {
      if (this.isFormValid) {
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('userId', this.signupData.id)
        this.$router.push({ name: 'Main' })
      }
    }
  }
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #F5F6FA;
}

.signup-form {
  background: white;
  padding: 60px 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.signup-title {
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
  position: relative;
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

.input-field.error {
  border-color: #ff4444;
}

.error-message {
  color: #ff4444;
  font-size: 12px;
  margin-top: 5px;
}

.signup-button {
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

.signup-button:hover:not(:disabled) {
  background-color: #1e36cc;
}

.signup-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>