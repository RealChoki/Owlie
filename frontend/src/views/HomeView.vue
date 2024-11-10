<template>
  <div class="container d-flex flex-column min-vh-100 h-100">
    <Navbar
      :isOpenBurgerMenu="isOpenBurgerMenu"
      @toggleBurgerMenu="toggleBurgerMenu"
      :selectedModule="selectedModule"
    />
    <div v-if="chatMessages.length === 0" class="logo-container">
      <img class="logo" src="../components/icons/OwlLogo.png" />
    </div>
    <ChatBubbleContainer v-if="chatMessages.length > 0" :chatMessages="chatMessages" />

    <FooterInput :isOpenBurgerMenu="isOpenBurgerMenu" @toggleOverlay="toggleOverlay" />
    <ExpandedInput v-if="isExpandedInput" @closeExpandedInput="closeExpandedInput" />
    <BurgerMenu
      v-if="isOpenBurgerMenu"
      @closeBurgerMenu="closeBurgerMenu"
      @moduleSelected="updateSelectedModule"
      ref="burgerMenuRef"
    />
  </div>
</template>

<script setup lang="ts">
import Navbar from '../components/Navbar.vue'
import FooterInput from '../components/FooterInput.vue'
import ExpandedInput from '../components/ExpandedInput.vue'
import BurgerMenu from '../components/BurgerMenu.vue'
import ChatBubbleContainer from '../components/ChatBubbleContainer.vue'
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import type { ComponentPublicInstance } from 'vue'

const isExpandedInput = ref(false)
const isOpenBurgerMenu = ref(false)

import chatService from '@/services/chatService'

const chatMessages = computed(() => chatService.getMessages())

const selectedModule = ref('')

function updateSelectedModule(module: string) {
  selectedModule.value = module
  localStorage.setItem('lastSelectedModule', module)
}

const burgerMenuRef = ref<ComponentPublicInstance | null>(null)
const toggleBurgerMenu = (newState: boolean) => {
  isOpenBurgerMenu.value = newState
  console.log('toggleBurgerMenu', isOpenBurgerMenu.value)
}

const closeBurgerMenu = () => {
  isOpenBurgerMenu.value = false
}

const closeExpandedInput = () => {
  isExpandedInput.value = false
}

const toggleOverlay = (newState: boolean) => {
  isExpandedInput.value = newState
  console.log('toggleExpandedInput', isExpandedInput.value)
}

const handleClickOutside = (event: MouseEvent) => {
  if (
    burgerMenuRef.value &&
    !burgerMenuRef.value.$el.contains(event.target) &&
    !(event.target as Element).closest('.navbar')
  ) {
    closeBurgerMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  const savedModule = localStorage.getItem('lastSelectedModule')
  if (savedModule) {
    selectedModule.value = savedModule
  } else {
    selectedModule.value = 'Grundlagen der Programmierung'
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
  position: absolute;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.logo {
  width: 75px;
}
</style>
