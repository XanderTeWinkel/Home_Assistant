<script setup lang="ts">
import { computed, type PropType, ref, onMounted, onUnmounted } from "vue";

interface NewsItem {
  title?: string;
  description?: string;
  link?: string;
  image?: string;
}

const props = defineProps({
  news: { type: Array as PropType<NewsItem[]>, required: true },
  index: { type: Number, required: true },
  isHovering: { type: Boolean, required: true }
});

const emit = defineEmits<{
  (e: "goTo", index: number): void;
  (e: "update:isHovering", value: boolean): void;
}>();

const current = computed<NewsItem>(() => props.news?.[props.index] ?? ({} as NewsItem));

// Reactive window width to detect screen size
const windowWidth = ref(window.innerWidth);

const updateWidth = () => {
  windowWidth.value = window.innerWidth;
};

onMounted(() => {
  window.addEventListener('resize', updateWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
});

const visibleNews = computed(() => {
  // Show 1 item on screens below 1170px, otherwise 3
  const num = windowWidth.value < 1170 ? 1 : 3;
  return props.news.slice(props.index, props.index + num);
});
</script>

<template>
  <div class="news-section" v-if="news.length">
    <div class="news-carousel">
      <transition-group name="fade" tag="div" class="news-cards-wrapper">
        <div class="news-card" v-for="(item, i) in visibleNews" :key="i" @mouseenter="$emit('update:isHovering', true)"
          @mouseleave="$emit('update:isHovering', false)"
          :style="item.image ? { backgroundImage: `url(${item.image})` } : {}">
          <div class="news-overlay">
            <h3 class="news-title">{{ item.title }}</h3>
            <p class="news-description">{{ item.description }}</p>
            <a :href="item.link" target="_blank" class="news-link">Read more</a>
          </div>
        </div>
      </transition-group>
    </div>

    <div class="dots">
      <span v-for="(n, i) in news" :key="i" :class="['dot', { active: i === index }]" @click="$emit('goTo', i)"></span>
    </div>
  </div>
</template>

<style scoped>
.news-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.news-cards-wrapper {
  display: flex;
  gap: 1rem;
  justify-content: center;
  width: 100%;
  flex-wrap: wrap;
}

/* Each news card */
.news-card {
  flex: 1 1 calc(33% - 1rem);
  /* 3 cards per row with gap */
  max-width: 350px;
  /* optional, adjusts card size */
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

/* Overlay inside each card */
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

/* Dots navigation */
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

/* Fade transition for carousel */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive: fallback for smaller screens */
@media (max-width: 1170px) {
  .news-cards-wrapper {
    flex-wrap: nowrap;
    /* optional: keep cards from wrapping */
    justify-content: center;
  }

  .news-card {
    flex: 1 1 100%;
    /* each card takes full width */
    /* max-width: 100%; */
  }
}
</style>