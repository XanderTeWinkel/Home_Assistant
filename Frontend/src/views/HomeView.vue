<script setup lang="ts">
/* Composables */
import { useWeather } from "@/composables/weather";
import { useNews } from "@/composables/news";

/* Components */
import WeatherSummary from "@/components/WeatherSummary.vue";
import HourlyForecast from "@/components/HourlyForecast.vue";
import NewsCarousel from "@/components/NewsCarousel.vue";

// Views
import SpotifyView from "@/views/SpotifyView.vue";

/* Data */
const { weather, loading, error } = useWeather();
const { news, currentIndex, goTo, isHovering } = useNews();
</script>

<template>
  <div class="home">
    <!-- Loading/Error States -->
    <div v-if="loading" class="status">Loading home page...</div>
    <div v-else-if="error" class="status error">{{ error }}</div>

    <div v-else-if="weather" class="grid">
      <!-- Row 1: Current Weather -->
      <section class="card card-hero">
        <WeatherSummary :weather="weather" />
      </section>

      <!-- Spotify (spans top 2 rows) -->
      <section class="card card-spotify">
        <SpotifyView />
      </section>

      <!-- Row 2: Hourly Forecast -->
      <section class="card card-hourly">
        <HourlyForecast :weather="weather" />
      </section>

      <!-- Row 3: News -->
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
  grid-template-columns: 1fr 1fr;
  /* 2 columns */
  grid-template-rows: auto auto auto;
  /* 3 rows */
  gap: 1.5rem;
  justify-items: center;
  align-items: start;
}

/* Cards */
.card {
  width: 100%;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem;

  /* Flexbox for centering */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* Specific Positions */
.card-hero {
  grid-column: 1;
  /* left column */
  grid-row: 1;
}

.card-spotify {
  grid-column: 2;
  /* right column */
  grid-row: 1 / span 2;
  /* spans top 2 rows */
  padding: 1rem;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.card-hourly {
  grid-column: 1;
  /* left column */
  grid-row: 2;
}

.card-wide {
  grid-column: 1 / span 2;
  /* spans both columns */
  grid-row: 3;
}
</style>
