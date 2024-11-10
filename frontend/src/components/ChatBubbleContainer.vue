<template>
  <div class="chat-bubble-container mt-4">
    <div
      v-for="(bubble, index) in messages"
      :key="index"
      class="chat-bubble"
    >
      {{ bubble }}
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
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    height: 100%;
    overflow-y: auto;
}

.chat-bubble-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  height: 100%;
  overflow-y: auto;
}
.chat-bubble-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 10px;
  padding-bottom: 80px;
}
.chat-bubble {
  background-color: #1a1a1b;
  color: white;
  padding: 12px 20px;
  border-radius: 20px;
  max-width: 85%;
  word-wrap: break-word;
  align-self: flex-end;
  box-shadow: 0 0px 10px #5b5b5b;
}
</style>