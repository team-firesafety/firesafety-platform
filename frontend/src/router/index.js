import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import ChatPage from '@/components/ChatPage.vue'
import LoginPage from '@/components/LoginPage.vue'
import SignupPage from '@/components/SignupPage.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginPage },
  { path: '/login', name: 'LoginRedirect', component: LoginPage },
  { path: '/signup', name: 'Signup', component: SignupPage },
  { path: '/main', name: 'Main', component: MainPage },
  { path: '/chat', name: 'Chat', component: ChatPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  if (!isLoggedIn && to.name !== 'Login' && to.name !== 'LoginRedirect' && to.name !== 'Signup') {
    next({ name: 'Login' })
  } else if (isLoggedIn && (to.name === 'Login' || to.name === 'LoginRedirect' || to.name === 'Signup')) {
    next({ name: 'Main' })
  } else {
    next()
  }
})

export default router
