<template>
  <div class="sidebar py-3 px-3 bg-black vh-100">
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
      <img
        src="../icons/MenuClose.png"
        class="ms-3"
        style="cursor: pointer"
        @click="closeSidebar"
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
            { 'inactive': !isModuleActive(module), 'cursor-pointer': isModuleActive(module), 'active-module': isModuleClicked(module) },
          ]"
          @click="isModuleActive(module) ? selectModule(module) : null"
        >
          <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
            <span class="module-name position-relative">
              {{ module }}
              <span
                v-if="selectedMode === 'quiz'"
                class="test-mode-text text-secondary small position-absolute top-0 end-0"
              >
                (Test)
              </span>
            </span>
          </p>
        </li>
      </ul>
    </div>

    <div
      class="mode-toggle d-flex flex-column align-items-center modes_container p-3 pt-2"
    >
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
        Quiz mode: A quiz feature that assesses knowledge, tracks
        performance, and provides personalized feedback.
      </div>

      <div
        class="toggle-btn-container d-flex justify-content-center mt-2 w-100"
      >
        <v-btn-toggle
          v-model="selectedMode"
          mandatory
          rounded="x2"
          color="#414141"
          base-color="#2a2a2a"
          class="equal-width-toggle"
        >
        <v-btn
            value="general"
            class="equal-width-btn"
            >General</v-btn
          >
          <v-btn
            value="quiz"
            class="equal-width-btn"
            >Quiz</v-btn
          >
        </v-btn-toggle>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits, onMounted } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faMagnifyingGlass,
  faCircleInfo,
} from "@fortawesome/free-solid-svg-icons";
import { VBtn, VBtnToggle } from "vuetify/components";
import { useThread } from "../hooks/useThread";
import { clearMessages } from "../services/chatService";
import { fetchAssistantIds, modules } from "../services/moduleService";
import {
  getAssistantCourseName,
  getAssistantModeName,
  setAssistantCourseName,
  setAssistantModeName,
} from "../services/openaiService";

library.add(faMagnifyingGlass, faCircleInfo);

const props = defineProps({
  isOpenSidebar: Boolean,
});

const emit = defineEmits(["closeSidebar", "moduleSelected"]);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const selectedMode = ref(getAssistantModeName() || 'general');
const moduleClicked = ref<{ module: string; mode: string } | null>(null);
const showInfo = ref(false);


const activeModules = ref<string[]>(["Grundlagen der Programmierung", "Englisch fÃ¼r Business Computing", "Statistik"]);

function isModuleActive(module: string): boolean {
  return activeModules.value.includes(module);
}

function isModuleClicked(module: string): boolean {
  return (
    moduleClicked.value !== null &&
    module === moduleClicked.value.module &&
    selectedMode.value === moduleClicked.value.mode
  );
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
  console.log("Selected module:", module);
  moduleClicked.value = { module, mode: selectedMode.value };

  const modeName = selectedMode.value;
  const courseName = module.replace(/ /g, "_");

  const currentModule = getAssistantCourseName();
  const currentMode = getAssistantModeName();

  if (module !== currentModule || modeName !== currentMode) {
    console.log("Module or mode changed. Resetting thread and messages.");
    clearThread();
    clearMessages(false);

    try {
      await fetchAssistantIds(courseName, modeName);

      setAssistantCourseName(module);
      setAssistantModeName(modeName);

      await initializeThread();
    } catch (error) {
      console.error("Error initializing thread:", error);
      return;
    }
  } else {
    console.log("Same module and mode selected. No action taken.");
  }

  

  const moduleNameWithMode =
    modeName === "quiz" ? `${module} (Test)` : module;
  emit("moduleSelected", moduleNameWithMode);
}

function closeSidebar() {
  emit("closeSidebar");
}

function focusInput() {
  searchInput.value?.focus();
}

function toggleInfo() {
  showInfo.value = !showInfo.value;
}

onMounted(() => {
  const currentModule = getAssistantCourseName();
  const currentMode = getAssistantModeName();
  if (currentModule && currentMode) {
    moduleClicked.value = { module: currentModule, mode: currentMode };
    selectedMode.value = currentMode;
  }
});
</script>

<style scoped>
.sidebar {
  height: 100vh;
  overflow-y: auto;
  min-width: 305px;
  position: relative;
  z-index: 1000;
  padding-right: 12px !important;
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

.sidebar-search-bar::placeholder {
  transition: color 0.2s ease;
}

.input-focused::placeholder {
  color: white !important;
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
  background-color: #000000;
  padding-bottom: 1em;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  color: #5b5b5b;
  transition: color 0.2s ease;
}

.module-list-container {
  max-height: 82vh;
  overflow-y: auto;
  scrollbar-width: none;
}

.list-item-hover {
  position: relative;
  padding-left: 0.2em;
  list-style-type: none;
  transition: background-color 0.4s ease, color 0.4s ease;
}

.list-item-hover:hover {
  background-color: #414141;
}

.list-item-hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(to bottom, white, #5b5b5b);
  opacity: 0;
  transition: width 0.4s ease, opacity 0.4s ease;
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

.mode-toggle {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
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
  transform: translate(
    28px,
    -5px
  );
  font-size: 0.7rem;
}

.circle-info {
  cursor: pointer;
}

.active-module {
  background-color: #2a2a2a;
  position: relative;
  overflow: hidden;
  transition: background-color 0.4s ease, color 0.4s ease;
}

.active-module::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background: linear-gradient(to bottom, white, #5b5b5b);
  opacity: 1;
}
</style>
