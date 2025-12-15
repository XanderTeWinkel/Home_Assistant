<template>
    <div class="login">
        <h2>Login</h2>
        <form @submit.prevent="login">
            <input type="text" v-model="username" placeholder="Username" required />
            <input type="password" v-model="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        <p v-if="error">{{ error }}</p>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            username: "",
            password: "",
            error: null,
        };
    },
    methods: {
        async login() {
            try {
                const res = await axios.post("http://localhost:1024/auth/login", {
                    username: this.username,
                    password: this.password,
                });
                // Save JWT in localStorage
                localStorage.setItem("token", res.data.access_token);
                this.$router.push("/"); // redirect after login
            } catch (err) {
                this.error = err.response.data.message || "Login failed";
            }
        },
    },
};
</script>
