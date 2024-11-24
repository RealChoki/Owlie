<template>
  <div class="chat-bubble-container my-4 pb-5">
    <div v-for="(message, index) in messages" :key="message.id">
      <div
        v-if="message.role === 'user'"
        class="chat-bubble user-msg my-3"
      >
        {{ message.content }}
      </div>
      <div
        v-else-if="message.role === 'assistant'"
        class="assistant-msg text-white  p-2 my-2"
      > 
        <img src="./icons/OwlLogo.png" alt="assistant" class="assistant-pfp p-1 pt-0" >
        {{ message.content }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { getMessages } from '../services/chatService';

const messages = computed(() => getMessages());
</script>

<style scoped>
.chat-bubble-container {
    padding: 10px;
    height: 100%;
    overflow-y: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.chat-bubble-container::-webkit-scrollbar {
    display: none;
}

.chat-bubble {
  background-color: #1a1a1b;
  color: white;
  padding: 12px 20px;
  border-radius: 20px;
  max-width: 85%;
  display: inline-block;
  word-wrap: break-word;
  box-shadow: 0 0px 10px #5b5b5b;
}

.assistant-pfp {
  width: 30px;
  height: 30px;
  object-fit: cover;
}
</style>