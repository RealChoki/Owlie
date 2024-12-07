<template>
  <div class="sticky-footer container-fluid d-flex align-items-end gap-2 py-2">
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
          'btn-disabled': !message && fileCount === 0 || disableSendButton(),
          'blur-effect': isOpenBurgerMenu,
        }"
        @click="sendMessage"
        v-if="message || fileCount > 0 || isFirstMessage()"
      />
      <!-- Text to speech when there's no message -->
      <font-awesome-icon
        v-else
        :icon="['fas', 'volume-high']"
        :class="{
          'cursor-pointer btn-circle bg-light align-bottom': true,
          'blur-effect': isOpenBurgerMenu,
        }"
        @click="readLatestAssistantMessage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, computed, watch } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faUpRightAndDownLeftFromCenter,
  faPlus,
  faArrowUp,
  faVolumeHigh,
} from "@fortawesome/free-solid-svg-icons";
import { getMessages } from '../services/chatService';
import {
  sendMessage as sendChatMessage,
  getCurrentMessage,
  setCurrentMessage,
} from "../services/chatService";
import { uploadFiles as uploadChatFiles } from "../services/filesService";
import fileService from "../services/filesService";
library.add(faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faVolumeHigh);

const props = defineProps({
  isExpandedInput: Boolean,
  isOpenBurgerMenu: Boolean,
});

const MAX_MESSAGE_LENGTH = 2000; // Set your desired maximum message length

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

function isFirstMessage() {
  return getMessages()[getMessages().length - 1] === undefined
}
function disableSendButton() {
  const messages = getMessages();
  const lastMessage = messages[messages.length - 1];
  const isLastMessageFromAssistant = lastMessage?.role === "assistant" || isFirstMessage();
  const isMessageNotEmpty = message.value.trim() !== "";
  const hasFilesAttached = fileCount.value > 0;

  return (
    !(isLastMessageFromAssistant && (isMessageNotEmpty || hasFilesAttached)) ||
    isMessageTooLong.value
  );
}

function sendMessage() {
  if (!disableSendButton()) {
    sendChatMessage(message.value);
    message.value = "";
    fileCount.value = 0;
    uploadedFiles.value.clear();
  }
}

const showResizeIcon = ref(false);

function resizeTextarea(event: Event) {
  const target = event.target as HTMLTextAreaElement;
  target.style.height = "45px";
  target.style.height = `${Math.min(target.scrollHeight, 200)}px`;
  if (parseInt(target.style.height) <= 91 || !message) {
    showResizeIcon.value = false;
  } else {
    showResizeIcon.value = true;
  }
}

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
      fileCount.value += newFiles.length; // Increment the file count
    }
    input.value = ""; // Reset the input after files are selected
  }
}

function readLatestAssistantMessage() {
  if (!props.isOpenBurgerMenu) {
    console.log('readLatestAssistantMessage called');
    const messages = getMessages();
    const assistantMessages = messages.filter(message => message.role === 'assistant');
    console.log('Assistant Messages:', assistantMessages);
    if (assistantMessages.length > 0) {
      const latestMessage = assistantMessages[assistantMessages.length - 1];
      console.log('Latest Assistant Message:', latestMessage.content);
      const utterance = new SpeechSynthesisUtterance(latestMessage.content);
      
      // Customize the speech properties
      utterance.lang = 'de-DE'; // Set language to German
      utterance.pitch = 1.1;
      utterance.rate = 1.2;
      utterance.volume = 1;

      // Select a female voice
      const voices = window.speechSynthesis.getVoices();
      const femaleGermanVoice = voices.find(voice => voice.lang === 'de-DE' && voice.name.includes('female'));
      if (femaleGermanVoice) {
        utterance.voice = femaleGermanVoice;
        console.log('Selected voice:', femaleGermanVoice.name);
      }

      window.speechSynthesis.cancel(); // Clear any pending speeches
      window.speechSynthesis.speak(utterance);
    } else {
      console.log('No assistant messages to read.');
    }
  }
}

const showFileCount = computed(() => fileCount.value > 0);

watch(message, (newValue) => {
  if (newValue === '') {
    if (textarea.value) {
      textarea.value.style.height = '45px'
    }
    showResizeIcon.value = false
  } else {
    resizeTextarea({ target: textarea.value } as Event)
    console.log('Resizing textarea')
  }
})
</script>

<style scoped>
.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #131213;
  z-index: 1000;
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
  max-height: 200px;
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
</style>