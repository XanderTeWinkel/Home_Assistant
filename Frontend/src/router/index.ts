import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/HomeView.vue'
import Spotify from '../views/SpotifyView.vue'
import Chat from '../views/ChatView.vue'
import FileManagement from '../views/FileManagementView.vue'
import SystemUsage from '../views/SystemUsageView.vue'

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
      path: '/spotify',
      name: 'spotify',
      component: Spotify
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
