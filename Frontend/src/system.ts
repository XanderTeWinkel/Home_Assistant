// src/store/system.ts
import { defineStore } from 'pinia';
import { reactive } from 'vue';
import { ref } from 'vue';

export interface NetworkInfo {
  bytes_sent: number;
  bytes_recv: number;
}

export interface SystemInfo {
  cpu: number;
  memory: number;
  disk: number;
  process_count: number;
  network: NetworkInfo;
}

export const useSystemStore = defineStore('system', () => {
  const info = reactive<SystemInfo>({
    cpu: 0,
    memory: 0,
    disk: 0,
    process_count: 0,
    network: { bytes_sent: 0, bytes_recv: 0 }
  });

  const hasFetched = ref(false);
  let intervalId: number | null = null;

  const fetchSystemInfo = async () => {
    try {
      const res = await fetch('http://localhost:5000/system-info');
      const data = await res.json();

      // Update reactive object properties individually
      info.cpu = data.cpu;
      info.memory = data.memory;
      info.disk = data.disk;
      info.process_count = data.process_count;
      info.network.bytes_sent = data.network.bytes_sent;
      info.network.bytes_recv = data.network.bytes_recv;

      hasFetched.value = true;
    } catch (err) {
      console.error('Failed to fetch system info:', err);
    }
  };

  const startAutoUpdate = (ms: number = 500) => {
    if (intervalId) return;
    intervalId = window.setInterval(fetchSystemInfo, ms);
  };

  const stopAutoUpdate = () => {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  };

  return { info, hasFetched, fetchSystemInfo, startAutoUpdate, stopAutoUpdate };
});