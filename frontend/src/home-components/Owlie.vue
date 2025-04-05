<template>
  <div class="d-flex justify-content-center align-items-center h-50 logo-container flex-column">
    <div class="position-relative">
      <div v-if="owlDisplayMessage !== ''" class="owl-speech-bubble p-2 position-absolute translate-middle-y">
        <p class="m-0 text-center" style="color: var(--text-color)">
          {{ owlDisplayMessage }}
        </p>
      </div>

      <img
        v-if="isDarkMode"
        src="../assets/icons/owl.svg"
        class="img-fluid owl-logo"
        style="width: 75px"
        @click="handleOwlClick"
      />
      <img
        v-else
        src="../assets/icons/OwlLogoWhiteMode.png"
        class="img-fluid owl-logo"
        style="width: 100px"
        @click="handleOwlClick"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { owlDisplayMessage } from '../services/homeService'
import { isDarkMode } from '@/services/themeService'

const clickCount = ref(0)

const playfulMessages = [
  'Hoot hoot!',
  'Boop! That tickles!',
  'I see you! Hoot!',
  'Oh, hi again!',
  'Fluffy hugs! Hoot!',
  'Peek-a-hoot!',
  'Too much love! Hoot!',
  'Hoo-hoo, still here!',
  'Careful, I’m blushing!',
  'Boop! Let’s focus!'
]

function handleOwlClick() {
  clickCount.value += 1
  const randomValue = Math.random()
  if (randomValue < 0.000001) {
    owlDisplayMessage.value =
      'Sending endless hoots of gratitude to @davidcraccer and @RealChoki for bringing me to life! 🦉✨'
  } else if (randomValue < 0.001) {
    owlDisplayMessage.value = 'The One Piece! The One Piece is real!!!'
  } else if (randomValue < 0.1) {
    displayRandomMessage()
  }
}

function displayRandomMessage() {
  const randomIndex = Math.floor(Math.random() * playfulMessages.length)
  owlDisplayMessage.value = playfulMessages[randomIndex]
}
</script>

<style scoped>
.owl-speech-bubble {
  top: -35px;
  right: -85px;
  background-color: var(--owlie-speech-bubble-bg);
  color: white;
  font-size: 0.8em;
  min-width: 100px;
  width: fit-content;
  box-shadow: var(--owlie-speech-bubble-shadow); /* Adjusted box-shadow color */
  border-radius: 10px;
}

.owl-speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -19px;
  left: 20px;
  border-width: 20px 20px 0 0;
  border-style: solid;
  border-color: var(--owlie-speech-bubble-bg) transparent;
}

.logo-container {
  margin-top: 6em;
}

.owl-logo {
  user-drag: none;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>
