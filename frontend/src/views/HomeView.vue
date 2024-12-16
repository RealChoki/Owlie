<template>
  <div     
    class="d-flex min-width"
  >
    <transition name="slide">
      <Sidebar
        v-if="isWideScreen && isOpenSidebar"
        @closeSidebar="closeSidebar"
        @moduleSelected="handleModuleSelected"
      />
    </transition>
    <div
      class="container d-flex flex-column vh-100"
      :style="{
        position: !isOpenSidebar && !isOpenBurgerMenu ? 'fixed' : 'relative',
        left: !isOpenSidebar && !isOpenBurgerMenu ? '50%' : 'auto',
        transform: !isOpenSidebar && !isOpenBurgerMenu ? 'translateX(-50%)' : 'none',
        transition: isWideScreen ? 'transform 0.7s ease' : 'none',
      }"
      
    >
      <Navbar
        :isOpenBurgerMenu="isOpenBurgerMenu"
        :isOpenSidebar="isOpenSidebar"
        @toggleBurgerMenu="toggleBurgerMenu"
        @toggleSidebar="toggleSidebar"
        :selectedModule="selectedModule"
      />
      <div
        v-if="!chatMessages.length"
        class="d-flex justify-content-center align-items-center h-50 logo-container"
      >
        <img src="../icons/OwlLogo.png" style="width: 75px" />
      </div>

      <div
        class="flex-grow-1 d-flex flex-column overflow-hidden"
        :class="{ 'chat-wrapper': isWideScreen }"
      >
        <ChatBubbleContainer
          v-if="chatMessages.length"
          :chatMessages="chatMessages"
          :isOpenBurgerMenu="isOpenBurgerMenu"
        />
        <FooterInput
          :messages="chatMessages"
          :isOpenBurgerMenu="isOpenBurgerMenu"
          @toggleOverlay="toggleOverlay"
        />
      </div>
      <ExpandedInput
        v-if="isExpandedInput"
        @closeExpandedInput="closeExpandedInput"
      />
      <transition name="slide">
        <BurgerMenu
          v-if="isOpenBurgerMenu"
          @closeBurgerMenu="closeBurgerMenu"
          @moduleSelected="handleModuleSelected"
          ref="burgerMenuRef"
        />
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import type { ComponentPublicInstance } from "vue";

import Navbar from "../components/Navbar.vue";
import FooterInput from "../components/FooterInput.vue";
import ExpandedInput from "../components/ExpandedInput.vue";
import BurgerMenu from "../components/BurgerMenu.vue";
import Sidebar from "@/components/Sidebar.vue";
import ChatBubbleContainer from "../components/ChatBubbleContainer.vue";
import type { RunStatus } from "../api/restService";
import chatService from "@/services/chatService";
import { useThread } from "../hooks/useThread";
import { fetchModules, fetchAssistantIds } from "@/services/moduleService";
import {
  getSelectedModuleLS,
  setSelectedModuleLS,
  getCurrentModeLS,
  getCurrentModuleLS
} from "@/services/localStorageService";
import { useScreenWidth } from "../utils/useScreenWidth";

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);
const isOpenSidebar = ref(true);
const chatMessages = computed(() => chatService.getMessages());
const selectedModule = ref(getSelectedModuleLS());

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

const run = ref<RunStatus | undefined>(undefined);
const setRun = (data: RunStatus | undefined) => {
  run.value = data;
};

function handleModuleSelected(moduleNameWithMode: string) {
  selectedModule.value = moduleNameWithMode;
  setSelectedModuleLS(moduleNameWithMode);
}

const { clearThread, initializeThread } = useThread(run, setRun);

function toggleBurgerMenu(newState: boolean) {
  isOpenBurgerMenu.value = newState;
}

function closeBurgerMenu() {
  isOpenBurgerMenu.value = false;
}

function openSidebar() {
  isOpenSidebar.value = true;
}

function closeSidebar() {
  isOpenSidebar.value = false;
}

function toggleSidebar(newState: boolean) {
  isOpenSidebar.value = newState;
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
    !(event.target as Element).closest(".navbar")
  ) {
    closeBurgerMenu();
  }
}

onMounted(async () => {
  clearThread();
  document.addEventListener("click", handleClickOutside);
  fetchModules();
  try {
    const currentModul = getCurrentModuleLS();
    await fetchAssistantIds(
      currentModul?.replace(/ /g, "_"),
      getCurrentModeLS()
    );
    await initializeThread();
  } catch (error) {
    console.error("Error during initialization:", error);
  }
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

// Use the imported useScreenWidth function
const { isWideScreen } = useScreenWidth();

watch(isWideScreen, (newVal) => {
  if (!newVal) {
    openSidebar();
  }
});

</script>

<style>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

.slide-enter-to,
.slide-leave-from {
  transform: translateX(0);
}

.container {
  background-color: #131213;
}

.logo-container {
  margin-top: 6em;
}

.chat-wrapper {
  width: 100%;
  max-width: 800px;
  align-self: center;
}

.min-width{
  min-width: 365px;
}
</style>
