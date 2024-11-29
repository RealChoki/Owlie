<template>
  <div ref="chatContainer" class="chat-bubble-container my-4 pb-5">
    <div v-for="(message, index) in messages" :key="message.id">
      <div v-if="message.role === 'user'" class="d-flex justify-content-end">
        <div
        :class="{
          'chat-bubble user-msg my-3': true,
          'blur-effect': props.isOpenBurgerMenu
        }">
          {{ message.content }}
        </div>
      </div>

      <div
        v-else-if="message.role === 'assistant'"
        class="assistant-msg text-white p-2 my-2"
      >
        <img
          src="./icons/OwlLogo.png"
          alt="assistant"
          class="assistant-pfp p-1 pt-0"
        />
        {{ message.content }}
      </div>
    </div>
    <div v-if="thinking">
      <img
        src="./icons/OwlLogo.png"
        alt="assistant"
        class="assistant-pfp p-1 pt-0"
      />
      <span class="thinking-animation text-white fst-italic ms-1"
        >thinking<span class="dot">.</span><span class="dot">.</span
        ><span class="dot">.</span></span
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from "vue";
import {
  getMessages,
  messageCount,
  getThinking,
} from "../services/chatService";

const messages = getMessages();
const chatContainer = ref<HTMLDivElement | null>(null);
const thinking = computed(() => getThinking());


const props = defineProps({
  isOpenBurgerMenu: Boolean,
});

watch(messageCount, async () => {
  await nextTick();
  if (chatContainer.value) {
    const assistantMessages =
      chatContainer.value.querySelectorAll(".assistant-msg");
    if (assistantMessages.length > 0) {
      const lastAssistantMessage = assistantMessages[
        assistantMessages.length - 1
      ] as HTMLElement;
      chatContainer.value.scrollTop =
        lastAssistantMessage.offsetTop - chatContainer.value.offsetTop;
    } else {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  }
});
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

.thinking-animation {
  display: inline-block;
}

.dot {
  animation: wave 1.5s infinite;
  display: inline-block;
  font-size: 1.5em;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.3s;
}

.dot:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes wave {
  0%,
  60%,
  100% {
    transform: initial;
  }
  30% {
    transform: translateY(-10px);
  }
}

.blur-effect {
  filter: blur(1.5px);
  pointer-events: none;
}
</style>
