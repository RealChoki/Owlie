<template>
  <div class="container d-flex flex-column min-vh-100">
    <Navbar :isOpenBurgerMenu="isOpenBurgerMenu" @toggleBurgerMenu="toggleBurgerMenu" />
    <!-- need to implement ai bubble first -->
    <ChatBubbleContainer />
    <div v-if="chatBubbles.length === 0" class="container my-4 logo-container">
      <img class="" src="../components/icons/dontSueChatGPT.png" />
    </div>
    <FooterInput />
    <ExpandedInput v-if="isExpandedInputVisible" />
    <BurgerMenu v-if="isOpenBurgerMenu" @closeBurgerMenu="closeBurgerMenu" ref="burgerMenuRef"/>
  </div>
</template>

<script setup lang="ts">
import Navbar from '../components/Navbar.vue'
import FooterInput from '../components/FooterInput.vue'
import ExpandedInput from '../components/ExpandedInput.vue'
import BurgerMenu from '../components/BurgerMenu.vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

// Reactive state for message input
const message = ref('')
const chatBubbles = ref<string[]>([])
const isExpandedInputVisible = ref(false)
const isOpenBurgerMenu = ref(false)
const isSearchFocused = ref(false)
const burgerMenuRef = ref(null)
const menuToggleRef = ref(null)
const searchQuery = ref('')

// Toggle burger menu
const toggleBurgerMenu = (newState: boolean) => {
  isOpenBurgerMenu.value = newState
  console.log('toggleBurgerMenu', isOpenBurgerMenu.value)
}

const closeBurgerMenu = () => {
  isOpenBurgerMenu.value = false
}

const sendMessage = () => {
  if (message.value.trim()) {
    chatBubbles.value.push(message.value)
    message.value = ''
  }
}

const toggleOverlay = () => {
  isExpandedInputVisible.value = !isExpandedInputVisible.value
}

// Handle click outside of the burger menu
const handleClickOutside = (event: MouseEvent) => {
  if (
    burgerMenuRef.value &&
    !burgerMenuRef.value.$el.contains(event.target) &&
    !(event.target as Element).closest('.navbar')
  ) {
    closeBurgerMenu()
  }
}

// Add event listener when the component is mounted
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

// Remove event listener when the component is unmounted
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
  position: relative;
  top: 0;
  bottom: 0;
  left: -42px;
  right: 0;
}
</style>
