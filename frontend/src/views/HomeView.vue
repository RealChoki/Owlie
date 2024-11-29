<template>
  <div class="container d-flex flex-column min-vh-100 h-100">
    <Navbar :isOpenBurgerMenu="isOpenBurgerMenu" @toggleBurgerMenu="toggleBurgerMenu"
      :selectedModule="selectedModule" />
    <div v-if="chatMessages.length === 0" class="position-absolute start-50 translate-middle" style="top: 45%;">
      <img src="../components/icons/OwlLogo.png" style="width: 75px;" />
    </div>
    
    <ChatBubbleContainer v-if="chatMessages.length > 0" :chatMessages="chatMessages" :isOpenBurgerMenu="isOpenBurgerMenu" />
    <FooterInput :isOpenBurgerMenu="isOpenBurgerMenu" @toggleOverlay="toggleOverlay" />
    <ExpandedInput v-if="isExpandedInput" @closeExpandedInput="closeExpandedInput" />
    <transition name="slide">
      <BurgerMenu
        v-if="isOpenBurgerMenu"
        @closeBurgerMenu="closeBurgerMenu"
        @moduleSelected="handleModuleSelected"
        :currentMode="currentMode"
        :currentModule="currentModule"
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
import chatService from '@/services/chatService';
import { createNewThread, startWebSocket } from '../api/restService';

const isExpandedInput = ref(false);
const isOpenBurgerMenu = ref(false);

const chatMessages = computed(() => chatService.getMessages());

const currentModule = ref<string | undefined>(undefined);
const currentMode = ref<string>('general');

const selectedModule = ref('');

function updateSelectedModule(module: string) {
  selectedModule.value = module;
  localStorage.setItem('lastSelectedModule', module);
  handleModuleSelected(module);
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

function handleModuleSelected(moduleNameWithMode: string) {
  if (moduleNameWithMode.endsWith(' (Test)')) {
    currentMode.value = 'testing';
    currentModule.value = moduleNameWithMode.replace(' (Test)', '');
    selectedModule.value = `${currentModule.value} (Test)`;
  } else {
    currentMode.value = 'general';
    currentModule.value = moduleNameWithMode;
    selectedModule.value = currentModule.value;
  }
  // Save the current mode and module to local storage
  localStorage.setItem('currentMode', currentMode.value);
  localStorage.setItem('currentModule', currentModule.value);
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

async function retrieveData() {
  let data;
  const storedData = null;
  if (storedData) {
    // data = JSON.parse(storedData);
  } else {
    //hardcoded data for testing 
    data = {
      "run_id": "run_zVfBIidTE2rG8s92eiNtD9Qo",
      "thread_id": "thread_GTXNjmUjU3O3eV0IAJGAIc7x",
      "status": "queued",
      "required_action": null,
      "last_error": null
    }
    localStorage.setItem('newThreadData', JSON.stringify(data));
  }
  console.log(data);
}


// async function retrieveData() {
//   let data;
//   // localStorage.removeItem('newThreadData')
//   const storedData = localStorage.getItem('newThreadData');
  
//   if (storedData) {
//     data = JSON.parse(storedData);
//   } else {
//     data = await createNewThread();
//     localStorage.setItem('newThreadData', JSON.stringify(data));
//   }
//   console.log(data);
//   //[Log] {run_id: "run_xXCT808DzQkmBHCkckDxYYT0", thread_id: "thread_wk7RAhj9oKImmFOeX8g95aW3", status: "queued", required_action: null, last_error: null} (HomeView.vue, line 49)
// }

onMounted(() => {
  retrieveData();
  document.addEventListener('click', handleClickOutside);

  // Retrieve the saved module and mode from local storage
  const savedModule = localStorage.getItem('currentModule');
  const savedMode = localStorage.getItem('currentMode');

  if (savedModule) {
    currentModule.value = savedModule;
    if (savedMode === 'testing') {
      selectedModule.value = `${savedModule} (Test)`;
    } else {
      selectedModule.value = savedModule;
    }
  } else {
    selectedModule.value = 'Grundlagen der Programmierung';
  }

  if (savedMode) {
    currentMode.value = savedMode;
  }
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
::v-deep(.slide-enter-active),
::v-deep(.slide-leave-active) {
  transition: transform 0.5s ease;
}

::v-deep(.slide-enter) {
  transform: translateX(-100%);
}

::v-deep(.slide-enter-to) {
  transform: translateX(0);
}

::v-deep(.slide-leave) {
  transform: translateX(0);
}

::v-deep(.slide-leave-to) {
  transform: translateX(-100%);
}
</style>