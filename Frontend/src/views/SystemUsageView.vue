<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount } from 'vue';
import { useSystemStore } from '../composables/system';

export default defineComponent({
  name: 'SystemUsage',
  setup() {
    const systemStore = useSystemStore();

    onMounted(() => {
      if (!systemStore.hasFetched) {
        systemStore.fetchSystemInfo();
      }
      systemStore.startAutoUpdate(1000); // auto-refresh every 1s
    });

    onBeforeUnmount(() => {
      systemStore.stopAutoUpdate(); // cleanup
    });

    const getColor = (value: number): string => {
      if (value < 50) return '#10b981';
      if (value < 75) return '#f59e0b';
      return '#ef4444';
    };

    return {
      info: systemStore.info,
      getColor
    };
  }
});
</script>



<template>
  <div class="system-info-dashboard">
    <h2>System Usage</h2>

    <!-- Top row: CPU, Memory, Disk -->
    <div class="cards-row top-row">
      <div class="card">
        <div class="dial">
          <svg viewBox="0 0 36 36">
            <path class="bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path 
              class="progress" 
              :stroke="getColor(info.cpu)" 
              :stroke-dasharray="info.cpu + ', 100'" 
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
            />
            <text x="18" y="20.35" class="dial-text" transform="rotate(90,18,18)">{{ info.cpu }}%</text>
          </svg>
        </div>
        <div class="card-title">CPU</div>
      </div>

      <div class="card">
        <div class="dial">
          <svg viewBox="0 0 36 36">
            <path class="bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path 
              class="progress" 
              :stroke="getColor(info.memory)" 
              :stroke-dasharray="info.memory + ', 100'" 
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
            />
            <text x="18" y="20.35" class="dial-text" transform="rotate(90,18,18)">{{ info.memory }}%</text>
          </svg>
        </div>
        <div class="card-title">Memory</div>
      </div>

      <div class="card">
        <div class="dial">
          <svg viewBox="0 0 36 36">
            <path class="bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path 
              class="progress" 
              :stroke="getColor(info.disk)" 
              :stroke-dasharray="info.disk + ', 100'" 
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
            />
            <text x="18" y="20.35" class="dial-text" transform="rotate(90,18,18)">{{ info.disk }}%</text>
          </svg>
        </div>
        <div class="card-title">Disk</div>
      </div>
    </div>

    <!-- Bottom row: Processes, Network -->
    <div class="cards-row bottom-row">
      <div class="card small-card">
        <div class="stat">{{ info.process_count }}</div>
        <div class="card-title">Processes</div>
      </div>

      <div class="card small-card">
        <div class="stat">
          <div>↑ {{ (info.network.bytes_sent / 1024 / 1024).toFixed(1) }} MB</div>
          <div>↓ {{ (info.network.bytes_recv / 1024 / 1024).toFixed(1) }} MB</div>
        </div>
        <div class="card-title">Network</div>
      </div>
    </div>
  </div>
</template>



<style>
.system-info-dashboard {
  font-family: sans-serif;
  padding: 1rem;
}

.system-info-dashboard h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  text-align: center;
}

.cards-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 1rem;
}

.top-row {
  margin-bottom: 2rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  width: 160px;
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}

.small-card {
  width: 140px;
  height: 140px;
}

.card-title {
  margin-top: 0.5rem;
  font-weight: 600;
  text-align: center;
}

.stat {
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
}

.dial {
  width: 80px;
  height: 80px;
}

.dial svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.dial path.bg {
  fill: none;
  stroke: #eee;
  stroke-width: 4;
}

.dial path.progress {
  fill: none;
  stroke-width: 4;
  stroke-linecap: round;
  transition: stroke-dasharray 1s ease, stroke 0.5s ease;
}

.dial-text {
  fill: #111;
  font-size: 0.6rem;
  text-anchor: middle;
  dominant-baseline: middle;
}
</style>