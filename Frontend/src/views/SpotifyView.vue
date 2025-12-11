<!-- SpotifyView.vue -->
<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount, computed } from 'vue';
import axios from 'axios';

import SpotifyStatus from '../components/SpotifyStatus.vue';
import SpotifyTrackCard from '../components/SpotifyTrackCard.vue';
import SpotifyControls from '../components/SpotifyControls.vue';
import SpotifyDeviceSelector from '../components/SpotifyDeviceSelector.vue';

interface SpotifyDevice {
    id: string;
    name: string;
    type: string;
}

interface SpotifyTrack {
    name: string;
    artist: string;
    artists: string[];
    progress_s: number;
    duration_s: number;
    is_playing: boolean;
}

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export default defineComponent({
    name: 'SpotifyView',
    components: {
        SpotifyStatus,
        SpotifyTrackCard,
        SpotifyControls,
        SpotifyDeviceSelector
    },
    setup() {
        const devices = ref<SpotifyDevice[]>([]);
        const selectedDevice = ref<string | undefined>(undefined);
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
                if (res.data && !res.data.error) {
                    const data = res.data;
                    const artist = data.artist ?? (Array.isArray(data.artists) && data.artists.length > 0 ? data.artists[0] : '');
                    currentTrack.value = {
                        name: data.name,
                        artist,
                        artists: data.artists || [],
                        progress_s: data.progress_s ?? 0,
                        duration_s: data.duration_s ?? 1,
                        is_playing: Boolean(data.is_playing)
                    };
                } else {
                    currentTrack.value = null;
                }
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

        const seek = async (pos: number) => {
            if (!selectedDevice.value) return;
            await axios.post(`${backendUrl}/spotify/seek`, { device_id: selectedDevice.value, position_s: pos });
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
        <SpotifyStatus :error="error ?? undefined" :currentTrack="currentTrack" />

        <SpotifyTrackCard
            v-if="currentTrack"
            :track="currentTrack"
            :progressPercent="progressPercent"
        />

        <SpotifyControls
            v-if="currentTrack"
            :isPlaying="currentTrack.is_playing"
            @play="play"
            @pause="pause"
            @next="nextTrack"
            @prev="prevTrack"
        />

        <SpotifyDeviceSelector
            v-if="devices.length > 0"
            :devices="devices"
            v-model="selectedDevice"
        />
    </div>
</template>

<style scoped>
.container {
    max-width: 500px;
    margin: 3.5rem auto;
    padding: 2.5rem;

    background: #1e1e1e;
    border-radius: 2rem;

    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.5),
        0 0 10px rgba(255, 255, 255, 0.05);

    transition: transform 0.25s ease;
}

.container:hover {
    transform: translateY(-4px);
}
</style>
