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
    <!-- Loading / Error States -->
    <div v-if="loading" class="status">Loading home page...</div>
    <div v-else-if="error" class="status error">{{ error }}</div>

    <!-- Main Grid -->
    <div v-else-if="weather" class="grid">
      <!-- Weather Summary -->
      <section class="card card-hero">
        <WeatherSummary :weather="weather" />
      </section>

      <!-- Spotify -->
      <section class="card card-spotify">
        <SpotifyView />
      </section>

      <!-- Hourly Forecast (desktop only) -->
      <section class="card card-hourly">
        <HourlyForecast :weather="weather" />
      </section>

      <!-- News -->
      <section class="card card-wide" v-if="news.length">
        <NewsCarousel :news="news" :index="currentIndex" :isHovering="isHovering" @goTo="goTo" />
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ============================= */
/* Status Messages               */
/* ============================= */
.status {
  text-align: center;
  font-size: 1rem;
  color: #4b5563;
  margin: 1rem 0;
}

.status.error {
  color: #ef4444;
}

/* ============================= */
/* Grid Layout (Desktop)         */
/* ============================= */
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-areas:
    "hero spotify"
    "hourly spotify"
    "news news";
  gap: 1.5rem;
  align-items: stretch;
}

/* ============================= */
/* Cards                         */
/* ============================= */
.card {
  width: 100%;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
  padding: 1.25rem;

  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* ============================= */
/* Grid Areas                    */
/* ============================= */
.card-hero {
  grid-area: hero;
}

.card-spotify {
  grid-area: spotify;
}

.card-hourly {
  grid-area: hourly;
}

.card-wide {
  grid-area: news;
}

/* ============================= */
/* Hide Hourly on Tablets/Mobile */
/* ============================= */
@media (max-width: 1024px) {
  .card-hourly {
    display: none;
  }

  .grid {
    grid-template-columns: 1fr;
    grid-template-areas:
      "hero"
      "spotify"
      "news";
  }

  .card {
    padding: 1.1rem;
  }
}

/* ============================= */
/* Mobile                        */
/* ============================= */
@media (max-width: 768px) {
  .grid {
    gap: 1rem;
  }

  .card {
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.08);
  }
}

/* ============================= */
/* Small Phones                  */
/* ============================= */
@media (max-width: 480px) {
  .card {
    padding: 0.85rem;
  }

  .status {
    font-size: 0.9rem;
  }
}
</style>
