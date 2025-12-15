<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

// Create an axios instance using the backend URL from .env.local
const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL
});

const register = async () => {
    error.value = "";
    loading.value = true;

    try {
        const response = await api.post("/auth/register", {
            username: username.value,
            password: password.value,
        });

        router.push("/login");
    } catch (err: any) {
        error.value = err.response?.data?.message || "Registration failed";
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <h1 class="title">Create account</h1>
            <p class="subtitle">Join Citadel</p>

            <form @submit.prevent="register">
                <div class="form-group">
                    <label>Username</label>
                    <input v-model="username" type="text" />
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input v-model="password" type="password" />
                </div>

                <p v-if="error" class="error">{{ error }}</p>

                <button type="submit" :disabled="loading">
                    {{ loading ? "Creating..." : "Register" }}
                </button>
            </form>

            <p class="switch">
                Already have an account?
                <router-link to="/login">Login</router-link>
            </p>
        </div>
    </div>
</template>


<style scoped>
.auth-container {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.auth-card {
    width: 360px;
    padding: 2rem;
    border-radius: 16px;
    background: #ffffff;
    box-shadow:
        0 10px 25px rgba(15, 23, 42, 0.08),
        0 4px 10px rgba(15, 23, 42, 0.05);
}

.title {
    font-size: 1.75rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.25rem;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 1.5rem;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    font-size: 0.85rem;
    color: #374151;
    margin-bottom: 0.35rem;
}

input {
    width: 100%;
    padding: 0.65rem 0.75rem;
    border-radius: 8px;
    border: 1px solid #d1d5db;
    font-size: 0.9rem;
}

input:focus {
    outline: none;
    border-color: #6366f1;
}

button {
    width: 100%;
    margin-top: 0.5rem;
    padding: 0.7rem;
    border: none;
    border-radius: 8px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: 600;
    cursor: pointer;
}

button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.error {
    color: #dc2626;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
    text-align: center;
}

.switch {
    margin-top: 1rem;
    text-align: center;
    font-size: 0.85rem;
}

.switch a {
    color: #6366f1;
    font-weight: 600;
    text-decoration: none;
}
</style>
