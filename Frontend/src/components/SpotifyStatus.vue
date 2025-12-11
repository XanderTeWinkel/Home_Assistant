<!-- SpotifyStatus.vue -->
<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

interface SpotifyTrack {
    name: string;
    artists: string[];
    album?: {
        name?: string;
        images?: { url: string }[];
    } | null;
    duration_ms?: number;
    is_playing?: boolean;
}

export default defineComponent({
    name: 'SpotifyStatus',
    props: {
        error: String,
        currentTrack: Object as PropType<SpotifyTrack | null>
    }
});
</script>

<template>
    <div>
        <div v-if="error" class="status error">{{ error }}</div>
        <div v-else-if="!currentTrack" class="status">No track currently playing.</div>
    </div>
</template>

<style scoped>
.status {
    text-align: center;
    font-size: 1rem;
    color: #6b7280;
    margin-bottom: 1rem;
}

.error {
    color: #ef4444;
}
</style>
