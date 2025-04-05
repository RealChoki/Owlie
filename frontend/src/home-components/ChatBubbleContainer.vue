<template>
  <div
    ref="chatContainer"
    :class="[
      'chat-bubble-container',
      'py-0',
      { 'no-scroll': props.isBurgerMenuOpen },
    ]"
  >
    <div v-for="(message, index) in messages" :key="message.id || index">
      <div v-if="message.role === 'user'" class="d-flex justify-content-end">
        <div
          :class="['chat-bubble user-msg', index === 0 ? 'mt-3 mb-4' : 'my-4']"
        >
          {{ message.content }}
        </div>
      </div>

      <div
        v-else-if="message.role === 'assistant'"
        class="position-relative assistant-msg"
        style="color: var(--text-color)"
      >
        <img
          v-if="!thinking || message.isComplete"
          :src="isDarkMode ? darkModeImage : lightModeImage"
          class="assistant-pfp p-1 pt-0"
          :style="isWideScreen ? 'position: absolute; left: 5px; top: 5px' : ''"
        />
        <div
          v-html="renderedMessages[index]"
          :style="isWideScreen ? 'margin-left: 50px' : ''"
        ></div>
        <div
          v-if="message.isComplete"
          class="position-absolute d-flex assistant-response-actions"
          :style="
            isWideScreen
              ? 'bottom: -2.1em; left: 3.07em'
              : 'bottom: -2.1em; left: 0em'
          "
        >
          <div
            class="response-action-icon cursor-pointer"
            @click="handleToggleTTS(message.content, index)"
          >
            <font-awesome-icon
              :icon="
                ttsPlayingIndex === index
                  ? ['fas', 'volume-xmark']
                  : ['fas', 'volume-high']
              "
              style="width: 0.85em"
            />
          </div>
          <div class="response-action-icon cursor-pointer" @click="handleCopy(index)">
            <font-awesome-icon
              :icon="['fas', copiedIndex === index ? 'check' : 'copy']"
            />
          </div>
          <div class="response-action-icon cursor-pointer" @click="resendMessage(index)">
            <font-awesome-icon
              :icon="['fas', 'arrow-rotate-right']"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="thinking">
      <img
        :src="isDarkMode ? darkModeImage : lightModeImage"
        alt="assistant"
        class="assistant-pfp p-1 pt-0"
      />
      <span class="thinking-animation fst-italic ms-1"
        style="color: var(--text-color)"
        >thinking<span class="dot">.</span><span class="dot">.</span
        ><span class="dot">.</span></span
      >
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed, onMounted } from "vue";
import {
  getMessages,
  getThinking,
  resendMessage,
} from "../services/chatService";
import { loadVoices, stopTTS, toggleTTS } from "../services/ttsService";
import { useScreenWidth } from "../utils/useScreenWidth";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import darkModeImage from '@/assets/icons/owl.svg'
import lightModeImage from '@/assets/icons/OwlLogoWhiteMode.png'
import { isDarkMode } from '@/services/themeService'

const messages = getMessages();
const chatContainer = ref<HTMLDivElement | null>(null);
const thinking = computed(() => getThinking());
const md = new MarkdownIt();
const { isWideScreen } = useScreenWidth();

const props = defineProps({
  isBurgerMenuOpen: {
    type: Boolean,
    required: true,
  },
});

// Funktion, um das Icon zu wechseln
const copiedIndex = ref<number | null>(null);
let copyTimer: ReturnType<typeof setTimeout> | null = null;

// Convert assistant messages from markdown to HTML
const renderedMessages = computed(() => {
  return messages.map((message) => {
    if (message.role === "assistant") {
      const markdownContent = md.render(message.content);
      // Sanitize the HTML to prevent XSS attacks
      return DOMPurify.sanitize(markdownContent);
    } else {
      return message.content;
    }
  });
});

// Handle the copy event
function handleCopy(index: number) {
  const html = renderedMessages.value[index];
  const tmp = document.createElement("div");
  tmp.innerHTML = html;
  let plainText = tmp.textContent || "";
  plainText = plainText.replace(/(\r?\n){2,}/g, "\n").trim();
  navigator.clipboard.writeText(plainText);

  if (copyTimer) clearTimeout(copyTimer);
  copiedIndex.value = index;
  copyTimer = setTimeout(() => {
    copiedIndex.value = null;
    copyTimer = null;
  }, 2500);
}

// Copy the assistant message to the clipboard
function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text);
}

const ttsPlayingIndex = ref<number | null>(null);

// Handle the tts
function handleToggleTTS(content: string, index: number) {
  if (ttsPlayingIndex.value === index) {
    stopTTS();
    ttsPlayingIndex.value = null;
  } else {
    stopTTS();
    toggleTTS(content, () => {
      ttsPlayingIndex.value = null;
    });
    ttsPlayingIndex.value = index;
  }
}

onMounted(() => {
  loadVoices();
});

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
    stopTTS();
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
  background-color: var(--chat-bubble-bg);
  color: var(--text-color);
  padding: 12px 20px;
  border-radius: 20px;
  max-width: 85%;
  display: inline-block;
  word-wrap: break-word;
  box-shadow: var(--chat-bubble-shadow);
}

.response-action-icon {
  color: var(--response-action-icon);
  font-size: 1em;
  padding: 0.1em 0.4em;
  border-radius: 8px;
  bottom: -2.1em;
  left: 3.1em;
  visibility: hidden; /* Hide icons by default */
}

.assistant-msg:hover .response-action-icon,
.assistant-response-actions:hover .response-action-icon {
  visibility: visible; /* Show icons on hover */
}

.response-action-icon:hover {
  background-color: var(--response-action-icon-hover);
}

.assistant-pfp {
  width: 40px;
  height: 40px;
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

:deep(p:last-of-type) {
  margin-bottom: 10px;
}

.no-scroll {
  overflow: hidden; /* Disable scrolling when this class is applied */
}

/* Optional: Prevent user from selecting text while scrolled */
.no-scroll * {
  user-select: none;
}

.surprise {
  animation: blink 1s steps(5, start) 3;
}

@keyframes blink {
  50% {
    background-color: yellow;
  }
}
</style>