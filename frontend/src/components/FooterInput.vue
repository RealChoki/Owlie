<template>
  <div
    :class="[
      'sticky-footer',
      'container-fluid',
      'd-flex',
      'align-items-end',
      'gap-2',
      'pb-2',
      'px-0',
      isMessageTooLong ? 'pt-4' : 'pt-2',
      { 'fixed-grow-0': !messages.length, 'mt-auto': !messages.length}
    ]"
  >
    <div class="position-relative">
      <font-awesome-icon
        :icon="['fas', 'plus']"
        class="cursor-pointer btn-circle align-bottom"
        style="background-color: #5b5b5b"
        @click="triggerFileInput"
      />
      <span v-if="showFileCount" class="file-count-indicator bg-danger text-white">{{ fileCount }}</span>
    </div>

    <input
      type="file"
      ref="fileInput"
      @change="handleFileChange"
      style="display: none"
      multiple
    />

    <div class="textarea-container flex-grow-1">
      <textarea
        ref="textarea"
        @input="resizeTextarea"
        @keydown="handleKeydown"
        placeholder="Type a message..."
        aria-label="Message input"
        v-model="message"
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
        :class="{
          'input-focused': isSearchFocused,
          'custom-input': true,
          'blur-effect': isOpenBurgerMenu,
        }"
      ></textarea>
      <font-awesome-icon
        v-if="showResizeIcon"
        :icon="['fas', 'up-right-and-down-left-from-center']"
        class="top-right-icon"
        @click="toggleOverlay"
        :class="{ 'blur-effect': isOpenBurgerMenu }"
      />
      <div v-if="isMessageTooLong" class="character-count">
        <span :class="{ 'text-danger': isMessageTooLong }">{{ messageLength }}</span> / {{ MAX_MESSAGE_LENGTH }}
      </div>
    </div>
    <div class="input-actions align-bottom d-flex gap-2">
      <font-awesome-icon
        class="btn-circle bg-white"
        :icon="['fas', 'arrow-up']"
        :class="{
          'cursor-pointer': !disableSendButton(),
          'btn-disabled': disableSendButton(),
          'blur-effect': isOpenBurgerMenu,
        }"
        @click="sendMessage"
        v-if="message || fileCount > 0 || isFirstMessage()"
      />
      <!-- Text to speech when there's no message -->
      <font-awesome-icon
        v-else
        :icon="isTTSPlaying ? ['fas', 'volume-xmark'] : ['fas', 'volume-high']"
        :class="{
          'cursor-pointer btn-circle bg-light align-bottom': true,
          'blur-effect': isOpenBurgerMenu,
        }"
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
  faVolumeXmark,
} from "@fortawesome/free-solid-svg-icons";
import { getMessages } from '../services/chatService';
import {
  sendMessage as sendChatMessage,
  getCurrentMessage,
  setCurrentMessage,
} from "../services/chatService";
import { uploadFiles as uploadChatFiles } from "../services/filesService";
import { franc } from 'franc-min';
library.add(faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faVolumeHigh, faVolumeXmark);

import { getThreadIdLS } from '../services/localStorageService';

const props = defineProps({
  isExpandedInput: Boolean,
  isOpenBurgerMenu: Boolean,
  messages: {
    type: Array,
    required: true,
  },
});

const MAX_MESSAGE_LENGTH = 2000;

const isSearchFocused = ref(false);
const textarea = ref<HTMLTextAreaElement | null>(null)
const emit = defineEmits(["toggle-overlay", "send-message"]);

const message = computed({
  get: () => getCurrentMessage(),
  set: (newMessage) => setCurrentMessage(newMessage),
});

const messageLength = computed(() => message.value.length);
const isMessageTooLong = computed(() => messageLength.value > MAX_MESSAGE_LENGTH);

const toggleOverlay = () => emit("toggle-overlay", !props.isExpandedInput);

const isTTSPlaying = ref(false);
let utterance: SpeechSynthesisUtterance | null = null;
const availableVoices = ref<SpeechSynthesisVoice[]>([]);

// Function to load voices
const loadVoices = () => {
  availableVoices.value = window.speechSynthesis.getVoices();
};

// Language detection function using franc-min
function detectLanguage(text: string): string {
  const langCode = franc(text, { only: ['deu', 'eng', 'fra', 'spa'] });
  console.log('Detected language code:', langCode);

  switch (langCode) {
    case 'deu':
      return 'de-DE';
    case 'eng':
      return 'en-US';
    case 'fra':
      return 'fr-FR';
    case 'spa':
      return 'es-ES';
    default:
      console.warn(`Language detection failed for text: "${text}". Defaulting to 'de-DE'.`);
      return 'de-DE'; // Fallback language
  }
}

const femaleVoicesMap: { [key: string]: string } = {
  'en-US': 'Microsoft Zira - English (United States)',
  'de-DE': 'Microsoft Katja - German (Germany)',
  'fr-FR': 'Microsoft Hortense - French (France)',
  'es-ES': 'Microsoft Helena - Spanish (Spain)',
};

onMounted(() => {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = () => {
    loadVoices();
    console.log('Voices updated:', availableVoices.value.map(voice => `${voice.name} (${voice.lang})`));
  };
  window.addEventListener('beforeunload', stopTTS);
});

function isFirstMessage() {
  return getMessages()[getMessages().length - 1] === undefined
}

function disableSendButton() {
  const messages = getMessages();
  const lastMessage = messages[messages.length - 1];
  const isLastMessageFromAssistant = lastMessage?.role === "assistant" || isFirstMessage();
  const isMessageNotEmpty = message.value.trim() !== ""; // Trim whitespace
  const hasFilesAttached = fileCount.value > 0;
  const isThreadInitialized = getThreadIdLS() !== null;

  return (
    !(
      isLastMessageFromAssistant &&
      (isMessageNotEmpty || hasFilesAttached)
    ) ||
    isMessageTooLong.value ||
    !isThreadInitialized
  );
}

function sendMessage() {
  if (!disableSendButton()) {
    sendChatMessage(message.value.trim()); // Trim the message
    message.value = "";
    fileCount.value = 0;
    uploadedFiles.value.clear();
  }
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter' && !event.shiftKey && window.innerWidth > 768) {
    event.preventDefault(); // Prevent newline on Enter key
    sendMessage();
  }
}

const showResizeIcon = ref(false);

const resizeTextarea = () => {
  const target = textarea.value;
  if (!target) return;

  // Reset the height to allow shrinkage
  target.style.height = '45px';

  // Get the computed max-height from CSS
  const computedStyle = window.getComputedStyle(target);
  const maxHeight = parseFloat(computedStyle.maxHeight);

  // Calculate the new height, respecting the max-height
  const newHeight = Math.min(target.scrollHeight, maxHeight);

  target.style.height = `${newHeight}px`;

  // Update the visibility of the resize icon
  if (newHeight <= 91 || !message.value) {
    showResizeIcon.value = false;
  } else {
    showResizeIcon.value = true;
  }
};

const fileCount = ref(0);
const fileInput = ref<HTMLInputElement | null>(null);
const uploadedFiles = ref<Set<string>>(new Set());

function triggerFileInput() {
  if (fileInput.value) {
    fileInput.value.click();
  }
}

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    const files = Array.from(input.files);
    const newFiles = files.filter(file => {
      const fileKey = `${file.name}-${file.size}`;
      if (!uploadedFiles.value.has(fileKey)) {
        uploadedFiles.value.add(fileKey);
        return true;
      }
      return false;
    });
    if (newFiles.length > 0) {
      uploadChatFiles(newFiles);
      fileCount.value += newFiles.length;
    }
    input.value = "";
  }
}

function readLatestAssistantMessage() {
  if (!props.isOpenBurgerMenu && !isTTSPlaying.value) {
    console.log('readLatestAssistantMessage called');
    const messages = getMessages();
    const assistantMessages = messages.filter(message => message.role === 'assistant');
    console.log('Assistant Messages:', assistantMessages);
    if (assistantMessages.length > 0) {
      const latestMessage = assistantMessages[assistantMessages.length - 1];
      console.log('Latest Assistant Message:', latestMessage.content);
      const detectedLang = detectLanguage(latestMessage.content);
      console.log('Detected Language:', detectedLang);

      utterance = new SpeechSynthesisUtterance(latestMessage.content);
      
      // Set language based on detection
      utterance.lang = detectedLang;
      utterance.pitch = 1.1;
      utterance.rate = 1.3;
      utterance.volume = 1;

      // Log available voices
      console.log('Available Voices:', availableVoices.value.map(voice => voice.name));

      // Select female voice based on detected language
      const selectedVoiceName = femaleVoicesMap[detectedLang];
      const selectedVoice = availableVoices.value.find(voice => voice.name === selectedVoiceName);

      if (selectedVoice) {
        utterance.voice = selectedVoice;
        console.log('Selected voice:', selectedVoice.name);
      } else {
        console.warn(`No female voice found for language ${detectedLang}. Using default voice.`);
      }

      utterance.onend = () => {
        isTTSPlaying.value = false;
        console.log('TTS playback ended.');
      };

      window.speechSynthesis.cancel(); // Clear any pending speeches
      window.speechSynthesis.speak(utterance);
      isTTSPlaying.value = true;
      console.log('TTS playback started.');
    } else {
      console.log('No assistant messages to read.');
    }
  }
}

function stopTTS() {
  if (utterance) {
    window.speechSynthesis.cancel();
    isTTSPlaying.value = false;
    console.log('TTS stopped');
  }
}

function toggleTTS() {
  if (isTTSPlaying.value) {
    stopTTS();
  } else {
    readLatestAssistantMessage();
  }
}

watch(() => props.messages, () => {
  stopTTS();
}, { deep: true });

const showFileCount = computed(() => fileCount.value > 0);

watch(message, (newValue) => {
  if (newValue === '') {
    if (textarea.value) {
      textarea.value.style.height = '45px'
    }
    showResizeIcon.value = false
  } else {
    nextTick(() => {
    resizeTextarea();
    });
  }
})
</script>

<style scoped>
.sticky-footer {
  /* Remove position: fixed */
  width: 100%;
  background-color: #131213;
  z-index: 1000;
  /* Add display flex to help with alignment */
  display: flex;
  align-items: center;
}

.btn-circle {
  border-radius: 50%;
  width: 25px;
  height: 25px;
  max-width: 25px;
  max-height: 25px;
  min-width: 25px;
  min-height: 25px;
  padding: 0.5em;
}

.btn-disabled {
  background-color: rgb(196, 195, 195) !important;
  cursor: default;
}

.textarea-container {
  position: relative;
  display: flex;
  align-items: center;
  flex-grow: 1;
}

.custom-input {
  flex: 1;
  background-color: #232323;
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
  color: #232323;
  cursor: pointer;
  background-color: #5b5b5b;
  padding: 6px;
  border-radius: 50%;
}

.align-bottom {
  align-self: flex;
}

.blur-effect {
  filter: blur(1.5px);
  cursor: default !important;
  pointer-events: none;
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

.text-danger {
  color: red !important;
}

@media (min-width: 768px) {
  .custom-input {
    max-height: calc(1.5em * 10 + 16px) !important; 
  }
}
</style>