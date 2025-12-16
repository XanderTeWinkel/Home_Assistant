<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const isAuthPage = computed(() => route.name === "login" || route.name === "register");

const username = ref("");
const mobileSidebarOpen = ref(false);

// Fetch username
const token = localStorage.getItem("access_token");
if (token) {
  const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL,
    headers: { Authorization: `Bearer ${token}` },
  });

  onMounted(async () => {
    try {
      const res = await api.get("/auth/me");
      username.value = res.data.username;
    } catch {
      console.error("Failed to load user info.");
    }
  });
}
</script>


<template>
  <div id="app">
    <!-- Sidebar -->
    <aside class="sidebar" v-if="!isAuthPage" :class="{ open: mobileSidebarOpen }">
      <nav class="sidebar-nav">
        <router-link @click="mobileSidebarOpen = false" to="/home" class="nav-link">Home</router-link>
        <router-link @click="mobileSidebarOpen = false" to="/people" class="nav-link">People</router-link>
        <router-link @click="mobileSidebarOpen = false" to="/chat" class="nav-link">AI Chat</router-link>
        <router-link @click="mobileSidebarOpen = false" to="/file-management" class="nav-link">Files</router-link>
        <router-link @click="mobileSidebarOpen = false" to="/system-usage" class="nav-link">System Usage</router-link>
        <router-link @click="mobileSidebarOpen = false" to="/settings" class="nav-link">Settings</router-link>
      </nav>
    </aside>


    <!-- Main content -->
    <div class="main-content">
      <header class="header" v-if="!isAuthPage">
        <div class="header-left">
          <!-- Mobile menu button -->
          <button class="menu-btn" @click="mobileSidebarOpen = !mobileSidebarOpen">
            ☰
          </button>

          <span class="app-name">Citadel</span>
        </div>

        <div class="header-right">
          <router-link to="/profile" class="avatar-link">
            <div class="avatar">
              {{ username ? username.charAt(0).toUpperCase() : "C" }}
            </div>
          </router-link>
        </div>
      </header>

      <main class="content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Layout */
#app {
  display: flex;
  width: 100vw;
  height: 100vh;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #eaecf0;
  color: #333;
}

/* Sidebar */
.sidebar {
  width: 175px;
  background-color: #1f2937;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  /* border-bottom: 1px solid #374151; */
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.nav-link {
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  color: #d1d5db;
  text-decoration: none;
  transition: background-color 0.2s, color 0.2s;
}

.nav-link:hover {
  background-color: #374151;
  color: #fff;
}

.nav-link.active {
  background-color: #4b5563;
  color: #fff;
}

/* Main content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;

  height: 100vh;
  background-color: #f8fafc;
}

.header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 0 2rem;

  background-color: #f8fafc;

  border-bottom: 1px solid rgba(15, 23, 42, 0.08);

  box-shadow:
    0 1px 0 rgba(15, 23, 42, 0.04),
    0 8px 24px rgba(15, 23, 42, 0.04);
}


.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-left::after {
  content: "";
  margin-left: 1rem;
  width: 1px;
  height: 24px;
  background: rgba(0, 0, 0, 0.08);
}


.app-name {
  font-size: 2.35rem;
  font-weight: 700;
  letter-spacing: 0.6px;

  background: linear-gradient(135deg, #111827, #4f46e5);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;

  text-transform: none;
}


.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.icon-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}

.avatar-link {
  display: inline-flex;
  text-decoration: none;
}

.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}

/* ============================= */
/* Responsive / Mobile Styles   */
/* ============================= */

.menu-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.4rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

/* Tablet and below */
@media (max-width: 1024px) {
  .sidebar {
    width: 150px;
  }

  .app-name {
    font-size: 1.8rem;
  }
}

/* Mobile */
@media (max-width: 768px) {
  #app {
    flex-direction: column;
    height: 100dvh;
  }

  .menu-btn {
    display: inline-flex;
  }

  /* Sidebar becomes off-canvas */
  .sidebar {
    position: fixed;
    top: 64px;
    left: 0;
    height: calc(100vh - 64px);
    width: 220px;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    z-index: 50;
  }

  .sidebar.open {
    transform: translateX(0);
  }

  .main-content {
    width: 100%;
  }

  .header {
    padding: 0 1rem;
  }

  .header-left::after {
    display: none;
  }

  .app-name {
    font-size: 1.4rem;
  }

  .content {
    padding: 1rem;
  }
}

/* Small phones */
@media (max-width: 480px) {
  .avatar {
    width: 30px;
    height: 30px;
    font-size: 0.75rem;
  }

  .nav-link {
    padding: 0.6rem 0.75rem;
    font-size: 0.9rem;
  }

  .content {
    padding: 0.75rem;
  }
}
</style>
