<template>
  <div class="card summary" v-if="weather">
    <div class="summary-top">
      <div class="temperature">{{ Math.round(weather.temperature) }}°C</div>
      <div class="description">
        <div class="desc-main">
          <span class="icon">{{ icon }}</span>
          <span>{{ weather.weather_description }}</span>
        </div>
        <div class="updated">Updated: {{ weather.time.split("T")[1] }}</div>
      </div>
    </div>

    <div class="summary-bottom">
      <div>Humidity: {{ weather.hourly.humidity[0] }}%</div>
      <div>Wind: {{ Math.round(weather.windspeed) }} km/h</div>
      <div>Direction: {{ weather.winddirection }}°</div>
      <div>Precipitation: {{ weather.hourly.precipitation[0] }} mm</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
  weather: { type: Object, required: true }
});

const icon = computed(() => {
  const desc = props.weather.weather_description ?? "";
  if (desc.includes("Clear")) return "☀️";
  if (desc.includes("Cloud")) return "☁️";
  if (desc.includes("Rain") || desc.includes("drizzle")) return "🌧️";
  if (desc.includes("Snow")) return "❄️";
  if (desc.includes("Thunderstorm")) return "⛈️";
  if (desc.includes("Fog")) return "🌫️";
  return "🌡️";
});
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 1rem;
  padding: 1rem;
  margin: 1rem;
  width: 300px;
  height: 200px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
}

.summary-top {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.temperature {
  font-size: 3rem;
  font-weight: bold;
}

.description {
  display: flex;
  flex-direction: column;
}

.desc-main {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
}

.icon {
  font-size: 2rem;
}

.updated {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.summary-bottom {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #4b5563;
}
</style>
