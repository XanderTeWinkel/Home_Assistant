<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

interface User {
    id: string;
    username: string;
    created_at: string;
}

const users = ref<User[]>([]);

const backendUrl = import.meta.env.VITE_BACKEND_URL;

const fetchUsers = async () => {
    try {
        const response = await axios.get<User[]>(`${backendUrl}/users`);
        users.value = response.data;
    } catch (error) {
        console.error("Failed to fetch users:", error);
        users.value = [];
    }
};

onMounted(fetchUsers);
</script>

<template>
    <div class="people-dashboard">
        <h2>People</h2>

        <div class="cards-row">
            <div v-for="user in users" :key="user.id" class="user-card">
                <h3>{{ user.username }}</h3>
                <p>Joined: {{ new Date(user.created_at).toLocaleDateString() }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.people-dashboard {
    font-family: sans-serif;
    padding: 1rem;
}

h2 {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    text-align: center;
}

.cards-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
}

.user-card {
    background-color: #f5f5f5;
    border-radius: 1rem;
    padding: 1.2rem;
    width: 180px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.user-card h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
}

.user-card p {
    margin: 0;
    font-size: 0.9rem;
    color: #555;
}
</style>
