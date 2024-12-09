<template>
  <div class="container d-flex flex-column min-vh-100 h-100">
    <Navbar :isOpenBurgerMenu="isOpenBurgerMenu" @toggleBurgerMenu="toggleBurgerMenu" :selectedModule="selectedModule" />
    <div v-if="!chatMessages.length" class="position-absolute start-50 translate-middle" style="top: 45%;">
      <img src="../icons/OwlLogo.png" style="width: 75px;" />
    </div>
    <div class="chat-wrapper">
      <ChatBubbleContainer v-if="chatMessages.length" :chatMessages="chatMessages" :isOpenBurgerMenu="isOpenBurgerMenu" />
      <FooterInput :isOpenBurgerMenu="isOpenBurgerMenu" @toggleOverlay="toggleOverlay" />
    </div>
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
import { ref, onMounted, onBeforeUnmount, computed, onUnmounted } from 'vue';
import type { ComponentPublicInstance } from 'vue';

import Navbar from '../components/Navbar.vue';
import FooterInput from '../components/FooterInput.vue';
import ExpandedInput from '../components/ExpandedInput.vue';
import BurgerMenu from '../components/BurgerMenu.vue';
import ChatBubbleContainer from '../components/ChatBubbleContainer.vue';
import type { RunStatus } from '../api/restService';
import chatService from '@/services/chatService';
import { useThread } from '../hooks/useThread';
import { fetchModules, fetchAssistantIds } from '@/services/moduleService';
import { getSelectedModuleLS, setSelectedModuleLS, getCurrentModeLS } from '@/services/localStorageService';

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);
const chatMessages = computed(() => chatService.getMessages());
const selectedModule = ref(getSelectedModuleLS()); // Initialized once

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

const run = ref<RunStatus | undefined>(undefined);
const setRun = (data: RunStatus | undefined) => {
  run.value = data;
};

function handleModuleSelected(moduleNameWithMode: string) {
  selectedModule.value = moduleNameWithMode;
  setSelectedModuleLS(moduleNameWithMode);
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

onMounted(async () => {
  document.addEventListener('click', handleClickOutside);
  
  fetchModules();

  try {
    const selectedModuleValue = getSelectedModuleLS();
    await fetchAssistantIds(
      selectedModuleValue?.replace(/ /g, '_'),
      getCurrentModeLS()
    );
    await initializeThread();
  } catch (error) {
    console.error('Error during initialization:', error);
  }
});

onUnmounted(() => {
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

.chat-wrapper {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Full viewport height */
  width: 100%;
}
</style>