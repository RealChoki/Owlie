<template>
  <div class="container d-flex flex-column min-vh-100">
    <Navbar
      :isOpenBurgerMenu="isOpenBurgerMenu"
      @toggleBurgerMenu="toggleBurgerMenu"
      :selectedModule="selectedModule" 
    />
    <div v-if="chatMessages.length === 0" class="container my-4 logo-container">
      <img class="" src="../components/icons/dontSueChatGPT.png" />
    </div>

    <ChatBubbleContainer :chatMessages="chatMessages" />
    
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
import Navbar from "../components/Navbar.vue";
import FooterInput from "../components/FooterInput.vue";
import ExpandedInput from "../components/ExpandedInput.vue";
import BurgerMenu from "../components/BurgerMenu.vue";
import ChatBubbleContainer from "../components/ChatBubbleContainer.vue";
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import type { ComponentPublicInstance } from "vue";

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);

import chatService from "@/services/chatService";

const chatMessages = computed(() => chatService.getMessages());

const selectedModule = ref('')

function updateSelectedModule(module: string) {
  selectedModule.value = module;
  localStorage.setItem("lastSelectedModule", module);
}

const burgerMenuRef = ref<ComponentPublicInstance | null>(null);
const toggleBurgerMenu = (newState: boolean) => {
  isOpenBurgerMenu.value = newState;
  console.log("toggleBurgerMenu", isOpenBurgerMenu.value);
};

const closeBurgerMenu = () => {
  isOpenBurgerMenu.value = false;
};

const closeExpandedInput = () => {
  isExpandedInput.value = false;
};

const toggleOverlay = (newState: boolean) => {
  isExpandedInput.value = newState;
  console.log("toggleExpandedInput", isExpandedInput.value);
};

// Handle click outside of the burger menu
const handleClickOutside = (event: MouseEvent) => {
  if (
    burgerMenuRef.value &&
    !burgerMenuRef.value.$el.contains(event.target) &&
    !(event.target as Element).closest(".navbar")
  ) {
    closeBurgerMenu();
  }
};

// Add event listener when the component is mounted
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  const savedModule = localStorage.getItem("lastSelectedModule");
  if (savedModule) {
    selectedModule.value = savedModule;
  } else {
    selectedModule.value = "Grundlagen der Programmierung";
  }
});

// Remove event listener when the component is unmounted
onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
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


.chat-bubble-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    height: 100%;
    overflow-y: auto;
}

.chat-bubble-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  height: 100%;
  overflow-y: auto;
}
.chat-bubble-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 10px;
  padding-bottom: 80px; /* Space for input area */
}
.chat-bubble {
  background-color: #1a1a1b;
  color: white;
  padding: 12px 20px;
  border-radius: 20px;
  max-width: 85%;
  word-wrap: break-word;
  align-self: flex-end; /* Align to the right side for user messages */
  box-shadow: 0 0px 10px #5b5b5b;
}
</style>
