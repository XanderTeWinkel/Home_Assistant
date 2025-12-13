<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  weather: { type: Object, required: true }
});

// Helper function to get emoji based on description
function getIcon(desc: string) {
  if (!desc) return "🌡️";
  if (desc.includes("Clear")) return "☀️";
  if (desc.includes("Cloud")) return "☁️";
  if (desc.includes("Rain") || desc.includes("drizzle")) return "🌧️";
  if (desc.includes("Snow")) return "❄️";
  if (desc.includes("Thunderstorm")) return "⛈️";
  if (desc.includes("Fog")) return "🌫️";
  return "🌡️";
}

// Compute a 7-hour window: 2 before, current, 4 after
const windowData = computed(() => {
  const w = props.weather;
  if (!w) return [];

  const now = new Date(w.time);
  const nowHour = now.getHours();

  const idx = w.hourly.time.findIndex(
    (t: string) => new Date(t).getHours() === nowHour
  );

  if (idx === -1) return [];

  let start = idx - 2;
  let end = idx + 5;

  if (start < 0) {
    end += Math.abs(start);
    start = 0;
  }

  if (end > w.hourly.time.length) {
    start -= end - w.hourly.time.length;
    end = w.hourly.time.length;
    start = Math.max(0, start);
  }

  return w.hourly.temperature_2m.slice(start, end).map((temp: number, i: number) => {
    const actual = start + i;
    // Optional: map hourly weather codes to description
    const weatherCode = w.weathercode; // fallback to current weather
    const description = w.weather_description; // fallback

    return {
      temp,
      time: w.hourly.time[actual],
      precipitation: w.hourly.precipitation[actual],
      isCurrent: actual === idx,
      icon: getIcon(description)
    };
  });
});
</script>

<template>
  <div class="card hourly" v-if="windowData.length">
    <div class="hourly-list">
      <div v-for="(h, i) in windowData" :key="i" :class="['hour-card', { current: h.isCurrent }]">
        <div class="hour-temp">{{ h.temp }}°C</div>
        <div class="hour-icon">{{ h.icon }}</div>
        <div class="hour-time">
          {{ h.time.split("T")[1].slice(0, 2) }}:00
        </div>
        <div class="hour-precip">{{ h.precipitation }} mm</div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.card.hourly {
  width: 38rem;
  overflow-x: auto;
  background: #ffffff;
  border-radius: 1rem;
  padding: 1rem;
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
