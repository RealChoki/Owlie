<template>
  <div class="sticky-footer container-fluid d-flex align-items-end gap-2">
    <font-awesome-icon
      :icon="['fas', 'plus']"
      class="cursor-pointer btn-circle align-bottom"
      style="background-color: #5b5b5b"
    />
    <div class="textarea-container flex-grow-1">
      <textarea
        :class="{ 'custom-input': true, 'blur-effect': isOpenBurgerMenu }"
        placeholder="Type a message..."
        aria-label="Message input"
        v-model="message"
        @input="resizeTextarea"
      ></textarea>
      <font-awesome-icon
        v-if="lineCount >= 3"
        :icon="['fas', 'up-right-and-down-left-from-center']"
        class="top-right-icon"
        @click="toggleOverlay"
      />
    </div>
    <div class="input-actions align-bottom d-flex gap-2">
      <font-awesome-icon
        v-if="message"
        :icon="['fas', 'arrow-up']"
        class="cursor-pointer btn-circle bg-light align-bottom"
        @click="sendMessage"
      />
      <font-awesome-icon
        v-else
        :icon="['fas', 'volume-high']"
        :class="{
          'cursor-pointer btn-circle bg-light align-bottom': true,
          'blur-effect': isOpenBurgerMenu
        }"
        @click="isOpenBurgerMenu ? null : null"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineEmits } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faVolumeHigh } from '@fortawesome/free-solid-svg-icons'
  
library.add(faUpRightAndDownLeftFromCenter, faPlus, faArrowUp, faVolumeHigh)

const emit = defineEmits(['toggle-overlay', 'send-message'])
const message = ref('')
const isOpenBurgerMenu = ref(false)
const lineCount = computed(() => message.value.split('\n').length)

function resizeTextarea(event: Event) {
  const target = event.target as HTMLTextAreaElement
  target.style.height = '45px'
  target.style.height = `${Math.min(target.scrollHeight, 200)}px`
}

function toggleOverlay() {
  // Emit an event to toggle overlay in the parent component
  emit('toggle-overlay')
}

function sendMessage() {
  if (message.value.trim()) {
    // Emit an event to send a message to the parent component
    emit('send-message', message.value)
    message.value = ''
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
    padding-top: 9px;
    padding-bottom: 9px;
    padding-left: 15px;
    width: 100%;
}

.custom-input::placeholder {
    color: white;
}

.custom-input:focus {
    outline: none;
}

.top-right-icon {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 1rem;
    color: white;
    cursor: pointer;
    z-index: 10;
}

.align-bottom {
    align-self: flex-end;
}

.blur-effect {
    filter: blur(1.5px);
    cursor: default !important;
    pointer-events: none;
}
</style>
