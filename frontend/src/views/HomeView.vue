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
    <BurgerMenu v-if="isOpenBurgerMenu" />
  </div>
</template>

<script setup lang="ts">
import Navbar from '../components/Navbar.vue'
import FooterInput from '../components/FooterInput.vue'
import ExpandedInput from '../components/ExpandedInput.vue'
import BurgerMenu from '../components/BurgerMenu.vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faBars,
  faPlus,
  faArrowUp,
  faLeaf,
  faVolumeHigh,
  faPenToSquare,
  faArrowRightLong,
  faCalendarDays,
  faUpRightAndDownLeftFromCenter,
  faDownLeftAndUpRightToCenter,
  faMagnifyingGlass
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faBars,
  faPlus,
  faArrowUp,
  faLeaf,
  faVolumeHigh,
  faPenToSquare,
  faArrowRightLong,
  faCalendarDays,
  faUpRightAndDownLeftFromCenter,
  faDownLeftAndUpRightToCenter,
  faMagnifyingGlass
)
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

// List of modules
const modules = ref([
  'Grundlagen der Programmierung',
  'Statistik',
  'Unternehmenssoftware',
  'Datenbanktechnologien',
  'Webentwicklung',
  'Betriebssysteme'
])

const sendMessage = () => {
  if (message.value.trim()) {
    chatBubbles.value.push(message.value)
    message.value = ''
  }
}

const filteredModules = computed(() => {
  return modules.value.filter((module) => module.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

const toggleOverlay = () => {
  isExpandedInputVisible.value = !isExpandedInputVisible.value
}

// const toggleBurgerMenu = () => {
//   isOpenBurgerMenu.value = !isOpenBurgerMenu.value
// }

const handleClickOutside = (event: any) => {
  const menu = burgerMenuRef.value as HTMLElement | null
  const toggleButton = menuToggleRef.value as HTMLElement | null
  if (
    isOpenBurgerMenu.value &&
    menu &&
    toggleButton &&
    !menu.contains(event.target) &&
    !toggleButton.contains(event.target)
  ) {
    isOpenBurgerMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const lineCount = computed(() => {
  return message.value.split('\n').length
})

const resizeTextarea = (event: any) => {
  const target = event.target
  target.style.height = '45px'
  target.style.height = `${Math.min(target.scrollHeight, 200)}px`
}

const reloadPage = () => {
  location.reload()
}
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
