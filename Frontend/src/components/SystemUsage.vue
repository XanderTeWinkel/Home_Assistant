<script setup lang="ts">
import { onMounted, onBeforeUnmount } from "vue";
import { useSystemStore } from "../composables/system";

import UsageDial from "../components/UsageDial.vue";
import SmallStatCard from "../components/SmallStatCard.vue";

const store = useSystemStore();

onMounted(() => {
  if (!store.hasFetched) {
    store.fetchSystemInfo();
  }
  store.startAutoUpdate(1000);
});

onBeforeUnmount(() => {
  store.stopAutoUpdate();
});

const info = store.info;
</script>

<template>
  <div class="system-info-dashboard">
    <h2>System Usage</h2>

    <!-- CPU / Memory / Disk -->
    <div class="cards-row top-row">
      <UsageDial label="CPU" :value="info.cpu" />
      <UsageDial label="Memory" :value="info.memory" />
      <UsageDial label="Disk" :value="info.disk" />
    </div>

    <!-- Processes & Network -->
    <div class="cards-row bottom-row">
      <SmallStatCard label="Processes" :value="info.process_count" />

      <SmallStatCard label="Network">
        <template #default>
          <div class="net">
            <div>↑ {{ (info.network.bytes_sent / 1024 / 1024).toFixed(1) }} MB</div>
            <div>↓ {{ (info.network.bytes_recv / 1024 / 1024).toFixed(1) }} MB</div>
          </div>
        </template>
      </SmallStatCard>
    </div>
  </div>
</template>

<style scoped>
.system-info-dashboard {
  font-family: sans-serif;
  padding: 1rem;
}

h2 {
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

.net {
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.3;
  text-align: center;
}
</style>
