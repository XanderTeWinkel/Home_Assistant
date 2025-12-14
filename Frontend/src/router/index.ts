import { createRouter, createWebHistory } from 'vue-router'
// Import views for login and registration
import Login from '../views/LoginView.vue'
import Register from '../views/RegisterView.vue'

// Import views for routes visible in sidebar
import Home from '../views/HomeView.vue'
import Profile from '../views/ProfileView.vue'
import People from '../views/PeopleView.vue'
import Chat from '../views/ChatView.vue'
import FileManagement from '../views/FileManagementView.vue'
import SystemUsage from '../views/SystemUsageView.vue'
import Settings from '../views/SettingsView.vue'

// import views for routes not visible in sidebar
import Spotify from '../views/SpotifyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  // Define routes
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    },
    {
      path: '/people',
      name: 'people',
      component: People
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
    },
    {
      path: '/settings',
      name: 'settings',
      component: Settings
    }
  ]

})
export default router
