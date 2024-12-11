<template>
  <div class="sidebar p-3 bg-black vh-100">
    <div class="search-container">
      <input
        ref="searchInput"
        type="text"
        v-model="searchQuery"
        class="sidebar-search-bar w-100"
        placeholder="Search modules..."
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
        :class="{ 'input-focused': isSearchFocused }"
      />
      <font-awesome-icon
        :icon="['fas', 'magnifying-glass']"
        class="magnifying-glass"
        :class="{ 'text-white': isSearchFocused }"
        style="cursor: pointer"
        @click="focusInput"
      />
    </div>

    <!-- Scrollable Module List -->
    <div class="module-list-container">
      <ul class="p-0 mt-1">
        <li
          v-for="(module, index) in filteredModules"
          :key="index"
          :class="[ 
            'list-item-hover', 
            'rounded', 
            'text-white', 
            'py-1', 
            {
              inactive: !isModuleActive(module),
              'cursor-pointer': isModuleActive(module),
            }
          ]"
          @click="isModuleActive(module) ? selectModule(module) : null"
        >
          <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
            <span class="module-name position-relative">
              {{ module }}
              <span
                v-if="selectedMode === 'testing'"
                class="test-mode-text text-secondary small position-absolute top-0 end-0"
              >
                (Test)
              </span>
            </span>
          </p>
        </li>
      </ul>
    </div>

    <div class="mode-toggle d-flex flex-column align-items-center modes_container p-3 pt-2">
      <div class="d-flex gap-2">
        <h6 class="m-0">
          Select a mode
          <font-awesome-icon
            :icon="['fas', 'circle-info']"
            class="circle-info"
            @click="toggleInfo"
          />
        </h6>
      </div>
      <div v-if="showInfo" class="small mt-1 text-warning text-center">
        Testing mode: A quiz feature that assesses knowledge, tracks performance,
        and provides personalized feedback.
      </div>

      <div
        class="toggle-btn-container d-flex justify-content-center mt-2 w-100"
      >
        <v-btn-toggle
          v-model="selectedMode"
          rounded="x2"
          color="#414141"
          base-color="#2a2a2a"
          class="equal-width-toggle"
        >
          <v-btn value="general" class="equal-width-btn">General</v-btn>
          <v-btn value="testing" class="equal-width-btn">Testing</v-btn>
        </v-btn-toggle>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, defineProps, defineEmits, watch } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faMagnifyingGlass, faCircleInfo } from '@fortawesome/free-solid-svg-icons';
import { VBtn, VBtnToggle } from 'vuetify/components';
import { useThread } from '../hooks/useThread';
import { clearMessages } from '../services/chatService';
import { fetchAssistantIds, modules } from '../services/moduleService';
import {
  getCurrentModuleLS,
  setCurrentModuleLS,
  getCurrentModeLS,
  setCurrentModeLS,
} from '../services/localStorageService';

library.add(faMagnifyingGlass, faCircleInfo);

const props = defineProps({
  isOpenBurgerMenu: Boolean,
  currentMode: {
    type: String,
    default: 'general',
  },
});

const emit = defineEmits(['moduleSelected']);

const searchQuery = ref('');
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const selectedMode = ref('general');
const showInfo = ref(false);

watch(
  () => props.currentMode,
  (newMode) => {
    selectedMode.value = newMode;
  }
);

const activeModules = ref<string[]>(['Grundlagen der Programmierung']);

function isModuleActive(module: string): boolean {
  return activeModules.value.includes(module);
}

const filteredModules = computed(() => {
  const query = searchQuery.value.toLowerCase();
  const filtered = modules.value.filter((module) =>
    module.toLowerCase().includes(query)
  );

  const active = filtered.filter(isModuleActive);
  const inactive = filtered.filter((module) => !isModuleActive(module));

  return [...active, ...inactive.sort()];
});

const { clearThread, initializeThread } = useThread(ref(undefined), () => {});

async function selectModule(module: string) {
  if (!isModuleActive(module)) {
    return;
  }
  console.log('Selected module:', module);

  const modeName = selectedMode.value;
  const courseName = module.replace(/ /g, '_');

  const currentModule = getCurrentModuleLS();
  const currentMode = getCurrentModeLS();

  if (module !== currentModule || modeName !== currentMode) {
    console.log('Module or mode changed. Resetting thread and messages.');

    clearMessages(false);
    clearThread();

    try {
      await fetchAssistantIds(courseName, modeName);

      setCurrentModuleLS(module);
      setCurrentModeLS(modeName);

      await initializeThread();
    } catch (error) {
      console.error('Error initializing thread:', error);
      return;
    }
  } else {
    console.log('Same module and mode selected. No action taken.');
  }

  const moduleNameWithMode =
    modeName === 'testing' ? `${module} (Test)` : module;
  emit('moduleSelected', moduleNameWithMode);
}

function focusInput() {
  searchInput.value?.focus();
}

function toggleInfo() {
  showInfo.value = !showInfo.value;
}
</script>


<style scoped>
.sidebar {
  width: 300px;
  height: 100vh;
  z-index: 9999;
  overflow-y: auto;
}

.sidebar-search-bar {
  background-color: #2a2a2a;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.5rem;
  padding-left: 2.6rem;
}

.sidebar-search-bar:focus {
  outline: none;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  color: #5b5b5b;
  transition: color 0.1s ease;
}

.module-list-container {
  max-height: calc(100vh - 200px); /* Adjust based on header/footer size */
  overflow-y: auto;
}

.list-item-hover {
  list-style-type: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.list-item-hover:hover {
  background-color: #414141;
}

.inactive {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.cursor-pointer {
  cursor: pointer !important;
}

.modes_container {
  background-color: #000000;
  bottom: 0;
  left: 0;
  width: 100%;
}

.equal-width-toggle {
  display: flex;
  justify-content: center;
  align-items: stretch;
  width: 100%;
}

.equal-width-btn {
  flex: 1 1 0;
  text-align: center;
  padding: 12px 16px;
  white-space: normal;
}

.test-mode-text {
  font-size: 0.7rem;
  position: relative;
  top: -5px;
}

.circle-info {
  cursor: pointer;
}
</style>
