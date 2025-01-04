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
        :class="['assistant-msg text-white']"
        :style="isWideScreen ? 'position: relative' : ''"
      >
        <img
          src="../assets/icons/OwlLogo.png"
          class="assistant-pfp p-1 pt-0"
          :style="isWideScreen ? 'position: absolute; left: 5px; top: 5px' : ''"
        />
        <div
          v-html="renderedMessages[index]"
          :style="isWideScreen ? 'margin-left: 50px' : ''"
        ></div>
        <div class="position-absolute d-flex assistant-response-actions">
          <font-awesome-icon
            :icon="['fas', copiedIndex === index ? 'check' : 'copy']"
            class="cursor-pointer response-action-icons"
            @click="handleCopy(index)"
          />
          <font-awesome-icon
            :icon="['fas', 'arrow-rotate-right']"
            class="cursor-pointer response-action-icons"
            @click="handleRerun(index)"
          />
        </div>
      </div>
    </div>
    <div v-if="thinking">
      <img
        src="../assets/icons/OwlLogo.png"
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
  getThinking,
  resendMessage,
} from "../services/chatService";
import { useScreenWidth } from "../utils/useScreenWidth";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCopy,
  faCheck,
  faArrowRotateRight,
} from "@fortawesome/free-solid-svg-icons";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";

library.add(faCopy, faCheck, faArrowRotateRight);

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

async function handleRerun(index: number) {
  try {
    await resendMessage(index);
  } catch (error) {
    console.error("Rerun error:", error);
  }
}

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
  box-shadow: 0 0px 10px var(--color-gray-shadow);
}

.response-action-icons {
  color: var(--color-gray-lighter);
  font-size: 1em;
  padding: 0.4em 0.5em;
  border-radius: 8px;
  bottom: -2.1em;
  left: 3.1em;
  visibility: hidden; /* Hide icons by default */
}

.assistant-msg:hover .response-action-icons,
.assistant-response-actions:hover .response-action-icons {
  visibility: visible; /* Show icons on hover */
}

.response-action-icons:hover {
  background-color: var(--color-gray-medium);
}

.assistant-pfp {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

.thinking-animation {
  display: inline-block;
}

.assistant-response-actions {
  bottom: -2.1em;
  left: 3.07em;
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

::v-deep p:last-of-type {
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