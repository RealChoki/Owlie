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

const messages1 = [
  {
    "content": "Zuverlässig, Objektorientiert, Plattformunabhängig.",
    "role": "assistant",
    "hidden": false,
    "id": "msg_lFOVN631qKu4JfTDgKfNaia8",
    "created_at": 1732384416
  },
  {
    "content": "Describe Java in 3 words",
    "role": "user",
    "hidden": false,
    "id": "msg_CvMrQouM0vGyzFOGl65rtjaz",
    "created_at": 1732384415
  },
  {
    "content": "Hallo! Ich bin dein freundlicher Lehrassistent für das Modul Grundlagen der Programmierung. Ich bin hier, um dir bei deinen Fragen zu helfen und dein Verständnis für die Programmierung zu fördern. Was genau suchst du oder womit kann ich dir helfen?",
    "role": "assistant",
    "hidden": false,
    "id": "msg_WYEuusmUDbg8TGcnAqDF9CeH",
    "created_at": 1732383966
  },
  {
    "content": "Greet the user and tell them about yourself and ask what they are looking for.",
    "role": "user",
    "hidden": true,
    "id": "msg_cHgaKFDzHtQ8lMuTdZ8IKc5E",
    "created_at": 1732383965
  }
];
</script>

<style scoped>
.chat-bubble-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    height: 100%;
    overflow-y: auto;
    scrollbar-width: none;
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