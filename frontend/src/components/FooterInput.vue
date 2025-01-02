<template>
  <div
    class="sticky-footer container-fluid d-flex align-items-end gap-2 pb-2 px-0"
    :class="{
      'pt-4': isMessageTooLong,
      'pt-2': !isMessageTooLong,
      'mt-auto': !messages.length,
    }"
  >
    <!-- File Upload Button -->
    <div class="position-relative">
      <font-awesome-icon
        :icon="['fas', 'plus']"
        class="cursor-pointer btn-circle align-self-end"
        style="background-color: var(--color-gray-shadow)"
        @click="triggerFileInput(fileInput)"
      />
      <span
        v-if="showFileCount"
        class="file-count-indicator bg-danger text-white"
      >
        {{ fileCount }}
      </span>
    </div>

    <!-- Hidden File Input -->
    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      style="display: none"
      multiple
    />

    <!-- Textarea Container -->
    <div class="position-relative d-flex align-items-center flex-grow-1">
      <textarea
        ref="textarea"
        placeholder="Type a message..."
        aria-label="Message input"
        v-model="message"
        @input="resizeTextarea"
        @keydown="handleKeydown"
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
        :class="{
          'input-focused': isSearchFocused,
          'custom-input': true,
        }"
      ></textarea>

      <!-- Resize Icon -->
      <font-awesome-icon
        v-if="showResizeIcon"
        :icon="['fas', 'up-right-and-down-left-from-center']"
        class="top-right-icon cursor-pointer"
        @click="toggleOverlay"
      />

      <!-- Character Count -->
      <div v-if="isMessageTooLong" class="character-count">
        <span :class="{ 'text-danger': isMessageTooLong }">
          {{ messageLength }}
        </span>
        / {{ MAX_MESSAGE_LENGTH }}
      </div>
    </div>

    <!-- Input Actions -->
    <div class="input-actions align-self-end d-flex gap-2">
      <!-- Send Button -->
      <font-awesome-icon
        v-if="message || fileCount > 0 || isFirstMessage()"
        :icon="['fas', 'arrow-up']"
        :class="{
          'cursor-pointer': !disableSendButton(),
          'btn-disabled': disableSendButton(),
        }"
        class="btn-circle bg-white"
        @click="sendMessage"
      />

      <!-- Text-to-Speech Button -->
      <font-awesome-icon
        v-else
        :icon="isTTSPlaying ? ['fas', 'volume-xmark'] : ['fas', 'volume-high']"
        class="cursor-pointer btn-circle bg-light align-self-end"
        @click="toggleTTS"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, computed, watch, nextTick, onMounted } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { 
  faUpRightAndDownLeftFromCenter, 
  faPlus, 
  faArrowUp, 
  faVolumeHigh, 
  faVolumeXmark 
} from "@fortawesome/free-solid-svg-icons";
import { 
  getMessages, 
  sendMessage as sendChatMessage, 
  getCurrentMessage, 
  setCurrentMessage 
} from "../services/chatService";
import { 
  fileCount, 
  uploadedFiles, 
  handleFileChange, 
  resetFileCount, 
  triggerFileInput 
} from "../services/filesService";
import { franc } from "franc-min";
import { 
  loadVoices, 
  readLatestAssistantMessage, 
  stopTTS, 
  toggleTTS, 
  availableVoices, 
  isTTSPlaying 
} from "../services/ttsService";
import { getAssistantThreadId } from "../services/openaiService";

library.add(
  faUpRightAndDownLeftFromCenter,
  faPlus,
  faArrowUp,
  faVolumeHigh,
  faVolumeXmark
);

// Constants
const MAX_MESSAGE_LENGTH = 2000;

// Props
const props = defineProps({
  isExpandedInput: Boolean,
  isBurgerMenuOpen: Boolean,
  messages: {
    type: Array,
    required: true,
  },
});

// Emits
const emit = defineEmits(["toggle-overlay", "send-message"]);

// Refs
const isSearchFocused = ref(false);
const textarea = ref<HTMLTextAreaElement | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const showResizeIcon = ref(false);

// Computed properties
const message = computed({
  get: getCurrentMessage,
  set: setCurrentMessage,
});

const messageLength = computed(() => message.value.length);
const isMessageTooLong = computed(() => messageLength.value > MAX_MESSAGE_LENGTH);
const showFileCount = computed(() => fileCount.value > 0);

// Lifecycle hooks
onMounted(() => {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = () => {
    loadVoices();
    console.log(
      "Voices updated:",
      availableVoices.value.map((voice) => `${voice.name} (${voice.lang})`)
    );
  };
  window.addEventListener("beforeunload", stopTTS);
});

// Watchers
watch(
  () => props.messages,
  stopTTS,
  { deep: true }
);

watch(message, (newValue) => {
  if (newValue === "") {
    resetTextareaHeight();
  } else {
    nextTick(resizeTextarea);
  }
});

// Methods
const toggleOverlay = () => emit("toggle-overlay", !props.isExpandedInput);

const isFirstMessage = () => !getMessages().length;

const disableSendButton = () => {
  const messages = getMessages();
  const lastMessage = messages[messages.length - 1];
  const isLastMessageFromAssistant = 
    lastMessage?.role === "assistant" || isFirstMessage();
  const isMessageNotEmpty = message.value.trim() !== "";
  const hasFilesAttached = fileCount.value > 0;
  const isThreadInitialized = Boolean(getAssistantThreadId());

  return (
    !(isLastMessageFromAssistant && (isMessageNotEmpty || hasFilesAttached)) ||
    isMessageTooLong.value ||
    !isThreadInitialized
  );
};

const sendMessage = () => {
  if (!disableSendButton()) {
    sendChatMessage(message.value.trim());
    message.value = "";
    resetFileCount();
  }
};

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === "Enter" && !event.shiftKey && window.innerWidth > 768) {
    event.preventDefault();
    sendMessage();
  }
};

const resizeTextarea = () => {
  const target = textarea.value;
  if (!target) return;

  target.style.height = "45px"; // Reset height
  const maxHeight = parseFloat(window.getComputedStyle(target).maxHeight);
  const newHeight = Math.min(target.scrollHeight, maxHeight);

  target.style.height = `${newHeight}px`;
  showResizeIcon.value = newHeight > 91 && Boolean(message.value);
};

const resetTextareaHeight = () => {
  if (textarea.value) {
    textarea.value.style.height = "45px";
  }
  showResizeIcon.value = false;
};
</script>

<style scoped>
.sticky-footer {
  z-index: 1000;
}

.btn-circle {
  border-radius: 50%;
  width: 25px;
  height: 25px;
  padding: 0.5em;
}

.btn-disabled {
  background-color: var(--color-disabled) !important;
  cursor: default;
}

.custom-input {
  flex: 1;
  background-color: var(--color-gray-dark);
  border: none;
  color: white;
  border-radius: 25px;
  height: 45px;
  max-height: calc(1.5em * 6 + 16px);
  resize: none;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 15px;
  padding-right: 10px;
  width: 100%;
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

.custom-input::-webkit-scrollbar {
  display: none;
}

.custom-input:focus {
  outline: none;
}

.custom-input::placeholder {
  transition: color 0.2s ease;
}

.top-right-icon {
  position: absolute;
  top: 7px;
  right: 7px;
  font-size: 0.8rem;
  color: var(--color-gray-dark);
  background-color: var(--color-gray-shadow);
  padding: 6px;
  border-radius: 50%;
}

.input-focused::placeholder {
  color: white !important;
}

.file-count-indicator {
  position: absolute;
  top: -5px;
  right: -5px;
  color: black;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}

.character-count {
  font-size: 12px;
  color: white;
  position: absolute;
  top: -20px;
  left: 20px;
}

@media (min-width: 768px) {
  .custom-input {
    max-height: calc(1.5em * 10 + 16px) !important;
  }
}
</style>