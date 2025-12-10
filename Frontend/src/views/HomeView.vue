<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, computed } from 'vue';
import axios from 'axios';

interface HourlyWeather {
  time: string[];
  temperature_2m: number[];
  humidity: number[];
  precipitation: number[];
}

interface WeatherData {
  temperature: number;
  windspeed: number;
  winddirection: number;
  weather_description: string;
  time: string;
  hourly: HourlyWeather;
}

interface NewsItem {
  title: string;
  description: string;
  link: string;
  image?: string;
}

export default defineComponent({
  name: 'HomeView',
  setup() {
    const weather = ref<WeatherData | null>(null);
    const news = ref<NewsItem[] | null>(null);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const currentNewsIndex = ref(0);
    let newsInterval: number | null = null;
    const isHoveringNews = ref(false);

    const fetchWeather = async () => {
      loading.value = true;
      try {
        const response = await axios.get('http://localhost:5000/weather');
        weather.value = response.data;
      } catch (err: any) {
        error.value = 'Failed to fetch weather.';
      } finally {
        loading.value = false;
      }
    };

    const fetchNews = async () => {
      try {
        const response = await axios.get('http://localhost:5000/nos-news');
        news.value = response.data;
        currentNewsIndex.value = 0;
        stopNewsCarousel();
        startNewsCarousel();
      } catch (err: any) {
        error.value = 'Failed to fetch news.';
      }
    };

    const startNewsCarousel = () => {
      if (news.value && news.value.length > 1 && !newsInterval) {
        newsInterval = window.setInterval(() => {
          if (!isHoveringNews.value) { 
            currentNewsIndex.value = (currentNewsIndex.value + 1) % news.value!.length;
          }
        }, 15000);
      }
    };

    const stopNewsCarousel = () => {
      if (newsInterval) {
        clearInterval(newsInterval);
        newsInterval = null;
      }
    };

    const goToNews = (index: number) => {
      currentNewsIndex.value = index;
      stopNewsCarousel();
      startNewsCarousel();
    };

    onMounted(() => {
      fetchWeather();
      fetchNews();
      setInterval(fetchWeather, 10 * 60 * 1000);
      setInterval(fetchNews, 60 * 60 * 1000);
      startNewsCarousel();
    });

    onUnmounted(() => {
      stopNewsCarousel();
    });

    const getIcon = (desc: string) => {
      if (desc.includes('Clear')) return '☀️';
      if (desc.includes('Cloud')) return '☁️';
      if (desc.includes('Rain') || desc.includes('drizzle')) return '🌧️';
      if (desc.includes('Snow')) return '❄️';
      if (desc.includes('Thunderstorm')) return '⛈️';
      if (desc.includes('Fog')) return '🌫️';
      return '🌡️';
    };

    const currentHourIndex = computed(() => {
      if (!weather.value) return 0;
      const nowHour = new Date(weather.value.time).getHours();
      return weather.value.hourly.time.findIndex(t => new Date(t).getHours() === nowHour);
    });

    const hourlyWindow = computed(() => {
      if (!weather.value) return [];
      const idx = currentHourIndex.value;
      const start = Math.max(0, idx - 6);
      const end = start + 13;
      return weather.value.hourly.temperature_2m.slice(start, end).map((temp, i) => {
        const actualIndex = start + i;
        return {
          temp,
          time: weather.value!.hourly.time[actualIndex],
          precipitation: weather.value!.hourly.precipitation[actualIndex],
          isCurrent: actualIndex === idx
        };
      });
    });

    const currentNewsItem = computed(() => {
      if (!news.value || news.value.length === 0) return null;
      return news.value[currentNewsIndex.value];
    });

    return {
      weather, news, loading, error, getIcon, hourlyWindow, currentNewsItem,
      currentNewsIndex, goToNews, isHoveringNews
    };
  }
});
</script>


<template>
  <div class="container">
    <div v-if="loading" class="status">Loading weather...</div>
    <div v-if="error" class="status error">{{ error }}</div>

    <div v-if="weather" class="grid">
      <!-- Forecast Summary -->
      <div class="card summary">
        <div class="summary-top">
          <div class="temperature">{{ Math.round(weather.temperature) }}°C</div>
          <div class="description">
            <div class="desc-main">
              <span class="icon">{{ getIcon(weather.weather_description) }}</span>
              <span>{{ weather.weather_description }}</span>
            </div>
            <div class="updated">Updated: {{ weather.time.split('T')[1] }}</div>
          </div>
        </div>
        <div class="summary-bottom">
          <div>Humidity: {{ weather.hourly.humidity[0] }}%</div>
          <div>Wind: {{ Math.round(weather.windspeed) }} km/h</div>
          <div>Direction: {{ weather.winddirection }}°</div>
          <div>Precipitation: {{ weather.hourly.precipitation[0] }} mm</div>
        </div>
      </div>

      <!-- Hourly Forecast -->
      <div class="card hourly">
        <div class="hourly-list">
          <div v-for="(hour, idx) in hourlyWindow" :key="idx" :class="['hour-card', { current: hour.isCurrent }]">
            <div class="hour-temp">{{ hour.temp }}°C</div>
            <div class="hour-icon">{{ getIcon(weather.weather_description) }}</div>
            <div class="hour-time">
              {{ hour.time ? (hour.time.split('T')[1]?.slice(0, 2) + ':00') : '' }}
            </div>
            <div class="hour-precip">{{ hour.precipitation ?? 0 }} mm</div>
          </div>
        </div>
      </div>
    </div>

    <!-- News Section -->
    <div v-if="news && news.length" class="news-section">
      <transition name="fade" mode="out-in">
        <div class="news-card" :key="currentNewsIndex" @mouseenter="isHoveringNews = true"
          @mouseleave="isHoveringNews = false"
          :style="currentNewsItem?.image ? { backgroundImage: 'url(' + currentNewsItem.image + ')' } : {}">
          <div class="news-overlay">
            <h3 class="news-title">{{ currentNewsItem?.title }}</h3>
            <p class="news-description">{{ currentNewsItem?.description }}</p>
            <a :href="currentNewsItem?.link" target="_blank" class="news-link">Read more</a>
          </div>
        </div>
      </transition>

      <div class="dots">
        <span v-for="(item, idx) in news" :key="idx" :class="['dot', { active: idx === currentNewsIndex }]"
          @click="goToNews(idx)"></span>
      </div>
    </div>
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

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media(min-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    /* Force single column so hourly forecast stays below summary */
  }
}

.card {
  background: #ffffff;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);

  width: 300px;
  height: 200px;
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

.hourly {
  width: 100%;
  /* Make it full width */
  overflow-x: auto;
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

.news-section {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.news-card {
  width: 100%;
  max-width: 500px;
  height: 280px;
  border-radius: 1rem;
  overflow: hidden;
  position: relative;
  background-color: #111;
  background-size: cover;
  background-position: center;
  color: white;
  display: flex;
  align-items: flex-end;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.4);
}

.news-overlay {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.news-title {
  font-size: 1.4rem;
  font-weight: bold;
  line-height: 1.2;
}

.news-description {
  font-size: 0.9rem;
  color: #e0e0e0;
  flex-grow: 1;
}

.news-link {
  font-size: 0.9rem;
  color: #3b82f6;
  font-weight: 500;
  text-decoration: none;
  align-self: flex-start;
}

.news-link:hover {
  text-decoration: underline;
}


.dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #d1d5db;
  transition: background-color 0.3s;
}

.dot.active {
  background-color: #3b82f6;
}

/* Smooth fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
