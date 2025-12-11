<script setup lang="ts">
import { useWeather } from "../composables/weather";
import { useNews } from "../composables/news";

import WeatherSummary from "@/components/WeatherSummary.vue";
import HourlyForecast from "@/components/HourlyForecast.vue";
import NewsCarousel from "@/components/NewsCarousel.vue";

const { weather, loading, error } = useWeather();
const { news, currentIndex, goTo, isHovering } = useNews();
</script>

<template>
  <div class="container">
    <div v-if="loading" class="status">Loading weather...</div>
    <div v-if="error" class="status error">{{ error }}</div>

    <WeatherSummary v-if="weather" :weather="weather" />

    <HourlyForecast v-if="weather" :weather="weather" />

    <NewsCarousel
      v-if="news.length"
      :news="news"
      :index="currentIndex"
      :isHovering="isHovering"
      @goTo="goTo"
    />
  </div>
</template>

<style scoped>
.container {
  margin: 2rem auto;
  font-family: 'Arial', sans-serif;
  padding: 1rem;
}

.status {
  text-align: center;
  font-size: 1rem;
  color: #4b5563;
  margin-bottom: 1rem;
}

.status.error {
  color: #ef4444;
}
</style>
