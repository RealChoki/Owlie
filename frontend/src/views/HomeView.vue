<template>
  <div     
    class="d-flex min-width"
  >
    <transition name="slide">
      <Sidebar
        v-if="isWideScreen && isOpenSidebar"
        @closeSidebar="closeSidebar"
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
        :class="{ 'blur-effect': isOpenBurgerMenu && !isWideScreen }"
      />
      
      <OwlLogo v-if="!chatMessages.length" :class="{ 'blur-effect': isOpenBurgerMenu && !isWideScreen }"/>
      
      <div
        class="flex-grow-1 d-flex flex-column overflow-hidden"
        :class="{ 'chat-wrapper': isWideScreen }"
      >
        <ChatBubbleContainer
          v-if="chatMessages.length"
          :chatMessages="chatMessages"
          :isOpenBurgerMenu="isOpenBurgerMenu"
          :class="{ 'blur-effect': isOpenBurgerMenu && !isWideScreen }"
        />
        <FooterInput
          class="mb-2"
          :messages="chatMessages"
          :isOpenBurgerMenu="isOpenBurgerMenu"
          @toggleOverlay="toggleOverlay"
          :class="{ 'blur-effect': isOpenBurgerMenu && !isWideScreen }"
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

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);
const isOpenSidebar = ref(true);
const chatMessages = computed(() => chatService.getMessages());

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

const run = ref<RunStatus | undefined>(undefined);
const setRun = (data: RunStatus | undefined) => {
  run.value = data;
};

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

onMounted(async () => {
  clearThread();
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
