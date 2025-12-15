<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const username = ref("");
const createdAt = ref("");
const oldPassword = ref("");
const newPassword = ref("");
const message = ref("");
const error = ref("");

const token = localStorage.getItem("access_token");

const api = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL, // <-- use the env variable
    headers: {
        Authorization: `Bearer ${token}`,
    },
});

// Fetch profile info
onMounted(async () => {
    try {
        const res = await api.get("/auth/me");
        username.value = res.data.username;
        createdAt.value = new Date(res.data.created_at).toLocaleDateString();
    } catch {
        error.value = "Failed to load profile";
    }
});

// Change password
const changePassword = async () => {
    message.value = "";
    error.value = "";

    try {
        await api.post("/auth/change-password", {
            old_password: oldPassword.value,
            new_password: newPassword.value,
        });

        message.value = "Password updated successfully";
        oldPassword.value = "";
        newPassword.value = "";
    } catch (err: any) {
        error.value = err.response?.data?.message || "Password update failed";
    }
};

// Logout
const logout = () => {
    localStorage.removeItem("access_token");
    router.push("/login");
};
</script>

<template>
    <div class="profile-container">
        <div class="profile-card">
            <div class="avatar"> 
                {{ username.charAt(0).toUpperCase() }}
            </div>

            <h1 class="username">{{ username }}</h1>
            <p class="subtitle">Member since {{ createdAt }}</p>

            <!-- Change Password -->
            <div class="section">
                <h3>Change Password</h3>
                <input type="password" placeholder="Current password" v-model="oldPassword" />
                <input type="password" placeholder="New password" v-model="newPassword" />
                <button @click="changePassword">Update Password</button>
                <p class="success" v-if="message">{{ message }}</p>
                <p class="error" v-if="error">{{ error }}</p>
            </div>

            <!-- Logout -->
            <div class="section logout-section">
                <button class="logout-button" @click="logout">Logout</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.profile-container {
    display: flex;
    justify-content: center;
    padding-top: 3rem;
}

.profile-card {
    width: 420px;
    padding: 2.5rem;
    border-radius: 20px;
    background: #fff;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
    text-align: center;
}

.avatar {
    width: 80px;
    height: 80px;
    margin: 0 auto;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 2rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.username {
    margin-top: 1rem;
    font-size: 1.6rem;
    font-weight: 700;
}

.subtitle {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 2rem;
}

.section {
    text-align: left;
    margin-top: 1.5rem;
}

.section h3 {
    margin-bottom: 1rem;
}

input {
    width: 100%;
    padding: 0.7rem;
    margin-bottom: 0.75rem;
    border-radius: 8px;
    border: 1px solid #d1d5db;
}

button {
    width: 100%;
    padding: 0.7rem;
    border-radius: 8px;
    border: none;
    background: #4f46e5;
    color: white;
    font-weight: 600;
    cursor: pointer;
}

button:hover {
    background: #4338ca;
}

.success {
    margin-top: 0.75rem;
    color: #16a34a;
}

.error {
    margin-top: 0.75rem;
    color: #dc2626;
}

/* Logout button styling */
.logout-section {
    margin-top: 2rem;
}

.logout-button {
    background: #ef4444;
    /* red */
    color: white;
    font-weight: 600;
    padding: 0.7rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}

.logout-button:hover {
    background: #b91c1c;
}
</style>
