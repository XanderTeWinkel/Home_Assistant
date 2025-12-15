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

  routes: [
    {
      path: '/',
      redirect: '/home'
    },

    // PUBLIC ROUTES
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

    // PROTECTED ROUTES
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/people',
      name: 'people',
      component: People,
      meta: { requiresAuth: true }
    },
    {
      path: '/spotify',
      name: 'spotify',
      component: Spotify,
      meta: { requiresAuth: true }
    },
    {
      path: '/chat',
      name: 'chat',
      component: Chat,
      meta: { requiresAuth: true }
    },
    {
      path: '/file-management',
      name: 'file-management',
      component: FileManagement,
      meta: { requiresAuth: true }
    },
    {
      path: '/system-usage',
      name: 'system-usage',
      component: SystemUsage,
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: Settings,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("access_token")

  // If route requires auth and user is not logged in
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: "login" })
  }
  // If user is logged in and tries to access login/register
  else if ((to.name === "login" || to.name === "register") && isAuthenticated) {
    next({ name: "home" })
  }
  else {
    next()
  }
})


export default router
