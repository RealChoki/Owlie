<template>
  <div class="mt-auto">
    <div v-if="fileCount > 0" class="d-flex justify-content-end mb-2 mx-5 px-2 mb-3">
      <span v-if="tooltipVisible" class="mode-tooltip" :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }">
        {{ hoveredFilename }}
      </span>
      <div
        class="d-flex gap-1 align-items-center justify-content-end"
        :style="{
          width: isMessageTooLong ? textareaWidth - 110 + 'px' : ''
        }"
        style="margin-bottom: -0.5em; overflow: auto"
      >
        <div
          v-for="(file, index) in uploadedFiles"
          :key="index"
          class="d-flex align-items-center p-2 rounded-4 shortened-link file-div position-relative"
          @mouseenter="showTooltip(file.name)"
          @mouseleave="hideTooltip"
          @mousemove="updateTooltipPosition"
        >
          <!-- Shortened display -->
          <span
            style="color: var(--text-color); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 11px; cursor: default"
            >{{ file.name }}</span
          >
          <font-awesome-icon
            :icon="['fas', 'times']"
            class="cursor-pointer rounded-4 x-icon"
            style="width: 15px; height: 15px"
            @click="removeFile(file)"
          />
        </div>
      </div>
    </div>
    <div
      class="sticky-footer container-fluid d-flex align-items-end gap-2 px-0 mt-2 mb-2"
      :class="{
        'mt-auto': !messages.length && !fileCount
      }"
    >
      <!-- File Upload Button -->
      <div class="position-relative">
        <font-awesome-icon
          :icon="['fas', 'plus']"
          class="cursor-pointer btn-circle align-self-end icon-click-effect"
          style="background-color: var(--color-gray-shadow)"
          @click="triggerFileInput(fileInput)"
        />
        <span v-if="fileCount" class="file-count-indicator bg-danger"
        style="color: var(--text-color)">
          {{ fileCount }}
        </span>
      </div>

      <!-- Hidden File Input -->
      <input
        type="file"
        ref="fileInput"
        @change="onFilesSelected"
        style="display: none"
        multiple
        :accept="computedAcceptedFileTypes.join(', ')"
      />

      <!-- Textarea Container -->
      <div class="position-relative d-flex align-items-center flex-grow-1">
        <textarea
          ref="textarea"
          placeholder="Type a message..."
          aria-label="Message input"
          v-model="currentUserInput"
          @input="resizeTextarea"
          @keydown="handleKeydown"
          @focus="isSearchFocused = true"
          @blur="isSearchFocused = false"
          :class="{
            'input-focused': isSearchFocused,
            'custom-input': true,
            'cursor-default': isBurgerMenuOpen
          }"
        ></textarea>

        <!-- Resize Icon -->
        <font-awesome-icon
          v-if="showResizeIcon"
          :icon="['fas', 'up-right-and-down-left-from-center']"
          class="top-right-icon cursor-pointer icon-click-effect"
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
          v-if="isCurrentAssistantResponseComplete"
          :icon="['fas', 'arrow-up']"
          :class="{
            'cursor-pointer icon-click-effect': !disableSendButton() && !isBurgerMenuOpen,
            'btn-disabled': disableSendButton()
          }"
          class="btn-circle bg-white"
          @click="sendMessage"
        />
        <font-awesome-icon
          v-else
          :icon="['fas', 'stop']"
          class="cursor-pointer btn-circle bg-light align-self-end icon-click-effect"
          @click="cancelAssistantResponse"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faUpRightAndDownLeftFromCenter,
  faPlus,
  faArrowUp,
  faStop,
  faFile,
  faTimes
} from '@fortawesome/free-solid-svg-icons'
import {
  getMessages,
  sendMessage as sendChatMessage,
  currentUserInput,
  cancelAssistantResponse,
  isCurrentAssistantResponseComplete
} from '../services/chatService'
import {
  fileCount,
  uploadedFiles,
  onFilesSelected,
  resetFileCount,
  triggerFileInput,
  removeFile,
  computedAcceptedFileTypes
} from '../services/filesService'
import { getAssistantThreadId } from '../services/openaiService'
import { get } from 'http'

library.add(faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faStop, faFile, faTimes)

const tooltipX = ref(0)
const tooltipY = ref(0)
const hoveredFilename = ref('')
const tooltipVisible = ref(false)

function showTooltip(name: string) {
  hoveredFilename.value = name
  tooltipVisible.value = true
}

function hideTooltip() {
  hoveredFilename.value = ''
  tooltipVisible.value = false
}

function updateTooltipPosition(event: MouseEvent) {
  tooltipX.value = event.pageX - 300
  tooltipY.value = event.pageY - 30
}

// Constants
const MAX_MESSAGE_LENGTH = 2000

// Props
const props = defineProps({
  isExpandedInput: Boolean,
  isBurgerMenuOpen: Boolean,
  messages: {
    type: Array,
    required: true
  }
})

// Emits
const emit = defineEmits(['toggle-overlay', 'send-message'])

// Refs
const isSearchFocused = ref(false)
const textarea = ref<HTMLTextAreaElement | null>(null)
const textareaWidth = ref(0)
const fileInput = ref<HTMLInputElement | null>(null)
const showResizeIcon = ref(false)

// Computed properties
const messageLength = computed(() => currentUserInput.value.length)
const isMessageTooLong = computed(() => messageLength.value > MAX_MESSAGE_LENGTH)

// Methods
const toggleOverlay = () => emit('toggle-overlay', !props.isExpandedInput)

const isFirstMessage = () => getMessages().length === 0

const disableSendButton = () => {
  const isLastMessageFromAssistant = () => {
    const messages = getMessages()
    const lastMessage = messages[messages.length - 1]
    return (lastMessage?.role === 'assistant' && lastMessage.isComplete) || isFirstMessage()
  }

  const isMessageValid = () => {
    return currentUserInput.value.trim() !== '' || fileCount.value > 0
  }

  return (
    !(isLastMessageFromAssistant() && isMessageValid()) || isMessageTooLong.value || !Boolean(getAssistantThreadId())
  )
}

interface ExtendedFile extends File {
  content?: string | ArrayBuffer | null
}

const sendMessage = () => {
  if (!disableSendButton() && !props.isBurgerMenuOpen) {
    let finalMessage = currentUserInput.value.trim()

    // Gather file content as hidden data
    const hiddenFileContents = Array.from(uploadedFiles.value).map((file) => {
      const typedFile = file as ExtendedFile
      return {
        name: typedFile.name,
        content: typedFile.content
      }
    })

    console.log('Sending message:', finalMessage)
    // Pass hidden file content separately
    sendChatMessage(finalMessage, hiddenFileContents)
    resetFileCount()
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey && window.innerWidth > 768) {
    event.preventDefault()
    sendMessage()
  }
}

const resizeTextarea = () => {
  const target = textarea.value
  if (!target) return

  target.style.height = '45px' // Reset height
  const maxHeight = parseFloat(window.getComputedStyle(target).maxHeight)
  const newHeight = Math.min(target.scrollHeight, maxHeight)

  target.style.height = `${newHeight}px`
  showResizeIcon.value = newHeight > 91 && Boolean(currentUserInput.value)
}

const resetTextareaHeight = () => {
  if (textarea.value) {
    textarea.value.style.height = '45px'
  }
  showResizeIcon.value = false
}

const updateWidth = () => {
  textareaWidth.value = textarea.value.offsetWidth
}

// Lifecycle hooks
onMounted(() => {
  updateWidth()
  window.addEventListener('resize', updateWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWidth)
})

// Watchers
// idk if we need this
watch(
  () => props.messages,
  () => {},
  { deep: true }
)

watch(currentUserInput, (newValue) => {
  if (newValue === '') {
    resetTextareaHeight()
  } else {
    nextTick(resizeTextarea)
  }
})

watch(fileCount, () => {
  updateWidth()
})
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
  color: var(--text-color);
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
  color: var(--text-color) !important;
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

.shortened-link {
  position: relative;
  max-width: 125px;
  max-height: 40px;
  z-index: 1001;
}

.mode-tooltip {
  position: absolute;
  background-color: #333;
  color: #fff;
  padding: 0.4em 0.6em;
  border-radius: 4px;
  font-size: 0.65rem;
  white-space: nowrap;
  pointer-events: none; /* So the mouse can pass through to the parent element */
  z-index: 9999;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

.file-div {
  background-color: var(--color-gray-shadow);
  height: 1.6em;
}

.x-icon {
  color: rgb(189, 189, 189);
  padding: 0.15em;
}
</style>
