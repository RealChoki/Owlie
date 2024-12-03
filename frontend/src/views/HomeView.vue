<template>
  <div class="container d-flex flex-column min-vh-100 h-100">
    <Navbar :isOpenBurgerMenu="isOpenBurgerMenu" @toggleBurgerMenu="toggleBurgerMenu" :selectedModule="selectedModule" />
    <div v-if="!chatMessages.length" class="position-absolute start-50 translate-middle" style="top: 45%;">
      <img src="../icons/OwlLogo.png" style="width: 75px;" />
    </div>
    <ChatBubbleContainer v-if="chatMessages.length" :chatMessages="chatMessages" :isOpenBurgerMenu="isOpenBurgerMenu" />
    <FooterInput :isOpenBurgerMenu="isOpenBurgerMenu" @toggleOverlay="toggleOverlay" />
    <ExpandedInput v-if="isExpandedInput" @closeExpandedInput="closeExpandedInput" />
    <transition name="slide">
      <BurgerMenu
        v-if="isOpenBurgerMenu"
        @closeBurgerMenu="closeBurgerMenu"
        @moduleSelected="handleModuleSelected"
        ref="burgerMenuRef"
      />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import type { ComponentPublicInstance } from 'vue';

import Navbar from '../components/Navbar.vue';
import FooterInput from '../components/FooterInput.vue';
import ExpandedInput from '../components/ExpandedInput.vue';
import BurgerMenu from '../components/BurgerMenu.vue';
import ChatBubbleContainer from '../components/ChatBubbleContainer.vue';
import type { RunStatus } from '../api/restService'; // Import RunStatus type if not already imported
import chatService, { clearMessages } from '@/services/chatService';
import { createNewThread, startWebSocket } from '../api/restService';
import { useThread } from '../hooks/useThread';
import axios from 'axios';

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);
const chatMessages = computed(() => chatService.getMessages());
const selectedModule = ref(localStorage.getItem('selectedModule') || '');
const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

const run = ref<RunStatus | undefined>(undefined);
const setRun = (data: RunStatus | undefined) => {
  run.value = data;
};

function handleModuleSelected(moduleNameWithMode: string) {
  selectedModule.value = moduleNameWithMode;
  localStorage.setItem('selectedModule', moduleNameWithMode);
  // Clear previous messages or thread if necessary
}

const { initializeThread } = useThread(run, setRun);

function toggleBurgerMenu(newState: boolean) {
  isOpenBurgerMenu.value = newState;
}

function closeBurgerMenu() {
  isOpenBurgerMenu.value = false;
}

function closeExpandedInput() {
  isExpandedInput.value = false;
}

function toggleOverlay(newState: boolean) {
  isExpandedInput.value = newState;
}

function handleClickOutside(event: MouseEvent) {
  if (
    burgerMenuRef.value &&
    !burgerMenuRef.value.$el.contains(event.target) &&
    !(event.target as Element).closest('.navbar')
  ) {
    closeBurgerMenu();
  }
}

// async function retrieveData() {
//   let data;
//   const storedData = null;
//   if (storedData) {
//     // data = JSON.parse(storedData);
//   } else {
//     data = {
//       run_id: "run_zVfBIidTE2rG8s92eiNtD9Qo",
//       thread_id: "thread_GTXNjmUjU3O3eV0IAJGAIc7x",
//       status: "queued",
//       required_action: null,
//       last_error: null
//     };
//     localStorage.setItem('newThreadData', JSON.stringify(data));
//   }
//   console.log(data);
// }
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  selectedModule.value = localStorage.getItem('selectedModule') || 'Grundlagen der Programmierung';
  initializeThread();
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-enter-to {
  transform: translateX(0);
}

.slide-leave-from {
  transform: translateX(0);
}

.slide-leave-to {
  transform: translateX(-100%);
}
</style>