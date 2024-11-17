<template>
  <div class="sticky-footer container-fluid d-flex align-items-end gap-2">
    <!-- Plus Icon for Upload -->
    <font-awesome-icon :icon="['fas', 'plus']" class="cursor-pointer btn-circle align-bottom"
      style="background-color: #5b5b5b" @click="triggerFileInput" />

    <!-- Hidden File Input -->
    <input type="file" ref="fileInput" @change="handleFileChange" style="display: none;" multiple />

    <div class="textarea-container flex-grow-1">
      <textarea @input="resizeTextarea" placeholder="Type a message..." aria-label="Message input" v-model="message"
        @focus="isSearchFocused = true" @blur="isSearchFocused = false"
        :class="{ 'input-focused': isSearchFocused, 'custom-input': true, 'blur-effect': isOpenBurgerMenu }"></textarea>
      <font-awesome-icon v-if="showResizeIcon" :icon="['fas', 'up-right-and-down-left-from-center']"
        class="top-right-icon" @click="toggleOverlay" />
    </div>
    <div class="input-actions align-bottom d-flex gap-2">
      <font-awesome-icon class="btn-circle bg-white" :icon="['fas', 'arrow-up']" :class="{
        'cursor-pointer': message,
        'btn-disabled': !message,
        'blur-effect': isOpenBurgerMenu
      }" @click="sendMessage" v-if="message" />
      <!-- Text to speech when there's no message -->
      <font-awesome-icon v-else :icon="['fas', 'volume-high']" :class="{
        'cursor-pointer btn-circle bg-light align-bottom': true,
        'blur-effect': isOpenBurgerMenu
      }" @click="isOpenBurgerMenu ? null : null" />
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, defineEmits, computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faVolumeHigh } from '@fortawesome/free-solid-svg-icons'

import { sendMessage as sendChatMessage } from '../services/chatService'
import messageService from '../services/chatService'
library.add(faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faVolumeHigh)

const props = defineProps({
  isExpandedInput: Boolean,
  isOpenBurgerMenu: Boolean
})

const isSearchFocused = ref(false)
const emit = defineEmits(['toggle-overlay', 'send-message'])

const message = computed({
  get: () => messageService.getCurrentMessage(),
  set: (newMessage) => messageService.setCurrentMessage(newMessage)
})

const toggleOverlay = () => emit('toggle-overlay', !props.isExpandedInput)

function sendMessage() {
  if (message.value.trim()) {
    sendChatMessage(message.value)
    message.value = ''
  }
}

const showResizeIcon = ref(false)

function resizeTextarea(event: Event) {
  const target = event.target as HTMLTextAreaElement
  target.style.height = '45px'
  target.style.height = `${Math.min(target.scrollHeight, 200)}px`
  if (parseInt(target.style.height) <= 91 || !message) {
    showResizeIcon.value = false;
  } else {
    showResizeIcon.value = true;
  }
}

const fileInput = ref<HTMLInputElement | null>(null)
const uploadedFiles = ref<Set<string>>(new Set()) // Track already uploaded files by their names (and optionally size)

function triggerFileInput() {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    // Handle multiple files
    const files = Array.from(input.files)
    files.forEach(file => {
      const fileKey = `${file.name}-${file.size}`  // Unique identifier for file based on name and size
      if (!uploadedFiles.value.has(fileKey)) {
        uploadedFiles.value.add(fileKey)  // Mark the file as uploaded
        console.log(`Uploading file: ${file.name}`) // Here you would add your upload logic
      } else {
        console.log(`File ${file.name} is a duplicate and will not be uploaded again.`)
      }
    })

    // Reset the input after files are selected
    input.value = ""
  }
}
</script>

<style scoped>
.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  padding-bottom: 1rem;
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
  opacity: 0.7;
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
</style>
