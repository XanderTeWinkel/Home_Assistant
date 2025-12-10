import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/HomeView.vue'
// @ts-ignore: no declaration file for .vue modules
import SystemUsage from '../views/SystemUsageView.vue'
// @ts-ignore: no declaration file for .vue modules
import FileManagement from '../views/FileManagementView.vue'

import Chat from '../views/ChatView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  // Define routes
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/chat',
      name: 'chat',
      component: Chat
    },
    {
      path: '/file-management',
      name: 'file-management',
      component: FileManagement
    },
    {
      path: '/system-usage',
      name: 'system-usage',
      component: SystemUsage
    }
  ]

})
export default router
