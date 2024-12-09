<template>
  <div ref="chatContainer" :class="['chat-bubble-container', 'py-0', { 'no-scroll': props.isOpenBurgerMenu }]">
    <div v-for="(message, index) in messages" :key="message.id || index">
      <div v-if="message.role === 'user'" class="d-flex justify-content-end">
        <div
          :class="[
            'chat-bubble user-msg',
            { 'blur-effect': props.isOpenBurgerMenu },
            index === 0 ? 'mt-2 mb-4' : 'my-4'
          ]"
        >
          {{ message.content }}
        </div>
      </div>

      <div
        v-else-if="message.role === 'assistant'"
        :class="['assistant-msg text-white', { 'blur-effect': props.isOpenBurgerMenu }]"
      >
        <img
          src="../icons/OwlLogo.png"
          alt="assistant"
          class="assistant-pfp p-1 pt-0"
        />
        <!-- Render the markdown content as HTML -->
        <div v-html="renderedMessages[index]"></div>
      </div>
    </div>
    <div v-if="thinking">
      <img
        src="../icons/OwlLogo.png"
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
import { getMessages, getThinking } from "../services/chatService";
import MarkdownIt from 'markdown-it';
import DOMPurify from 'dompurify';

const messages = getMessages();
const chatContainer = ref<HTMLDivElement | null>(null);
const thinking = computed(() => getThinking());
const md = new MarkdownIt();

// Convert assistant messages from markdown to HTML
const renderedMessages = computed(() => {
  return messages.map(message => {
    if (message.role === 'assistant') {
      const markdownContent = md.render(message.content);
      // Sanitize the HTML to prevent XSS attacks
      return DOMPurify.sanitize(markdownContent);
    } else {
      return message.content;
    }
  });
});

const props = defineProps({
  isOpenBurgerMenu: {
    type: Boolean,
    required: true,
  }
});

// Watch for changes in messages to scroll to the latest message
watch(
  messages,
  async () => {
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
  },
  { deep: true }
);
</script>

<style scoped>
.chat-bubble-container {
  padding: 10px;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  flex-grow: 1;
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

::v-deep p {
  margin-bottom: 0;
}

::v-deep p:last-of-type {
  margin-bottom: 10px; /* Adjust the value as needed */
}

.no-scroll {
  overflow: hidden; /* Disable scrolling when this class is applied */
}

/* Optional: Prevent user from selecting text while scrolled */
.no-scroll * {
  user-select: none;
}

/* Assistant message styles (change)
.assistant-msg pre {
  background-color: #2d2d2d;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 10px 0;
}

.assistant-msg code {
  background-color: #2d2d2d;
  padding: 2px 4px;
  border-radius: 3px;
  color: #e96900;
}

.assistant-msg h1,
.assistant-msg h2,
.assistant-msg h3 {
  font-weight: bold;
  margin: 10px 0 5px;
}

.assistant-msg p {
  margin: 5px 0;
}

.assistant-msg strong {
  font-weight: bold;
}

.assistant-msg em {
  font-style: italic;
}

.assistant-msg ul {
  list-style-type: disc;
  margin-left: 20px;
}

.assistant-msg ol {
  list-style-type: decimal;
  margin-left: 20px;
}
  */
</style>
