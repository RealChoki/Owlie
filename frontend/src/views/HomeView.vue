<template>
  <div     
    class="d-flex min-width"
  >
    <transition name="slide">
      <Sidebar
        v-if="isWideScreen && isOpenSidebar"
        @closeSidebar="closeSidebar"
        @courseSelected="handleCourseSelected"
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
        :selectedCourse="selectedCourse"
      />
      <div
        v-if="!chatMessages.length"
        class="d-flex justify-content-center align-items-center h-50 logo-container"
      >
      <img
        src="../icons/OwlLogo.png"
        style="width: 75px"
        @click="handleOwlClick"
        :class="{ 'blur-effect': isOpenBurgerMenu && !isWideScreen }"
      />
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
          class="mb-2"
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
          @courseSelected="handleCourseSelected"
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
import { fetchCourses, fetchAssistantIds } from "@/services/courseService";
import {
  getAssistantCourseName,
  getAssistantModeName,
  setAssistantCourseName,
} from "@/services/openaiService";
import { useScreenWidth } from "../utils/useScreenWidth";

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);
const isOpenSidebar = ref(true);
const chatMessages = computed(() => chatService.getMessages());
const selectedCourse = ref(getAssistantCourseName());

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);

const run = ref<RunStatus | undefined>(undefined);
const setRun = (data: RunStatus | undefined) => {
  run.value = data;
};

function handleCourseSelected(CourseNameWithMode: string) {
  selectedCourse.value = CourseNameWithMode;
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
  // Hier kannst du weitere überraschende Aktionen hinzufügen, z.B. Animationen, Sounds etc.
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
  fetchCourses();
  try {
    const currentCourse = getAssistantCourseName();
    await fetchAssistantIds(
      currentCourse?.replace(/ /g, "_"),
      getAssistantModeName()
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

.blur-effect {
  filter: blur(2px);
}
</style>
