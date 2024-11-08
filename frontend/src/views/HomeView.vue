<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
      <div
        class="container-fluid d-flex justify-content-between align-items-center"
      >
        <!-- Burger icon -->
        <img
          src="../components/icons/Menu.png"
          style="cursor: pointer"
          @click="toggleBurgerMenu"
        />

        <div class="calendar-days-background">
          <font-awesome-icon
            :icon="['fas', 'calendar-days']"
            class="calendar-days"
          />
        </div>

        <font-awesome-icon
          :icon="['fas', 'pen-to-square']"
          :class="{ 'pen-to-square': true, 'blur-effect': isOpenBurgerMenu }"
          style="color: #5b5b5b; cursor: pointer"
          @click="reloadPage"
        />
      </div>
    </nav>

    <div class="container my-4 logo-container">
      <img class="" src="../components/icons/dontSueChatGPT.png" />
    </div>

    <!-- Sticky input bar at the bottom -->
    <div class="sticky-footer navbar navbar-expand-lg navbar-light">
      <div
        class="container-fluid d-flex justify-content-center align-items-start gap-2"
      >
        <font-awesome-icon
          :icon="['fas', 'plus']"
          class="cursor-pointer btn-circle align-bottom"
          style="background-color: #5b5b5b"
        />

        <textarea
          :class="{ 'custom-input': true, 'blur-effect': isOpenBurgerMenu }"
          placeholder="Type a message..."
          aria-label="Message input"
          v-model="message"
          @input="resizeTextarea"
        ></textarea>

        <div class="input-actions align-bottom">
          <font-awesome-icon
            v-if="message"
            :icon="['fas', 'arrow-up']"
            class="cursor-pointer btn-circle bg-light align-bottom"
          />
          <font-awesome-icon
            v-else
            :icon="['fas', 'volume-high']"
            :class="{
              'cursor-pointer btn-circle bg-light align-bottom': true,
              'blur-effect': isOpenBurgerMenu,
            }"
          />
          <font-awesome-icon
            v-if="lineCount >= 3"
            :icon="['fas', 'up-right-and-down-left-from-center']"
            class="align-bottom custom-expand-btn"
            @click="toggleOverlay"
          />
        </div>
      </div>
    </div>
  </div>
  <!-- Full-screen overlay -->
  <div v-if="isOverlayVisible" class="full-screen-overlay">
    <div class="height-100 p-2" style="background-color: #232323">
      <div class="container h-100 d-flex flex-column">
        <div class="d-flex justify-content-end mt-2 mb-3">
          <font-awesome-icon
            :icon="['fas', 'down-left-and-up-right-to-center']"
            @click.stop="toggleOverlay"
            class="collapse-icon"
          />
        </div>

        <textarea
          class="full-screen-textarea"
          style="background-color: #232323"
          placeholder="Type a message..."
          aria-label="Message input"
          v-model="message"
        ></textarea>
      </div>
    </div>
  </div>
  <div
    v-if="isOpenBurgerMenu"
    class="burger-menu-open p-3 bg-black rounded shadow-sm">
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        class="burger-menu-search-bar w-100"
        placeholder="Search modules..."
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
      />
      <font-awesome-icon
        :icon="['fas', 'magnifying-glass']"
        class="magnifying-glass"
        style="color: #5b5b5b"
        :class="{ 'text-white': isSearchFocused }"
      />
      <img
        src="../components/icons/Menu gray.png"
        style="cursor: pointer"
        class="ms-3"
        @click="toggleBurgerMenu"
      />
    </div>
    <ul class="p-0 mt-3">
      <li
        v-for="(module, index) in filteredModules"
        :key="index"
        class="list-item-hover rounded text-white py-1"
      >
        <p class="m-0 py-2 px-2">{{ module }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBars,
  faPlus,
  faArrowUp,
  faLeaf,
  faVolumeHigh,
  faPenToSquare,
  faArrowRightLong,
  faCalendarDays,
  faUpRightAndDownLeftFromCenter,
  faDownLeftAndUpRightToCenter,
  faMagnifyingGlass,
} from "@fortawesome/free-solid-svg-icons";

// Add icons to the library
library.add(
  faBars,
  faPlus,
  faArrowUp,
  faLeaf,
  faVolumeHigh,
  faPenToSquare,
  faArrowRightLong,
  faCalendarDays,
  faUpRightAndDownLeftFromCenter,
  faDownLeftAndUpRightToCenter,
  faMagnifyingGlass
);
// Reactive state for message input
const message = ref("");

const isOverlayVisible = ref(false);
const isOpenBurgerMenu = ref(false);
const isSearchFocused = ref(false);

const searchQuery = ref("");

// List of modules
const modules = ref([
  "Grundlagen der Programmierung",
  "Statistik",
  "Unternehmenssoftware",
  "Datenbanktechnologien",
  "Webentwicklung",
  "Betriebssysteme",
]);

// Computed property to filter modules based on search query
const filteredModules = computed(() => {
  return modules.value.filter((module) =>
    module.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const toggleOverlay = () => {
  isOverlayVisible.value = !isOverlayVisible.value;
};

const toggleBurgerMenu = () => {
  isOpenBurgerMenu.value = !isOpenBurgerMenu.value;
};

const lineCount = computed(() => {
  return message.value.split("\n").length;
});

const resizeTextarea = (event: any) => {
  const target = event.target;
  target.style.height = "45px";
  target.style.height = `${Math.min(target.scrollHeight, 200)}px`;
};

const reloadPage = () => {
  location.reload();
};
</script>

<style scoped>
.custom-input::placeholder {
  color: white;
  padding: 0px;
  margin: 0px;
}

.custom-input:focus {
  outline: none;
}

.btn-input-group {
  font-size: 2rem;
}

.btn-circle {
  border-radius: 50%;
  width: 25px;
  height: 25px;
  max-width: 25px;
  max-height: 25px;
  min-width: 25px;
  min-height: 25px;
  padding: 0.5em;
}

.btn-circle font-awesome-icon {
  font-size: 1rem;
}

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

.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 1rem;
  z-index: 1000;
}

.sticky-footer .input-container {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.pen-to-square {
  font-size: 1.8rem;
}

.calendar-days {
  font-size: 1.8rem;
  color: #717171;
}

.calendar-days-background {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 5.5em;
  height: 2.6em;
  background: linear-gradient(90deg, white, #5b5b5b);
  border-radius: 20px;
  cursor: pointer;
}

.align-bottom {
  align-self: flex-end;
}

.custom-input {
  flex: 1;
  background-color: #232323;
  border: none;
  color: white;
  border-radius: 25px;
  height: 45px;
  max-height: 200px;
  resize: none;
  padding-top: 8px;
  padding-left: 15px;
}

.input-actions {
  position: relative;
}

.collapse-icon {
  align-self: flex-end;
  font-size: 1.5rem;
  color: white;
  cursor: pointer;
  z-index: 10000;
}

.custom-expand-btn {
  font-size: 0.9rem;
  color: white;
  position: absolute;
  right: 14px;
  top: -27px;
  cursor: pointer;
}

.full-screen-textarea {
  all: unset;
  background-color: #232323;
  color: white;
  font-family: inherit;
  font-size: 16px;
  width: 100%;
  height: 100%;
  padding: 10px;
  resize: none;
  outline: none;
  border: none;
  box-sizing: border-box;
  overflow-y: auto;
  line-height: 1.5;
}

.full-screen-textarea::placeholder {
  color: #bbb;
  opacity: 1;
}

.height-100 {
  height: 100%;
}

.full-screen-overlay {
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9999;
}

.burger-menu-open {
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  width: 80vw;
  z-index: 9999;
}

.burger-menu-search-bar {
  background-color: #232323;
  border: none;
  color: white;
  border-radius: 25px;
  height: 45px;
  max-height: 200px;
  padding-left: 40px;
}

.burger-menu-search-bar::placeholder {
  padding: 0px;
  margin: 0px;
}

.burger-menu-search-bar:focus::placeholder {
  color: white;
}

.burger-menu-search-bar:focus {
  outline: none;
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
}

.magnifying-glass {
  position: absolute;
  left: 15px;
  top: 15px;
}

.list-item-hover {
  list-style-type: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.list-item-hover:hover {
  background-color: #444;
  cursor: pointer;
}

::-webkit-scrollbar {
  width: 10px;
}

ul.p-0 {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

.blur-effect {
  filter: blur(1.5px);
}
</style>
