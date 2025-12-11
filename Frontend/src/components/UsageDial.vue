<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  value: number;
  label: string;
}>();

const color = computed(() => {
  const v = props.value;
  if (v < 50) return "#10b981";
  if (v < 75) return "#f59e0b";
  return "#ef4444";
});
</script>

<template>
  <div class="card">
    <div class="dial">
      <svg viewBox="0 0 36 36">
        <path
          class="bg"
          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <path
          class="progress"
          :stroke="color"
          :stroke-dasharray="value + ', 100'"
          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <text x="18" y="20.35" class="dial-text" transform="rotate(90,18,18)">
          {{ value }}%
        </text>
      </svg>
    </div>
    <div class="card-title">{{ label }}</div>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border-radius: 12px;
  padding: 1rem;
  width: 160px;
  height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}

.card-title {
  margin-top: 0.5rem;
  font-weight: 600;
  text-align: center;
}

.dial {
  width: 80px;
  height: 80px;
}

svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

path.bg {
  fill: none;
  stroke: #eee;
  stroke-width: 4;
}

path.progress {
  fill: none;
  stroke-width: 4;
  stroke-linecap: round;
  transition: stroke-dasharray 1s ease, stroke 0.3s ease;
}

.dial-text {
  fill: #111;
  font-size: 0.6rem;
  text-anchor: middle;
  dominant-baseline: middle;
}
</style>
