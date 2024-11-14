<template>
  <div class="full-screen-overlay">
    <div class="h-100 p-2 pb-2" style="background-color: #232323">
      <div class="container h-100 d-flex flex-column">
        <div class="d-flex justify-content-end mt-2 mb-3" style="position: fixed; top: 10px; right: 10px; z-index: 10">
          <font-awesome-icon
            :icon="['fas', 'down-left-and-up-right-to-center']"
            @click.stop="closeExpandedInput"
            class="collapse-icon"
          />
        </div>
        <textarea
          class="full-screen-textarea flex-grow-1 mt-3"
          style="background-color: #232323"
          placeholder="Type a message..."
          aria-label="Message input"
          v-model="message"
        ></textarea>
        <font-awesome-icon
          class="btn-circle bg-white"
          :icon="['fas', 'arrow-up']"
          :class="{
            'cursor-pointer': message,
            'btn-disabled': !message
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
import { ref, computed } from 'vue'
import chatService from '../services/chatService'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faDownLeftAndUpRightToCenter } from '@fortawesome/free-solid-svg-icons'
import { sendMessage as sendChatMessage } from '../services/chatService'
import messageService from '../services/chatService'

library.add(faDownLeftAndUpRightToCenter)

const props = defineProps({
  isExpandedInput: Boolean
})

const emit = defineEmits(['closeExpandedInput'])

const message = computed({
  get: () => chatService.getCurrentMessage(),
  set: (newMessage) => chatService.setCurrentMessage(newMessage)
})

function closeExpandedInput() {
  emit('closeExpandedInput')
}

function sendMessage() {
  if (message.value.trim()) {
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
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1020;
}

.collapse-icon {
  color: #ffffff;
  cursor: pointer;
  font-size: 1.5rem;
}

.full-screen-textarea {
  flex: 1;
  width: 95%;
  height: 100%;
  border: none;
  outline: none;
  color: #ffffff;
  padding: 1rem;
  font-size: 1rem;
  resize: none;
  -ms-overflow-style: none;
  scrollbar-width: none;
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
}

.btn-disabled {
  opacity: 0.7;
  cursor: default;
}
</style>
