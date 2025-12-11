<template>
  <div class="card hourly" v-if="windowData.length">
    <div class="hourly-list">
      <div
        v-for="(h, i) in windowData"
        :key="i"
        :class="['hour-card', { current: h.isCurrent }]"
      >
        <div class="hour-temp">{{ h.temp }}°C</div>
        <div class="hour-icon">{{ icon }}</div>
        <div class="hour-time">
          {{ h.time.split("T")[1].slice(0, 2) }}:00
        </div>
        <div class="hour-precip">{{ h.precipitation }} mm</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  weather: { type: Object, required: true }
});

const icon = "☁️"; // simplified, could accept prop

// Compute a 13-hour sliding window centered on current hour
const windowData = computed(() => {
  const w = props.weather;
  if (!w) return [];

  const nowHour = new Date(w.time).getHours();
  const idx = w.hourly.time.findIndex(
    (t: string) => new Date(t).getHours() === nowHour
  );

  const start = Math.max(0, idx - 6);
  const end = start + 13;

  return w.hourly.temperature_2m.slice(start, end).map((temp: number, i: number) => {
    const actual = start + i;
    return {
      temp,
      time: w.hourly.time[actual],
      precipitation: w.hourly.precipitation[actual],
      isCurrent: actual === idx
    };
  });
});
</script>

<style scoped>
.card.hourly {
  width: 100%;
  overflow-x: auto;
  background: #ffffff;
  border-radius: 1rem;
  padding: 1rem;
  margin: 1rem;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
}

.hourly-list {
  display: flex;
  gap: 0.75rem;
  min-width: max-content;
}

.hour-card {
  background: #f9fafb;
  padding: 0.5rem;
  border-radius: 0.75rem;
  text-align: center;
  min-width: 4.5rem;
}

.hour-card.current {
  background: #9ea4b3;
  color: #ffffff;
  font-weight: bold;
}

.hour-temp {
  font-weight: 600;
}

.hour-icon {
  font-size: 1.5rem;
  margin: 0.25rem 0;
}

.hour-time,
.hour-precip {
  font-size: 0.75rem;
  color: #6b7280;
}
</style>
