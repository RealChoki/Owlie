<template>
  <div class="burger-menu-open p-3 bg-black rounded shadow-sm">
    <div class="search-container">
      <input
        ref="searchInput"
        type="text"
        v-model="searchQuery"
        class="burger-menu-search-bar w-100"
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
        @click="closeBurgerMenu"
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
            },
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
        Testing mode: A quiz feature that assesses knowledge, tracks
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
            value="testing"
            class="equal-width-btn"
            >Testing</v-btn
          >
        </v-btn-toggle>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  defineProps,
  defineEmits,
  watch,
  onMounted,
  onUnmounted,
} from "vue";
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
  getCurrentModuleLS,
  setCurrentModuleLS,
  getCurrentModeLS,
  setCurrentModeLS,
} from "../services/localStorageService";

library.add(faMagnifyingGlass, faCircleInfo);

const props = defineProps({
  isOpenBurgerMenu: Boolean,
});

const emit = defineEmits(["closeBurgerMenu", "moduleSelected"]);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const selectedMode = ref("general");
const showInfo = ref(false);

const activeModules = ref<string[]>(["Grundlagen der Programmierung"]);

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
  console.log("Selected module:", module);

  const modeName = selectedMode.value;
  const courseName = module.replace(/ /g, "_");

  const currentModule = getCurrentModuleLS();
  const currentMode = getCurrentModeLS();

  if (module !== currentModule || modeName !== currentMode) {
    console.log("Module or mode changed. Resetting thread and messages.");
    clearThread();
    clearMessages(false);

    try {
      await fetchAssistantIds(courseName, modeName);

      setCurrentModuleLS(module);
      setCurrentModeLS(modeName);

      await initializeThread();
    } catch (error) {
      console.error("Error initializing thread:", error);
      return;
    }
  } else {
    console.log("Same module and mode selected. No action taken.");
  }

  const moduleNameWithMode =
    modeName === "testing" ? `${module} (Test)` : module;
  emit("moduleSelected", moduleNameWithMode);
  closeBurgerMenu();
}

function closeBurgerMenu() {
  emit("closeBurgerMenu");
}

function focusInput() {
  searchInput.value?.focus();
}

function toggleInfo() {
  showInfo.value = !showInfo.value;
}

function handleResize() {
  if (window.innerWidth >= 768) {
    emit("closeBurgerMenu");
  }
}

onMounted(() => {
  window.addEventListener("resize", handleResize);
  handleResize(); // Initial check
});

// Remove the resize handler when the component is unmounted
onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
.burger-menu-open {
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  width: 80vw;
  z-index: 9999;
  min-width: 305px;
}

.module-list-container {
  max-height: 82vh;
  overflow-y: auto;
  scrollbar-width: none;
}

.burger-menu-search-bar {
  background-color: #2a2a2a;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.5rem;
  padding-left: 2.6rem;
}

.burger-menu-search-bar:focus {
  outline: none;
}

.burger-menu-search-bar::placeholder {
  transition: color 0.1s ease;
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
  transition: color 0.1s ease;
}

.input-focused::placeholder {
  color: white !important;
}

.list-item-hover {
  list-style-type: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.list-item-hover:hover {
  background-color: #414141;
}

ul.p-0 {
  padding-left: 0 !important;
  padding-right: 0 !important;
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
  max-width: 300px;
  box-sizing: border-box;
}

.equal-width-btn {
  flex: 1 1 0;
  text-align: center;
  min-width: 0;
  box-sizing: border-box;
  padding: 12px 16px;
  height: auto;
  line-height: 1.2;
  white-space: normal;
  word-wrap: break-word;
}

.info-message {
  font-size: 14px;
  color: #333;
  left: -1em;
  top: -30em;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  z-index: 1000;
}

.circle-info {
  margin-bottom: -1.5px;
  cursor: pointer;
}

/* Other styles remain the same */

.inactive {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.list-item-hover:hover {
  background-color: #414141 !important;
}

.inactive:hover {
  background-color: transparent !important;
}

.cursor-pointer {
  cursor: pointer !important;
}

.modes_container {
  background-color: #000000;
}

.small{
  max-width: 285px;
}

::v-deep(.test-mode-text) {
  position: relative;
  top: -5px; /* Adjust to position it higher */
  font-size: 0.8rem; /* Smaller font */
}

.test-mode-text {
  transform: translate(
    28px,
    -5px
  ); /* Adjust alignment relative to the module name */
  font-size: 0.7rem; /* Make it smaller */
}
</style>
