<template>
  <div
    class="d-flex flex-column vh-100"
    style="background-color: var(--color-black)"
  >
    <!-- Navbar -->
    <div class="container-fluid navbar-container">
      <nav class="py-2 px-3 d-flex align-items-center justify-content-between">
        <!-- Home Icon -->
        <button
          class="btn btn-link p-0 d-flex align-items-center"
          @click="handleHomeClick"
          aria-label="Home"
        >
          <font-awesome-icon
            class="icon-click-effect"
            :icon="['fas', 'home']"
            style="color: var(--color-gray-shadow); width: 29px; height: 29px"
          />
        </button>
        <div class="nav-icon-holder">
          <!-- if user doesnt have pfp -->
          <!-- <font-awesome-icon
            class="arrows-rotate icon-click-effect cursor-pointer"
            v-if="isWideScreen && isSidebarOpen"
            :icon="['fas', 'user-circle']"
            style="color: var(--color-gray-shadow);"
          /> -->
          <div
            class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle icon-click-effect pfp-container"
          >
            <img
              alt="User"
              src="https://s.gravatar.com/avatar/6276a6c42e2f0f22bb0a96c4b1f2bd32?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fsh.png"
              class="img-fluid rounded-circle"
              @click="toggleProfileMenu"
            />
          </div>
        </div>
        <Profilemenu
          v-if="isProfileMenuVisible"
          :origin="'Nav-EditQuiz'"
          @toggleProfileMenu="toggleProfileMenu"
        />
      </nav>
    </div>

    <!-- Content Container -->
    <div class="d-flex flex-grow-1">
      <!-- Sidebar -->
      <div v-if="isSidebarOpen" class="sidebar py-3 px-3">
        <div class="search-container">
          <input
            ref="searchInput"
            type="text"
            v-model="searchQuery"
            class="sidebar-search-bar w-100"
            placeholder="Search courses..."
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
        </div>
        <div class="file-list-container">
          <ul class="p-0 mt-1">
            <li
              v-for="(course, index) in filteredCourses"
              :key="index"
              class="list-item-hover rounded text-white py-1 cursor-pointer"
              :class="{ 'selected-course': course === courseSelected }"
              @click="selectCourse(course)"
            >
              <p class="m-0 py-2 px-2 d-flex align-items-start">
                <span class="file-name">{{ course }}</span>
              </p>
            </li>
          </ul>
        </div>
      </div>

      <!-- Right Content -->
      <div
        class="right-side w-100 d-flex flex-column align-items-center rounded pt-3 px-3"
      >
        <div
          v-for="(file, index) in files"
          :key="file.title"
          :class="[
            'd-flex flex-column w-100 align-items-center mt-3',
            index !== files.length - 1 ? 'file-container' : '',
          ]"
        >
          <div
            :key="file.title"
            class="textarea-container position-relative w-100 flex-grow-1 mb-4"
          >
            <h3 class="text-white text-center mb-3 flex-grow-1">
              {{ file.title }}
            </h3>

            <textarea
              v-model="file.content"
              class="w-100 p-3 rounded file-textarea"
              :ref="(el) => setTextareaRef(el, index)"
              :readonly="!file.isEditMode"
              @input="adjustHeight"
            ></textarea>

            <button
              class="btn btn-edit bg-white position-absolute bottom-0 end-0 mx-3 my-3 icon-click-effect"
              @click="toggleEdit(index)"
            >
              <span v-if="file.isEditMode"> Save </span>
              <span v-else>
                Edit
                <font-awesome-icon
                  :icon="['fas', 'pen-to-square']"
                  class="cursor-pointer"
                  style="color: var(--color-gray-shadow)"
                />
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faMagnifyingGlass,
  faCircleInfo,
  faHome,
  faPenToSquare,
} from "@fortawesome/free-solid-svg-icons";
import {
  fetchQuizFiles,
  fetchQuizFile,
  postQuizFile,
} from "../services/filesService";
// import { courses, fetchCourses } from "../services/courseService";
import Profilemenu from "../widgets/Profilemenu.vue";
import { useScreenWidth } from "../utils/useScreenWidth";
import { useRouter } from "vue-router";

library.add(faMagnifyingGlass, faCircleInfo, faHome, faPenToSquare);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);
const files = ref<{ title: string; content: string; isEditMode: boolean }>({
  title: "",
  content: "",
  isEditMode: false,
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
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const router = useRouter();
const handleHomeClick = () => {
  router.push("/");
};

const toggleEdit = (index) => {
  const file = files.value[index];
  const textarea = textareaRefs.value[index];

  file.isEditMode = !file.isEditMode;

  if (file.isEditMode) {
    textarea.focus();
  } else {
    postQuizFile(file.title, file.content);
    adjustHeight();
  }
};

const courses = ref<string[]>([
  // "Grundlagen der Programmierung",
  // "Statistik",
  // "Datenbanken",
  // "Web-Entwicklung",
  // "Künstliche Intelligenz",
  // "Betriebssysteme",
  // "Netzwerke",
  // "IT-Sicherheit",
  // "Projektmanagement",
  // "Soft Skills",
]);
const courseSelected = ref<string | null>(null);

const filteredCourses = computed(() => {
  const query = searchQuery.value.toLowerCase();
  const filtered = courses.value.filter((course) =>
    course.toLowerCase().includes(query)
  );
  return filtered;
});

function selectCourse(course: string) {
  courseSelected.value = course;
}

function focusInput() {
  searchInput.value?.focus();
}

onMounted(async () => {
  const storedCourses = localStorage.getItem("courses");
  courses.value = storedCourses ? JSON.parse(storedCourses) : [];
  try {
    const response = await fetchQuizFiles();
    files.value = response.data.sort((a: any, b: any) => a.title.localeCompare(b.title));
    console.log("Files fetched:", files.value);
  } catch (error) {
    console.error("Error fetching files:", error);
  } finally {
    setTimeout(() => {
      adjustHeight();
    }, 0);
  }
});

const textareaRefs = ref([]);

const setTextareaRef = (el, index) => {
  if (el) {
    textareaRefs.value[index] = el;
  }
};

const adjustHeight = () => {
  textareaRefs.value.forEach((textarea) => {
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = `${textarea.scrollHeight}px`;
      if (parseInt(textarea.style.height) < 150) {
        textarea.style.height = "150px";
      }
    }
  });
};
</script>

<style scoped>
.navbar-container {
  background-color: var(--color-black);
}

.sidebar {
  background-color: var(--color-black);
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

.right-side {
  background-color: var(--color-background-dark);
  border: 1px solid var(--color-gray-shadow);
  margin: 5px;
  overflow-y: auto;
  max-height: calc(100vh - 60px);
}

.unclickable {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
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
  display: inline-block;
  transition: transform 0.2s ease;
}

.icon-click-effect:active {
  transform: scale(0.9);
}

.file-container2 {
  border-bottom: 1px solid var(--color-gray-shadow);
  max-width: 800px;
  margin-bottom: 2em;
  padding-bottom: 2em ;
}

.textarea-container {
  max-width: 800px;
}

.file-textarea {
  background-color: var(--color-gray-dark);
  max-width: 1000px;
  max-height: 80vh;
  border: none;
  outline: none;
  resize: none;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.nav-icon-holder {
  width: 29px;
}

.btn-edit:hover {
  opacity: 0.2;
}

.pfp-container {
  width: 32px;
  height: 32px;
}
</style>
