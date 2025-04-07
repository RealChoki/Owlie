<template>
  <div class="d-flex justify-content-center align-items-center h-50 logo-container flex-column">
    <div class="position-relative">
      <div v-if="owlDisplayMessage !== ''" class="owl-speech-bubble p-2 position-absolute translate-middle-y">
        <p class="m-0 text-center" style="color: var(--text-color)">
          {{ owlDisplayMessage }}
        </p>
      </div>

      <img
        src="../assets/icons/owl-filled-white.png"
        class="img-fluid owl-logo"
        style="width: 75px;"
        :style="isDarkMode ? 'filter: brightness(0.8)' : ''"
        @click="handleOwlClick"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { owlDisplayMessage } from '../services/homeService'
import { isDarkMode } from '@/services/themeService'

const { t } = useI18n()

const clickCount = ref(0)

const playfulMessages = [
  t('owlie.default'),
  t('owlie.boop'),
  t('owlie.greeting'),
  t('owlie.blushing'),
  t('owlie.focus'),
]

function handleOwlClick() {
  clickCount.value += 1
  const randomValue = Math.random()
  if (randomValue < 0.000001) {
    owlDisplayMessage.value = t('owlie.onePiece')
  } else if (randomValue < 0.001) {
    owlDisplayMessage.value = t('owlie.thankYou')
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
