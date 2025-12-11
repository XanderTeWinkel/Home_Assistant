<script setup lang="ts">
defineProps<{
  label: string;
  value?: number | string;
}>();
</script>

<template>
  <div class="card small">
    <div class="stat">
      <slot>{{ value }}</slot>
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

.card.small {
  width: 140px;
  height: 140px;
}

.card:hover {
  transform: translateY(-5px);
}

.card-title {
  margin-top: 0.5rem;
  font-weight: 600;
  text-align: center;
}

.stat {
  font-size: 1.4rem;
  font-weight: bold;
  text-align: center;
}
</style>
