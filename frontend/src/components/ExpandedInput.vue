<template>
  <div class="full-screen-overlay">
    <div class="h-100 p-2 pb-2" style="background-color: var(--color-gray-dark);">
      <div class="container" style="background-color: var(--color-gray-dark);">
        <div class="minimize-screen d-flex justify-content-end mt-2 mb-3" style="position: fixed; top: 10px; right: 10px; z-index: 10">
          <font-awesome-icon
            :icon="['fas', 'down-left-and-up-right-to-center']"
            @click.stop="closeExpandedInput"
            class="collapse-icon text-white cursor-pointer"
          />
        </div>
        <textarea
          class="full-screen-textarea text-white flex-grow-1"
          style="background-color: var(--color-gray-dark)"
          placeholder="Type a message..."
          aria-label="Message input"
          v-model="message"
          @focus="isSearchFocused = true"
          @blur="isSearchFocused = false"
          :class="{ 'input-focused': isSearchFocused }"
        ></textarea>
        <div class="character-count">
          <span :class="{ 'text-danger': isMessageTooLong }">{{ messageLength }}</span> / {{ MAX_MESSAGE_LENGTH }}
        </div>
        <font-awesome-icon
          class="btn-circle bg-white"
          :icon="['fas', 'arrow-up']"
          :class="{
            'cursor-pointer': !disableSendButton(),
            'btn-disabled': disableSendButton()
          }"
          style="position: fixed; bottom: 10px; right: 10px; z-index: 10"
          @click="sendMessage"
          v-if="message !== null"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed } from 'vue'
import chatService from '../services/chatService'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faDownLeftAndUpRightToCenter, faArrowUp } from '@fortawesome/free-solid-svg-icons'
import { sendMessage as sendChatMessage } from '../services/chatService'

library.add(faDownLeftAndUpRightToCenter, faArrowUp)

const props = defineProps({
  isExpandedInput: Boolean
})

const isSearchFocused = ref(false);

const emit = defineEmits(['closeExpandedInput'])

const MAX_MESSAGE_LENGTH = 2000; // Maximum allowed message length

const message = computed({
  get: () => chatService.getCurrentMessage(),
  set: (newMessage) => chatService.setCurrentMessage(newMessage)
})

const messageLength = computed(() => message.value.length)
const isMessageTooLong = computed(() => messageLength.value > MAX_MESSAGE_LENGTH)

function closeExpandedInput() {
  emit('closeExpandedInput')
}

function disableSendButton() {
  return isMessageTooLong.value || message.value.trim() === ''
}

function sendMessage() {
  if (!disableSendButton()) {
    sendChatMessage(message.value)
    message.value = ''
    closeExpandedInput()
  }
}
</script>

<style scoped>
.full-screen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1020;
}

.collapse-icon {
  font-size: 1.5rem;
  margin-right: 0.2em;
}

.container {
  width: 95%;
  height: 100%;
  position: relative;
}

.full-screen-textarea {
  flex: 1;
  width: 95%;
  height: 95%;
  border: none;
  outline: none;
  padding: 0 1em;
  font-size: 1rem;
  resize: none;
  -ms-overflow-style: none;
  scrollbar-width: none;
  margin-top: 2em;
}

.full-screen-textarea::placeholder {
  transition: color 0.2s ease;
}

.input-focused::placeholder {
  color: white !important;
}

.full-screen-textarea::-webkit-scrollbar {
  display: none;
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
  margin-right: 0.15em;
  margin-bottom: 0.4em;
}

.btn-disabled {
  background-color: var(--color-disabled) !important;
  cursor: default;
}

.character-count {
  font-size: 14px;
  color: white;
  position: absolute;
  top: 0.8em;
  left: 2em;
}

.text-danger {
  color: red !important;
}

@media (min-width: 768px) {
  ::v-deep .minimize-screen {
    position: absolute !important;
    right: 0;
    top: 0.5em;
  }

  ::v-deep .character-count {
    position: absolute !important;
    top: 0.8em;
    left: 2em;
  }

  ::v-deep .btn-circle {
    position: absolute !important;
    bottom: 0;
    right: 0;
    margin-bottom: -0.5px !important;
  }
}

</style>
