<template>
  <div class="d-flex">
    <div class="sidebar py-3 px-3 vh-100">
      <div class="search-container">
        <input
          ref="searchInput"
          type="text"
          v-model="searchQuery"
          class="sidebar-search-bar w-100"
          placeholder="Search files..."
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

      <!-- Scrollable Course List -->
      <div class="course-list-container">
        <ul class="p-0 mt-1">
          <li
            v-for="(course, index) in filteredFiles"
            :key="index"
            :class="[
              'list-item-hover',
              'rounded',
              'text-white',
              'py-1',
              'cursor-pointer',
              'selected-course',
            ]"
          >
            <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
              <span class="course-name position-relative">
                {{ course }}
              </span>
            </p>
          </li>
        </ul>
      </div>
    </div>
    <div class="right-side w-100 p-4">
      <h3 class="text-center text-white">File1</h3>
      <div class="d-flex">
        <!-- <input type="file" @change="handleFileSelect" class="bg-white border" /> -->
        <textarea v-model="fileContent" rows="10" class="bg-white w-100 "></textarea>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faMagnifyingGlass,
  faCircleInfo,
} from "@fortawesome/free-solid-svg-icons";

library.add(faMagnifyingGlass, faCircleInfo);

const fileContent = ref("");

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];

  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      fileContent.value = (e.target?.result as string) || "";
    };
    reader.readAsText(file);
  }
};

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const files = [
  "file1",
  "file2",
  "file3",
  "file4",
  "file5",
  "file6",
  "file7",
  "file8",
  "file9",
  "file10",
];

const filteredFiles = computed(() => {
  const query = searchQuery.value.toLowerCase();
  const filtered = files.filter((course) =>
    course.toLowerCase().includes(query)
  );
  return filtered;
});

function focusInput() {
  searchInput.value?.focus();
}
</script>

<style scoped>
.sidebar {
  background-color: var(--color-black);
  height: 100vh;
  overflow-y: auto;
  min-width: 305px;
  max-width: 305px;
  position: relative;
  z-index: 1000;
  padding-right: 10px !important;
}

.sidebar-search-bar {
  background-color: var(--color-gray-medium);
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
  /* background-color: var(--color-black); */
  padding-bottom: 0.75em;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  color: var(--color-gray-shadow);
  transition: color 0.2s ease;
}

.course-list-container {
  max-height: 82vh;
  overflow-y: auto;
  scrollbar-width: none;
}

.list-item-hover {
  position: relative;
  padding-left: 0.2em;
  list-style-type: none;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.list-item-hover:hover {
  background-color: var(--color-gray-light);
}

.list-item-hover::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(to bottom, white, var(--color-gray-shadow));
  opacity: 0;
  transition: width 0.5s ease, opacity 0.5s ease;
}

.unclickable {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.cursor-pointer {
  cursor: pointer !important;
}

.modes_container {
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
  transform: translate(30px, -5px);
  font-size: 0.7rem;
}

.circle-info {
  cursor: pointer;
}

.selected-course {
  background-color: var(--color-gray-medium);
  position: relative;
  overflow: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.selected-course::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background: linear-gradient(to bottom, white, var(--color-gray-shadow));
  opacity: 1;
}

.icon-click-effect {
  cursor: pointer;
  display: inline-block;
  transition: transform 0.2s ease;
}

.icon-click-effect:active {
  transform: scale(0.9);
}
</style>
