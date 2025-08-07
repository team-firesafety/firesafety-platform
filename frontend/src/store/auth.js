import { reactive } from 'vue'

const authStore = reactive({
  isLoggedIn: false,
  userId: '',
  
  init() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    const userId = localStorage.getItem('userId') || ''
    
    this.isLoggedIn = isLoggedIn
    this.userId = userId
  },
  
  login(userId) {
    this.isLoggedIn = true
    this.userId = userId
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userId', userId)
  },
  
  logout() {
    this.isLoggedIn = false
    this.userId = ''
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('userId')
  }
})

authStore.init()

export default authStore