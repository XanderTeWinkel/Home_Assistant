<template>
  <div class="file-explorer">
    <h2>File Explorer</h2>

    <!-- Breadcrumb -->
    <div class="breadcrumb">
      <span
        v-for="(part, i) in currentPath.split('/').filter(Boolean)"
        :key="i"
      >
        / {{ part }}
      </span>
    </div>

    <button
      class="back-btn"
      v-if="currentPath !== '/Plex/'"
      @click="fetchFiles('/Plex/')"
    >
      ⬅ Back to root
    </button>

    <!-- Loading skeleton -->
    <div v-if="loading" class="loading">
      <div class="skeleton" v-for="n in 8" :key="n"></div>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-box">
      ⚠️ {{ error }}
    </div>

    <!-- Files -->
    <div v-if="!loading && !error" class="file-grid">
      <div
        v-for="file in files"
        :key="file.path"
        class="file-card"
        @click="openFolder(file)"
      >
        <div class="icon">
          <span v-if="file.isDirectory">📁</span>
          <span v-else>📄</span>
        </div>
        <div class="name">{{ file.name }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface FileItem {
  name: string
  path: string
  isDirectory: boolean
}

// Backend URL
const backendUrl = import.meta.env.VITE_BACKEND_URL

const files = ref<FileItem[]>([])
const currentPath = ref<string>('/Plex/')
const loading = ref<boolean>(false)
const error = ref<string | null>(null)

const fetchFiles = async (path: string = '/Plex/') => {
  loading.value = true
  error.value = null

  try {
    const res = await fetch(
      `${backendUrl}/files?path=${encodeURIComponent(path)}`
    )
    const data = await res.json()

    if (data.error) throw new Error(data.error)

    files.value = data
    currentPath.value = path
  } catch (err: any) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const openFolder = (file: FileItem) => {
  if (!file.isDirectory) return

  let newPath = file.path
  if (!newPath.endsWith('/')) newPath += '/'

  fetchFiles(newPath)
}

onMounted(() => {
  fetchFiles('/Plex/')
})
</script>

<style scoped>
.file-explorer {
  font-family: sans-serif;
  padding: 1rem;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  text-align: center;
}

/* Breadcrumb */
.breadcrumb {
  font-size: 0.85rem;
  color: #555;
  margin-bottom: 0.5rem;
}

/* Back button */
.back-btn {
  background: #eee;
  padding: 8px 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #ddd;
}

/* Loading skeleton */
.loading .skeleton {
  height: 20px;
  background: linear-gradient(90deg, #eee, #f5f5f5, #eee);
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
  margin: 6px 0;
}

@keyframes shimmer {
  0% {
    background-position: -150px 0;
  }
  100% {
    background-position: 150px 0;
  }
}

/* Error box */
.error-box {
  background: #fee2e2;
  color: #991b1b;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 1rem;
}

/* File grid */
.file-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
}

.file-card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.25s, box-shadow 0.25s;
}

.file-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.icon {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
}

.name {
  font-size: 0.95rem;
  font-weight: 600;
  word-break: break-all;
}
</style>
