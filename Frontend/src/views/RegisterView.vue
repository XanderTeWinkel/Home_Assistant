<template>
    <div class="register">
        <h2>Register</h2>
        <form @submit.prevent="register">
            <input type="text" v-model="username" placeholder="Username" required />
            <input type="password" v-model="password" placeholder="Password" required />
            <button type="submit">Register</button>
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
        async register() {
            try {
                await axios.post("http://localhost:1024/auth/register", {
                    username: this.username,
                    password: this.password,
                });
                this.$router.push("/login"); // redirect to login after registration
            } catch (err) {
                this.error = err.response.data.message || "Registration failed";
            }
        },
    },
};
</script>
