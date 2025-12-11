<template>
    <div class="chat-container">
        <h2>AI Chat</h2>

        <div class="messages">
            <div
                v-for="(msg, index) in messages"
                :key="index"
                :class="['message', msg.role]"
            >
                <div class="bubble">
                    <span>{{ msg.content }}</span>
                </div>
            </div>
        </div>

        <div class="input-area">
            <input
                v-model="userInput"
                @keyup.enter="sendMessage"
                placeholder="Type your message..."
            />
            <button @click="sendMessage">Send</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import axios from 'axios'

// Backend URL
const backendUrl = import.meta.env.VITE_BACKEND_URL

// Chat state
interface ChatMessage {
    role: 'user' | 'ai'
    content: string
}

const messages = ref<ChatMessage[]>([])
const userInput = ref('')

async function sendMessage() {
    if (!userInput.value.trim()) return

    // Add user message
    messages.value.push({ role: 'user', content: userInput.value })
    const tempInput = userInput.value
    userInput.value = ''

    try {
        const response = await axios.get(`${backendUrl}/chat`, {
            params: { prompt: tempInput }
        })

        messages.value.push({
            role: 'ai',
            content: response.data.response
        })
    } catch (error) {
        messages.value.push({
            role: 'ai',
            content: 'Error: Could not reach the server.'
        })
        console.error(error)
    }

    await nextTick()
    scrollToBottom()
}

function scrollToBottom() {
    const container = document.querySelector('.messages')
    if (container) container.scrollTop = container.scrollHeight
}
</script>

<style scoped>
.chat-container {
    height: 90%;
    width: 600px;
    max-width: 90%;
    margin: 2rem auto;
    border-radius: 10px;
    background: #f4f7fb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    padding: 1rem;
    font-family: 'Segoe UI', sans-serif;
}

h2 {
    text-align: center;
    margin-bottom: 1rem;
    color: #333;
}

/* Messages list */
.messages {
    flex: 1;
    height: 400px;
    overflow-y: auto;
    padding: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;
    background: #e9eef5;
    border-radius: 8px;
    scrollbar-width: thin;
}

.messages::-webkit-scrollbar {
    width: 6px;
}

.messages::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
}

.message {
    display: flex;
}

.message.user {
    justify-content: flex-end;
}

.message.ai {
    justify-content: flex-start;
}

/* Chat bubble */
.bubble {
    max-width: 70%;
    padding: 0.6rem 1rem;
    border-radius: 15px;
    line-height: 1.4;
    word-wrap: break-word;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.message.user .bubble {
    background-color: #0077cc;
    color: white;
    border-bottom-right-radius: 2px;
}

.message.ai .bubble {
    background-color: #ffffff;
    color: #333;
    border-bottom-left-radius: 2px;
}

/* Input */
.input-area {
    display: flex;
    gap: 0.5rem;
}

input {
    flex: 1;
    padding: 0.6rem;
    border-radius: 10px;
    border: 1px solid #ccc;
    outline: none;
}

input:focus {
    border-color: #0077cc;
    box-shadow: 0 0 5px rgba(0, 119, 204, 0.3);
}

button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 10px;
    background-color: #0077cc;
    color: white;
    cursor: pointer;
    transition: background 0.2s;
}

button:hover {
    background-color: #005fa3;
}
</style>
