<template>
  <div class="news-section" v-if="news.length">
    <transition name="fade" mode="out-in">
      <div
        class="news-card"
        :key="index"
        @mouseenter="$emit('update:isHovering', true)"
        @mouseleave="$emit('update:isHovering', false)"
        :style="current.image ? { backgroundImage: `url(${current.image})` } : {}"
      >
        <div class="news-overlay">
          <h3 class="news-title">{{ current.title }}</h3>
          <p class="news-description">{{ current.description }}</p>
          <a :href="current.link" target="_blank" class="news-link">Read more</a>
        </div>
      </div>
    </transition>

    <div class="dots">
      <span
        v-for="(n, i) in news"
        :key="i"
        :class="['dot', { active: i === index }]"
        @click="$emit('goTo', i)"
      ></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType } from "vue";

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
</script>

<style scoped>
.news-section {
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
