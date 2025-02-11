<template>
  <div     
    class="d-flex min-width"
  >
    <transition name="slide">
      <Sidebar
        v-if="isWideScreen && isSidebarOpen"
        @closeSidebar="closeSidebar"
      />
    </transition>
    <div
      class="container d-flex flex-column vh-100"
      :style="{
        position: !isSidebarOpen && !isBurgerMenuOpen ? 'fixed' : 'relative',
        left: !isSidebarOpen && !isBurgerMenuOpen ? '50%' : 'auto',
        transform: !isSidebarOpen && !isBurgerMenuOpen ? 'translateX(-50%)' : 'none',
        transition: isWideScreen ? 'transform 0.5s ease' : 'none',
      }"
      
    >
      <Navbar
        :isBurgerMenuOpen="isBurgerMenuOpen"
        :isSidebarOpen="isSidebarOpen"
        @toggleBurgerMenu="toggleBurgerMenu"
        @toggleSidebar="toggleSidebar"
        :class="{ 'blur-effect': isBurgerMenuOpen && !isWideScreen }"
      />
      
      <OwlLogo v-if="!chatMessages.length" :class="{ 'blur-effect': isBurgerMenuOpen && !isWideScreen }"/>
      
      <div
        class="flex-grow-1 d-flex flex-column overflow-hidden"
        :class="{ 'chat-wrapper': isWideScreen }"
      >
        <ChatBubbleContainer
          v-if="chatMessages.length"
          :chatMessages="chatMessages"
          :isBurgerMenuOpen="isBurgerMenuOpen"
          :class="{ 'blur-effect': isBurgerMenuOpen && !isWideScreen }"
        />
        <FooterInput
          class="mb-2"
          :messages="chatMessages"
          :isBurgerMenuOpen="isBurgerMenuOpen"
          @toggleOverlay="toggleOverlay"
          :class="{ 'blur-effect': isBurgerMenuOpen && !isWideScreen }"
        />
      </div>
      <ExpandedInput
        v-if="isExpandedInput"
        @closeExpandedInput="closeExpandedInput"
      />
      <transition name="slide">
        <BurgerMenu
          v-if="isBurgerMenuOpen"
          @closeBurgerMenu="closeBurgerMenu"
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
import Sidebar from "../components/Sidebar.vue";
import ChatBubbleContainer from "../components/ChatBubbleContainer.vue";
import OwlLogo from "../components/Owlie.vue"; 
import type { RunStatus } from "../api/restService";
import chatService from "../services/chatService";
import { useThread } from "../hooks/useThread";
import { fetchCourses, fetchAssistantIds } from "../services/courseService";
import {
  getAssistantCourse,
  getAssistantMode,
} from "../services/openaiService";
import { useScreenWidth } from "../utils/useScreenWidth";
import { setNavbarCourseTitle } from "../services/homeService";
import { stopTTS } from "../services/ttsService";
import WebSocketService from "../services/websocketService";
import websocketService from "../services/websocketService";

const isExpandedInput = ref(false);
const isBurgerMenuOpen = ref(false);
const isSidebarOpen = ref(true);
const chatMessages = computed(() => chatService.getMessages());

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

const run = ref<RunStatus | undefined>(undefined);
const setRun = (data: RunStatus | undefined) => {
  run.value = data;
};

const { clearThread, initializeThread } = useThread(run, setRun);

function toggleBurgerMenu(newState: boolean) {
  isBurgerMenuOpen.value = newState;
}

function closeBurgerMenu() {
  isBurgerMenuOpen.value = false;
}

function openSidebar() {
  isSidebarOpen.value = true;
}

function closeSidebar() {
  isSidebarOpen.value = false;
}

function toggleSidebar(newState: boolean) {
  isSidebarOpen.value = newState;
}

function closeExpandedInput() {
  isExpandedInput.value = false;
}

function toggleOverlay(newState: boolean) {
  isExpandedInput.value = newState;
}

const clickCount = ref(0);

// Funktion, die aufgerufen wird, wenn das Owl-Bild geklickt wird
function handleOwlClick() {
  clickCount.value += 1;
  console.log(`Owl clicked ${clickCount.value} times`);
  if (clickCount.value === 40) {
    triggerSurprise();
    clickCount.value = 0; // Zähler zurücksetzen
  }
}

// Funktion, die die Überraschung auslöst
function triggerSurprise() {
  console.log("Surprise triggered!");
  alert("OwO, what's this? Stwop pewtting me baka UwU");
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

// Define the beforeunload handler
const handleBeforeUnload = () => {
  stopTTS();
};

onMounted(async () => {
  websocketService.connectWebSocket();
  clearThread();
  window.addEventListener('beforeunload', handleBeforeUnload);
  setNavbarCourseTitle(getAssistantCourse(), getAssistantMode());
  document.addEventListener("click", handleClickOutside);
  fetchCourses();
  try {
    await fetchAssistantIds(
      getAssistantCourse(),
      getAssistantMode()
    );
    await initializeThread();
  } catch (error) {
    console.error("Error during initialization:", error);
  }
});

onUnmounted(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload);
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

.chat-wrapper {
  width: 100%;
  max-width: 800px;
  align-self: center;
}

.min-width{
  min-width: 365px;
}

.blur-effect {
  filter: blur(1.5px);
}
</style>
