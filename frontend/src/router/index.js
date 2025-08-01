import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/components/MainPage.vue'
import ChatPage from '@/components/ChatPage.vue'

const routes = [
  { path: '/', name: 'Home', component: MainPage },
  { path: '/chat', name: 'Chat', component: ChatPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
