<template>
  <div class="container d-flex flex-column min-vh-100 h-100">
    <Navbar
      :isOpenBurgerMenu="isOpenBurgerMenu"
      @toggleBurgerMenu="toggleBurgerMenu"
      :selectedModule="selectedModule"
    />
    <div
      v-if="chatMessages.length === 0"
      class="position-absolute start-50 translate-middle"
      style="top: 45%;"
    >
      <img src="../components/icons/OwlLogo.png" style="width: 75px;" />
    </div>
    <ChatBubbleContainer
      v-if="chatMessages.length > 0"
      :chatMessages="chatMessages"
    />
    <FooterInput
      :isOpenBurgerMenu="isOpenBurgerMenu"
      @toggleOverlay="toggleOverlay"
    />
    <ExpandedInput
      v-if="isExpandedInput"
      @closeExpandedInput="closeExpandedInput"
    />
    <BurgerMenu
      v-if="isOpenBurgerMenu"
      @closeBurgerMenu="closeBurgerMenu"
      @moduleSelected="updateSelectedModule"
      ref="burgerMenuRef"
    />
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
import chatService from '@/services/chatService';

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);

const chatMessages = computed(() => chatService.getMessages());

const selectedModule = ref('');

function updateSelectedModule(module: string) {
  selectedModule.value = module;
  localStorage.setItem('lastSelectedModule', module);
}

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

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

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  const savedModule = localStorage.getItem('lastSelectedModule');
  selectedModule.value = savedModule || 'Grundlagen der Programmierung';
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>