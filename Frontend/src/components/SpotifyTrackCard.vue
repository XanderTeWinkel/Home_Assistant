<!-- SpotifyTrackCard.vue -->
<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

type SpotifyTrack = {
    name: string;
    artist: string;
    album?: string;
    durationMs?: number;
    artworkUrl?: string;
};

export default defineComponent({
    name: 'SpotifyTrackCard',
    props: {
        track: { type: Object as PropType<SpotifyTrack>, required: true },
        progressPercent: { type: Number, required: true }
    }
});
</script>

<template>
    <div class="spotify-card">
        <div class="track-art">
            <div class="album-placeholder">🎵</div>
        </div>

        <div class="track-info">
            <div class="track-name">{{ track.name }}</div>
            <div class="track-artist">{{ track.artist }}</div>

            <div class="progress-bar">
                <div class="progress" :style="{ width: progressPercent + '%' }"></div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.spotify-card {
    background: linear-gradient(145deg, #222, #2c2c2c);
    color: #fff;
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.track-art {
    display: flex;
    justify-content: center;
}

.album-placeholder {
    font-size: 4rem;
    width: 100px;
    height: 100px;
    background: #374151;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 1rem;
}

.track-info {
    text-align: center;
}

.track-name {
    font-size: 1.5rem;
    font-weight: 600;
}

.track-artist {
    font-size: 1rem;
    color: #9ca3af;
}

.progress-bar {
    height: 8px;
    background: #374151;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 0.5rem;
}

.progress {
    height: 100%;
    background: #3b82f6;
    transition: width 0.2s ease;
}
</style>
