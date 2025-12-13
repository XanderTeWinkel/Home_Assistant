<script setup lang="ts">
/* Composables */
import { useWeather } from "@/composables/weather";
import { useNews } from "@/composables/news";

/* Components */
import WeatherSummary from "@/components/WeatherSummary.vue";
import HourlyForecast from "@/components/HourlyForecast.vue";
import NewsCarousel from "@/components/NewsCarousel.vue";

/* Data */
const { weather, loading, error } = useWeather();
const { news, currentIndex, goTo, isHovering } = useNews();
</script>

<template>
  <div class="home">
    <!-- Loading/Error States -->
    <div v-if="loading" class="status">Loading home page...</div>
    <div v-else-if="error" class="status error">{{ error }}</div>

    <!-- Main Grid -->
    <div v-else-if="weather" class="grid">
      <!-- Weather Hero -->
      <section class="card card-hero">
        <WeatherSummary :weather="weather" />
      </section>

      <!-- Hourly Forecast -->
      <section class="card card-hourly">
        <HourlyForecast :weather="weather" />
      </section>

      <!-- News Carousel -->
      <section class="card card-wide" v-if="news.length">
        <NewsCarousel :news="news" :index="currentIndex" :isHovering="isHovering" @goTo="goTo" />
      </section>
    </div>
  </div>
</template>

<style scoped>
/* Status Messages */
.status {
  text-align: center;
  font-size: 1rem;
  color: #4b5563;
  margin: 1rem 0;
}

.status.error {
  color: #ef4444;
}

/* Grid Layout */
.grid {
  display: grid;
  grid-template-columns: 1fr minmax(300px, 800px) 1fr;
  grid-template-rows: auto;
  gap: 1.5rem;
  justify-items: center;
}

/* Cards */
.card {
  width: 100%;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

/* Specific Positions */
.card-hero {
  grid-column: 2;
}

.card-hourly {
  grid-column: 2;
}

.card-wide {
  grid-column: 2;
}
</style>
