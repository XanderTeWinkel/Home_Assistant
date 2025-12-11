<!-- SpotifyControls.vue -->
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'SpotifyControls',
    emits: ['play', 'pause', 'next', 'prev'],
    props: {
        isPlaying: { type: Boolean, required: true }
    }
});
</script>

<template>
    <div class="controls">
        <button @click="$emit('prev')" title="Previous Track">⏮️</button>

        <button v-if="!isPlaying" @click="$emit('play')" title="Play">▶️</button>
        <button v-else @click="$emit('pause')" title="Pause">⏸️</button>

        <button @click="$emit('next')" title="Next Track">⏭️</button>
    </div>
</template>

<style scoped>
.controls {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    font-size: 1.8rem;
    margin-top: 1rem;
}

button {
    background: linear-gradient(145deg, #1f1f1f, #2a2a2a);
    border: none;
    color: white;
    padding: 0.6rem 1rem;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.2s ease;
}

button:hover {
    transform: scale(1.2);
    background: linear-gradient(145deg, #3b82f6, #2563eb);
}
</style>
