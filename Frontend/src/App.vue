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
      </nav>
    </aside>

    <!-- Main content -->
    <div class="main-content">
      <header class="header">
        <h1>Citadel</h1>
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
}

.header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  
  /* background-color: #fff; */
  /* box-shadow: 0 2px 4px rgba(0,0,0,0.05); */
}

.header h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

.content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
}
</style>
