<template>
  <div
    ref="burgerMenuRef"
    class="burger-menu-open p-3 bg-black rounded shadow-sm"
  >
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
      <!-- Add event to close the burger menu -->
      <img
        src="../components/icons/Menu gray.png"
        style="cursor: pointer"
        class="ms-3"
        @click="closeBurgerMenu"
      />
    </div>
    <ul class="p-0 mt-3" style="cursor: pointer">
      <li
        v-for="(module, index) in filteredModules"
        :key="index"
        class="list-item-hover rounded text-white py-1"
        @click="selectModule(module)"
      >
        <p class="m-0 py-2 px-2">{{ module }}</p>
      </li>
    </ul>
    <div class="mode-toggle d-flex flex-column align-items-center">
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
        Test mode: A quiz feature that evaluates students' knowledge, tracks
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

// Import necessary Vuetify components
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
("general");

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
]);

const filteredModules = computed(() =>
  modules.value.filter((module) =>
    module.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

function selectModule(module: string) {
  emit("moduleSelected", module); // Emit the selected module to the parent
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
}
</style>
