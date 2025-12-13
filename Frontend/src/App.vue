<script setup lang="ts">
// Vue Router hooks
import { useRouter, useRoute } from "vue-router";

// Initialize router and route
const router = useRouter();
const route = useRoute();
</script>



<template>
  <!-- < backend_test /> -->
  <div id="app">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">

      </div>
      <nav class="sidebar-nav">
        <router-link to="/home" class="nav-link" active-class="active">Home</router-link>
        <router-link to="/spotify" class="nav-link" active-class="active">Spotify</router-link>
        <router-link to="/chat" class="nav-link" active-class="active">AI Chat</router-link>
        <router-link to="/file-management" class="nav-link" active-class="active">Files</router-link>
        <router-link to="/system-usage" class="nav-link" active-class="active">System Usage</router-link>
        <router-link to="/settings" class="nav-link" active-class="active">Settings</router-link>
      </nav>
    </aside>

    <!-- Main content -->
    <div class="main-content">
      <header class="header">
        <div class="header-left">
          <span class="app-name">Citadel</span>
        </div>

        <div class="header-right">
          <div class="avatar">C</div>
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



.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}
</style>
