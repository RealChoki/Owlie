<template>
    <div ref="burgerMenuRef" class="burger-menu-open p-3 bg-black rounded shadow-sm">
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        class="burger-menu-search-bar w-100"
        placeholder="Search modules..."
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
        :class="{ 'input-focused': isSearchFocused }"
        ref="searchInput"
      />
      <font-awesome-icon
        :icon="['fas', 'magnifying-glass']"
        class="magnifying-glass"
        :class="{ 'text-white': isSearchFocused }"
        @click="focusInput"
        style="cursor: pointer"
      />
      <img
        src="../components/icons/Menu gray.png"
        style="cursor: pointer"
        class="ms-3"
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
            { 'inactive': !isModuleActive(module) }, 
            { 'cursor-pointer': isModuleActive(module) }
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

    <div class="mode-toggle d-flex flex-column align-items-center modes_container">
      <div class="d-flex align-items-center gap-2">
        <h6 class="m-0 text-center">
          Which mode do you want to use?
          <font-awesome-icon
            :icon="['fas', 'circle-info']"
            class="circle-info"
            @click="toggleInfo"
          />
        </h6>
      </div>
      <div v-if="showInfo" class="small mt-1 text-warning text-center">
        Testing mode: A quiz feature that evaluates student's knowledge, tracks
        their performance, and offers personalized feedback based on their
        answers.
      </div>

      <div class="toggle-btn-container mt-2">
        <!-- Toggle Button Group -->
        <v-btn-toggle
          v-model="selectedMode"
          rounded="x2"
          color="#414141"
          base-color="#2a2a2a"
        >
          <v-btn value="general">General mode</v-btn>
          <v-btn value="testing">Testing mode</v-btn>
        </v-btn-toggle>
      </div>
    </div>
  </div>
</template>




<script setup lang="ts">
import { ref, computed } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { VBtn, VBtnToggle } from "vuetify/components"; // Import Vuetify components

library.add(faMagnifyingGlass, faCircleInfo);

// Props for burger menu visibility (received from the parent)
const props = defineProps({
  isOpenBurgerMenu: Boolean,
});

const selectedMode = ref("general");
const showInfo = ref(false);
const infoTitel = ref("Testing Mode Explanation:");
const infoMessage = ref(
  "In 'Test Mode,' activate it by typing 'Test [Topic]' (e.g., 'Test Variables'). The assistant will ask questions to help you identify areas of difficulty and guide you with hints or explanations."
);

const toggleInfo = () => {
  showInfo.value = !showInfo.value;
};

const emit = defineEmits(["closeBurgerMenu", "moduleSelected"]);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const modules = ref([
  "Grundlagen der Programmierung",
  "Statistik",
  "Unternehmenssoftware",
  "Datenbanktechnologien",
  "Webentwicklung",
  "Betriebssysteme",
  "asometing ool",
  "bsdsasad",
  "cbisdsa",
  "boob",
  "eerrrr",
  "ffammm",
  "google",
  "habibi",
  "islam",
  "justin bieber",
  "kill me",
]);

const activeModules = ref([
  "Grundlagen der Programmierung",
  "Webentwicklung", 
]);

// Sorting the modules to prioritize active ones, then sorting alphabetically
const filteredModules = computed(() => {
  // Filter the modules based on search query
  const filtered = modules.value.filter((module) =>
    module.toLowerCase().includes(searchQuery.value.toLowerCase())
  );

  // Split into active and inactive modules
  const active = filtered.filter((module) => activeModules.value.includes(module));
  const inactive = filtered.filter((module) => !activeModules.value.includes(module));

  // Sort inactive modules alphabetically
  inactive.sort();

  // Combine active modules (in original order) and sorted inactive modules
  return [...active, ...inactive];
});

function isModuleActive(module: string): boolean {
  return activeModules.value.includes(module);
}

function selectModule(module: string) {
  // Append (Test) if the selected mode is 'testing'
  const moduleNameWithMode = selectedMode.value === 'testing' ? `${module} (Test)` : module;
  emit("moduleSelected", moduleNameWithMode); // Emit the selected module with mode
  closeBurgerMenu(); // Close the menu after selecting the module
}

function closeBurgerMenu() {
  emit("closeBurgerMenu");
}

function focusInput() {
  if (searchInput.value) {
    searchInput.value.focus();
  }
}

// Display module names based on the selected mode
function displayModuleName(module: string): string {
  return module; // Return only the module name
}

</script>



<style scoped>
.burger-menu-open {
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  width: 80vw;
  z-index: 9999;
}

.module-list-container {
  max-height: 82vh;  /* Set the max height to control the scroll area */
  overflow-y: auto;   /* Enable vertical scrolling */
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
  padding: 1rem;
}

.toggle-btn-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: relative;
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
  opacity: 0.5 !important;  /* Reduce opacity */
  cursor: standard !important;  /* Make the cursor a "not-allowed" symbol */
  pointer-events: none !important;  /* Make it unclickable */
}

.list-item-hover:hover {
  background-color: #414141 !important;  /* Keep hover effect for active items only */
}

ul.p-0 {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

/* Optional: Styling for the inactive items on hover (optional as they are unclickable) */
.inactive:hover {
  background-color: transparent !important; /* No hover effect */
}

/* Style for active modules that are clickable */
.cursor-pointer {
  cursor: pointer !important;  /* Apply cursor pointer only for active modules */
}

.modes_container{
  background-color: #000000;
}

::v-deep(.test-mode-text) {
  position: relative;
  top: -5px; /* Adjust to position it higher */
  font-size: 0.8rem; /* Smaller font */
}

.test-mode-text {
  transform: translate(28px, -5px); /* Adjust alignment relative to the module name */
  font-size: 0.7rem; /* Make it smaller */
}
</style>