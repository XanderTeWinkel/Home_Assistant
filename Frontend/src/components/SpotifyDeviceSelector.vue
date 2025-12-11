<!-- SpotifyDeviceSelector.vue -->
<script lang="ts">
import { defineComponent } from 'vue';
import type { PropType } from 'vue';

interface SpotifyDevice {
    id: string;
    name: string;
    type: string;
}

export default defineComponent({
    name: 'SpotifyDeviceSelector',
    props: {
        devices: { type: Array as PropType<SpotifyDevice[]>, required: true },
        modelValue: { type: String, required: false }
    },
    emits: ['update:modelValue'],
    methods: {
        handleChange(event: Event) {
            const target = event.target as HTMLSelectElement | null;
            const value = target?.value ?? undefined;
            this.$emit('update:modelValue', value);
        }
    }
});
</script>

<template>
    <div class="devices">
        <label for="device-select">Device:</label>
        <select
            id="device-select"
            :value="modelValue"
            @change="handleChange"
        >
            <option
                v-for="d in devices"
                :key="d.id"
                :value="d.id"
            >
                {{ d.name }} ({{ d.type }})
            </option>
        </select>
    </div>
</template>

<style scoped>
.devices {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

label {
    font-size: 0.9rem;
    color: #d1d5db;
}

select {
    background: #374151;
    color: #fff;
    border: none;
    border-radius: 0.5rem;
    padding: 0.3rem 0.5rem;
    font-size: 0.9rem;
}
</style>
