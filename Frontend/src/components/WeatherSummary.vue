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



<template>
  <div class="card summary" v-if="weather">
    <div class="summary-header">
      <div class="temp-block">
        <div class="temperature">{{ Math.round(weather.temperature) }}°</div>
        <div class="feels">Celsius</div>
      </div>

      <div class="condition">
        <div class="condition-main">
          <span class="icon">{{ icon }}</span>
          <span class="text">{{ weather.weather_description }}</span>
        </div>
        <div class="updated">
          Updated {{ weather.time.split("T")[1].slice(0, 5) }}
        </div>
      </div>
    </div>

    <div class="divider" />

    <div class="summary-stats">
      <div class="stat">
        <span>💧</span>
        <span>{{ weather.hourly.humidity[0] }}%</span>
        <small>Humidity</small>
      </div>

      <div class="stat">
        <span>🌬️</span>
        <span>{{ Math.round(weather.windspeed) }} km/h</span>
        <small>Wind</small>
      </div>

      <div class="stat">
        <span>🧭</span>
        <span>{{ weather.winddirection }}°</span>
        <small>Direction</small>
      </div>

      <div class="stat">
        <span>🌧️</span>
        <span>{{ weather.hourly.precipitation[0] }} mm</span>
        <small>Rain</small>
      </div>
    </div>
  </div>
</template>



<style scoped>
.card.summary {
  background: linear-gradient(180deg, #ffffff, #f9fafb);
  border-radius: 1.25rem;
  padding: 1.25rem;
  width: 320px;
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.08);
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.temp-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.temperature {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1;
}

.feels {
  font-size: 0.75rem;
  color: #6b7280;
}

.condition {
  text-align: right;
}

.condition-main {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 500;
}

.icon {
  font-size: 2rem;
}

.updated {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 1rem 0;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.stat {
  background: #ffffff;
  border-radius: 0.75rem;
  padding: 0.5rem;
  text-align: center;
  box-shadow: inset 0 0 0 1px #f1f5f9;
}

.stat span {
  display: block;
  font-size: 1rem;
  font-weight: 600;
}

.stat small {
  font-size: 0.7rem;
  color: #6b7280;
}
</style>
