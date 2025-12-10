<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, computed } from 'vue';
import axios from 'axios';

interface SpotifyDevice {
    id: string;
    name: string;
    type: string;
}

interface SpotifyTrack {
    name: string;
    artist: string;
    progress_s: number;
    duration_s: number;
    is_playing: boolean;
}

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export default defineComponent({
    name: 'SpotifyView',
    setup() {
        const devices = ref<SpotifyDevice[]>([]);
        const selectedDevice = ref<string | null>(null);
        const currentTrack = ref<SpotifyTrack | null>(null);
        const error = ref<string | null>(null);

        let intervalId: number | null = null;

        const fetchDevices = async () => {
            try {
                const res = await axios.get(`${backendUrl}/spotify/devices`);
                devices.value = res.data;
                if (!selectedDevice.value && devices.value.length > 0 && devices.value[0]) {
                    selectedDevice.value = devices.value[0].id;
                }
            } catch {
                error.value = 'Failed to fetch devices.';
            }
        };

        const fetchCurrentTrack = async () => {
            try {
                const res = await axios.get(`${backendUrl}/spotify/current`);
                currentTrack.value = res.data.error ? null : res.data;
            } catch {
                error.value = 'Failed to fetch current track.';
            }
        };

        const play = async () => {
            if (!selectedDevice.value) return;
            await axios.post(`${backendUrl}/spotify/play`, { device_id: selectedDevice.value });
            fetchCurrentTrack();
        };

        const pause = async () => {
            if (!selectedDevice.value) return;
            await axios.post(`${backendUrl}/spotify/pause`, { device_id: selectedDevice.value });
            fetchCurrentTrack();
        };

        const nextTrack = async () => {
            if (!selectedDevice.value) return;
            await axios.post(`${backendUrl}/spotify/next`, { device_id: selectedDevice.value });
            fetchCurrentTrack();
        };

        const prevTrack = async () => {
            if (!selectedDevice.value) return;
            await axios.post(`${backendUrl}/spotify/previous`, { device_id: selectedDevice.value });
            fetchCurrentTrack();
        };

        const seek = async (position: number) => {
            if (!selectedDevice.value) return;
            await axios.post(`${backendUrl}/spotify/seek`, { device_id: selectedDevice.value, position_s: position });
            fetchCurrentTrack();
        };

        const progressPercent = computed(() => {
            if (!currentTrack.value) return 0;
            return Math.min(100, (currentTrack.value.progress_s / currentTrack.value.duration_s) * 100);
        });

        onMounted(() => {
            fetchDevices();
            fetchCurrentTrack();
            intervalId = window.setInterval(fetchCurrentTrack, 2000);
        });

        onBeforeUnmount(() => {
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = null;
            }
        });

        return {
            devices,
            selectedDevice,
            currentTrack,
            error,
            play,
            pause,
            nextTrack,
            prevTrack,
            seek,
            progressPercent
        };
    }
});
</script>

<template>
    <div class="container">
        <div v-if="error" class="status error">{{ error }}</div>
        <div v-if="!currentTrack && !error" class="status">No track currently playing.</div>

        <div v-if="currentTrack" class="spotify-card">
            <div class="track-art">
                <div class="album-placeholder">🎵</div>
            </div>

            <div class="track-info">
                <div class="track-name">{{ currentTrack.name }}</div>
                <div class="track-artist">{{ currentTrack.artist }}</div>

                <div class="progress-bar">
                    <div class="progress" :style="{ width: progressPercent + '%' }"></div>
                </div>
            </div>

            <div class="controls">
                <button @click="prevTrack" title="Previous Track">⏮️</button>
                <button @click="play" v-if="!currentTrack.is_playing" title="Play">▶️</button>
                <button @click="pause" v-else title="Pause">⏸️</button>
                <button @click="nextTrack" title="Next Track">⏭️</button>
            </div>

            <div class="devices">
                <label for="device-select">Device:</label>
                <select id="device-select" v-model="selectedDevice">
                    <option v-for="device in devices" :key="device.id" :value="device.id">
                        {{ device.name }} ({{ device.type }})
                    </option>
                </select>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 480px;
    margin: 2rem auto;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    padding: 1rem;
}

.status {
    text-align: center;
    font-size: 1rem;
    color: #6b7280;
    margin-bottom: 1rem;
    transition: color 0.3s ease;
}

.status.error {
    color: #ef4444;
}

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
    margin-bottom: 0.5rem;
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
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.track-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
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

.controls {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    font-size: 1.8rem;
}

.controls button {
    background: linear-gradient(145deg, #1f1f1f, #2a2a2a);
    border: none;
    color: #fff;
    padding: 0.6rem 1rem;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.2s ease;
}

.controls button:hover {
    transform: scale(1.2);
    background: linear-gradient(145deg, #3b82f6, #2563eb);
}

.devices {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

.devices label {
    font-size: 0.9rem;
    color: #d1d5db;
}

.devices select {
    background: #374151;
    color: #fff;
    border: none;
    border-radius: 0.5rem;
    padding: 0.3rem 0.5rem;
    font-size: 0.9rem;
}
</style>
