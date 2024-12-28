<template>
  <div class="d-flex vh-100">
    <div v-if="isSidebarOpen" class="sidebar py-3 px-3">
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
          class="magnifying-glass cursor-pointer"
          :class="{ 'text-white': isSearchFocused }"
          @click="focusInput"
        />
        <img
          src="../assets/icons/MenuClose.png"
          class="ms-3 icon-click-effect cursor-pointer"
          @click="toggleSidebar"
        />
      </div>

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

    <div class="right-side w-100 p-4 pb-5 d-flex flex-column align-items-center">
      <nav class=" d-flex justify-content-between w-100 mb-3">
        <!-- phone -->
        <img
          v-if="!isWideScreen"
          class="icon-click-effect cursor-pointer"
          src="../assets/icons/MenuOpen.png"
          @click="toggleBurgerMenu"
        />
        <!-- pc and sidebar closed -->
        <img
          v-else-if="isWideScreen && !isSidebarOpen"
          class="icon-click-effect cursor-pointer"
          src="../assets/icons/MenuOpen.png"
          
          @click="toggleSidebar"
        />
        <!-- pc and sidebar open -->
        <div v-else class="icon-holder">
          <font-awesome-icon
            class="icon-click-effect cursor-pointer"
            :icon="['fas', 'home']"
            style="
              color: var(--color-gray-shadow);
              width: 29px;
              height: 29px;
            "
            @click="handleHomeClick"
          />
        </div>
        <h3 class="text-white text-center m-0">{{ selectedFile.title }}</h3>

        <div class="icon-holder">
          <!-- if user doesnt have pfp -->
          <!-- <font-awesome-icon
            class="arrows-rotate icon-click-effect cursor-pointer"
            v-if="isWideScreen && isSidebarOpen"
            :icon="['fas', 'user-circle']"
            style="color: var(--color-gray-shadow);"
          /> -->
          <div
            class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle icon-click-effect"
            style="width: 32px; height: 32px"
          >
            <img
              alt="User"
              src="https://s.gravatar.com/avatar/6276a6c42e2f0f22bb0a96c4b1f2bd32?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fsh.png"
              class="img-fluid rounded-circle"
              style="width: 100%; height: 100%"
              @click="toggleProfileMenu"
            />
          </div>
        </div>
        <Profilemenu
          v-if="isProfileMenuVisible"
          :origin="'Nav'"
          @toggleProfileMenu="toggleProfileMenu"
        />
      </nav>
      <div v-if="fileTitles.length" class="d-flex flex-column w-100 h-100 align-items-center">
        <div class="textarea-container position-relative w-100 flex-grow-1">
          <textarea
            v-model="selectedFile.content"
            rows="10"
            class="w-100 h-100 p-3 rounded file-textarea"
            readonly
          ></textarea>
          <button
            class="btn btn-edit bg-white position-absolute bottom-0 end-0 mx-3 my-3 icon-click-effect"
            style="z-index: 1"
            @click="toggleEdit"
          >
            <span v-if="isEditMode"> Save </span>
            <span v-else>
              Edit
              <font-awesome-icon
                :icon="['fas', 'pen-to-square']"
                class="cursor-pointer"
                style="color: var(--color-gray-shadow);"
              />
            </span>
          </button>
        </div>
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
  faHome,
  faPenToSquare,
} from "@fortawesome/free-solid-svg-icons";
import { fetchQuizFiles, fetchQuizFile, postQuizFile } from "../services/filesService";
import Profilemenu from "../widgets/Profilemenu.vue";
import { useScreenWidth } from "../utils/useScreenWidth";
import { useRouter } from "vue-router";

library.add(faMagnifyingGlass, faCircleInfo, faHome, faPenToSquare);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);
const fileTitles = ref<string[]>([]);
const selectedFile = ref<{ title: string; content: string }>({
  title: "",
  content: "",
});
const { isWideScreen } = useScreenWidth();

const isSidebarOpen = ref(true);
const isBurgerMenuOpen = ref(false);
const isProfileMenuVisible = ref(false);
const isEditMode = ref(false);

const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
};

const toggleBurgerMenu = () => {
  isBurgerMenuOpen.value = !isBurgerMenuOpen.value;
  console.log("Burger menu open:", isBurgerMenuOpen.value);
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
  console.log("sidebar menu open:", isSidebarOpen.value);
};

const router = useRouter();
const handleHomeClick = () => {
  router.push("/");
};

const toggleEdit = () => {
  isEditMode.value = !isEditMode.value;
  const textarea = document.querySelector(".file-textarea") as HTMLTextAreaElement;
  if (isEditMode.value) {
    textarea.readOnly = false;
    textarea.focus();
  } else {
    textarea.readOnly = true;
    postQuizFile(selectedFile.value.title, selectedFile.value.content);
  }
};

const filteredFileTitles = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return fileTitles.value.filter((title) => title.toLowerCase().includes(query));
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
  display: inline-block;
  transition: transform 0.2s ease;
}

.icon-click-effect:active {
  transform: scale(0.9);
}

.textarea-container {
  max-width: 800px;
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

.icon-holder {
  width: 29px;
}

.btn-edit:hover {
  opacity: 0.2;
}
</style>
