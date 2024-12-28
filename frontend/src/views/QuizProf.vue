<template>
  <div class="d-flex vh-100">
    <div class="sidebar py-3 px-3">
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
      <div class="file-list-container">
        <ul class="p-0 mt-1">
          <li
            v-for="(fileTitle, index) in filteredFileTitles"
            :key="index"
            :class="[
              'list-item-hover',
              'rounded',
              'text-white',
              'py-1',
              'cursor-pointer',
              { 'selected-file': fileTitle === selectedFile.title },
            ]"
            @click="selectFile(fileTitle)"
          >
            <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
              <span class="file-name position-relative">
                {{ fileTitle }}
              </span>
            </p>
          </li>
        </ul>
      </div>
    </div>
    <div class="right-side w-100 p-4 d-flex flex-column align-items-center">
      <h3 class="text-white text-center">{{ selectedFile.title }}</h3>
      <div class="d-flex flex-column w-100 h-100 align-items-center">
        <textarea
          v-model="selectedFile.content"
          rows="10"
          class="w-100 flex-grow-1 p-3 rounded file-textarea"
          readonly
        ></textarea>
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
import { fetchQuizFiles, fetchQuizFile } from "../services/filesService";

library.add(faMagnifyingGlass, faCircleInfo);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);
const fileTitles = ref<string[]>([]);
const selectedFile = ref<{ title: string; content: string }>({
  title: "",
  content: "",
});

const filteredFileTitles = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return fileTitles.value.filter((title) =>
    title.toLowerCase().includes(query)
  );
});

async function selectFile(fileTitle: string) {
  try {
    const response = await fetchQuizFile(fileTitle);
    selectedFile.value = {
      title: response.data.title,
      content: response.data.content,
    };
  } catch (error) {
    console.error("Error fetching file:", error);
  }
  console.log("Selected file:", fileTitle);
}

function focusInput() {
  searchInput.value?.focus();
}

onMounted(async () => {
  try {
    const response = await fetchQuizFiles();
    fileTitles.value = response.data.sort();
    selectFile(fileTitles.value[0]);
    console.log("Files fetched:", fileTitles.value);
  } catch (error) {
    console.error("Error fetching files:", error);
  }
});
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

.file-list-container {
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

.selected-file {
  background-color: var(--color-gray-medium);
  position: relative;
  overflow: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.selected-file::before {
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

.file-textarea {
  background-color: var(--color-gray-dark);
  max-width: 800px;

  border: none;
  outline: none;
  resize: none;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
