<template>
  <div class="burger-menu-open py-3 px-3 bg-black rounded shadow-sm">
    <div class="search-container">
      <input
        ref="searchInput"
        type="text"
        v-model="searchQuery"
        class="burger-menu-search-bar w-100"
        placeholder="Search courses..."
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
        class="ms-3 icon-click-effect"
        style="cursor: pointer"
        @click="closeBurgerMenu"
      />
    </div>

    <!-- Scrollable Course List -->
    <div class="course-list-container">
      <ul class="p-0 mt-1">
        <li
          v-for="(course, index) in filteredCourses"
          :key="index"
          :class="[
            'list-item-hover',
            'rounded',
            'text-white',
            'py-1',
            {
              unclickable: !isCourseClickable(course),
              'cursor-pointer': isCourseClickable(course),
              'clickable-course': isCourseClicked(course),
            },
          ]"
          @click="
            isCourseClickable(course) ? selectCourse(course) : null;
            handleCourseClick(course);
          "
        >
          <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
            <span class="course-name position-relative">
              {{ course }}
              <span
                v-if="selectedMode === 'quiz'"
                class="test-mode-text text-secondary small position-absolute top-0 end-0"
              >
                (Quiz)
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
        <h6 class="m-0">Switch mode to:</h6>
      </div>
      <div v-if="showInfo" class="small mt-1 text-warning text-center">
        Quiz mode: A quiz feature that assesses knowledge, tracks performance,
        and provides personalized feedback.
      </div>

      <div
        class="toggle-btn-container d-flex justify-content-center mt-2 w-100 position-relative"
      >
        <v-btn
          @click="toggleMode"
          class="equal-width-btn equal-width-toggle"
          color="#414141"
          :style="{ backgroundColor: '#2a2a2a' }"
        >
          {{ selectedMode === "general" ? "Quiz" : "General" }}
        </v-btn>
        <font-awesome-icon
          :icon="['fas', 'circle-info']"
          class="circle-info"
          @click="toggleInfo"
        />
      </div>

      <button
        class="equal-width-toggle mt-2 d-flex align-items-center w-100 p-2 text-dark border-0 profile-btn"
        type="button"
        aria-haspopup="menu"
        :aria-expanded="isPopoverVisible"
        @click="togglePopover"
      >
        <div class="me-2">
          <div
            class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle"
            style="width: 32px; height: 32px"
          >
            <img
              alt="User"
              src="https://s.gravatar.com/avatar/6276a6c42e2f0f22bb0a96c4b1f2bd32?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fsh.png"
              class="img-fluid rounded-circle"
              style="width: 100%; height: 100%"
            />
          </div>
        </div>
        <div class="text-start text-truncate text-white">
          <span>David Svoboda</span>
        </div>
      </button>

      <!-- popover -->
      <div v-if="isPopoverVisible" class="popover position-absolute z-50">
        <nav
          class="rounded shadow-sm p-2 text-white"
          style="background-color: #2a2a2a"
        >
          <div class="ms-2 my-2">Hochschule für Technisch und Wirtschaft</div>
          <hr />
          <a
            href="#"
            class="d-flex align-items-center gap-2 text-decoration-none text-white py-2"
          >
            <i class="bi bi-person-circle"></i> My GPTs
          </a>
          <a
            href="#"
            class="d-flex align-items-center gap-2 text-decoration-none text-white py-2"
          >
            <i class="bi bi-pencil-square"></i> Customize ChatGPT
          </a>
          <a
            href="https://help.openai.com/en/collections/3742473-chatgpt"
            target="_blank"
            class="d-flex align-items-center gap-2 text-decoration-none text-white py-2"
          >
            <i class="bi bi-question-circle"></i> Help & FAQ
          </a>
          <a
            href="#"
            class="d-flex align-items-center gap-2 text-decoration-none text-white py-2"
          >
            <i class="bi bi-gear"></i> Settings
          </a>
        </nav>
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
import { fetchAssistantIds, courses } from "../services/courseService";
import {
  getAssistantCourse,
  getAssistantMode,
  setAssistantCourse,
  setAssistantMode,
} from "../services/openaiService";
import { setNavbarCourseTitle } from "../services/homeService";

library.add(faMagnifyingGlass, faCircleInfo);

const props = defineProps({
  isOpenBurgerMenu: Boolean,
});

const emit = defineEmits(["closeBurgerMenu"]);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const selectedMode = ref(getAssistantMode() || "general");
const courseClicked = ref<{ course: string; mode: string } | null>(null);
const showInfo = ref(false);

function toggleMode() {
  selectedMode.value = selectedMode.value === "general" ? "quiz" : "general";
}

const clickableCourses = ref<string[]>([
  "Grundlagen der Programmierung",
  "Investition und Finanzierung",
  "Statistik",
]);

const isPopoverVisible = ref(false);

const togglePopover = () => {
  isPopoverVisible.value = !isPopoverVisible.value;
};

function isCourseClickable(course: string): boolean {
  return clickableCourses.value.includes(course);
}

function handleCourseClick(course: string) {
  if (!isCourseClickable(course)) {
    return;
  }
  console.log("Selected course:", course);
  setNavbarCourseTitle(course, selectedMode.value);
}

function isCourseClicked(course: string): boolean {
  return (
    courseClicked.value !== null &&
    course === courseClicked.value.course &&
    selectedMode.value === courseClicked.value.mode
  );
}

const filteredCourses = computed(() => {
  const query = searchQuery.value.toLowerCase();
  const filtered = courses.value.filter((course) =>
    course.toLowerCase().includes(query)
  );

  const clickable = filtered.filter(isCourseClickable);
  const unclickable = filtered.filter((course) => !isCourseClickable(course));

  return [...clickable, ...unclickable.sort()];
});

const { clearThread, initializeThread } = useThread(ref(undefined), () => {});

async function selectCourse(course: string) {
  setTimeout(() => {
    closeBurgerMenu();
  }, 350);

  if (!isCourseClickable(course)) {
    return;
  }
  console.log("Selected course:", course);
  courseClicked.value = { course, mode: selectedMode.value };

  const modeName = selectedMode.value;
  const courseName = course.replace(/ /g, "_");

  const currentCourse = getAssistantCourse();
  const currentMode = getAssistantMode();

  if (course !== currentCourse || modeName !== currentMode) {
    console.log("Course or mode changed. Resetting thread and messages.");
    clearThread();
    clearMessages(false);

    setAssistantCourse(course);
    setAssistantMode(modeName);
    try {
      await fetchAssistantIds(courseName, modeName);
      await initializeThread();
    } catch (error) {
      console.error("Error initializing thread:", error);
      return;
    }
  } else {
    console.log("Same course and mode selected. No action taken.");
  }
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
  const currentCourse = getAssistantCourse();
  const currentMode = getAssistantMode();
  if (currentCourse && currentMode) {
    courseClicked.value = { course: currentCourse, mode: currentMode };
    selectedMode.value = currentMode;
  }
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
  z-index: 1000;
  min-width: 305px;
  padding-right: 10px !important;
}

.course-list-container {
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
  transition: color 0.2s ease;
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
  background-color: #000000;
  padding-bottom: 0.75em;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  color: #5b5b5b;
  transition: color 0.2s ease;
}

.input-focused::placeholder {
  color: white !important;
}

.list-item-hover {
  position: relative;
  padding-left: 0.2em;
  list-style-type: none;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.list-item-hover:hover {
  background-color: #414141;
}

.list-item-hover::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(to bottom, white, #5b5b5b);
  opacity: 0;
  transition: width 0.5s ease, opacity 0.5s ease;
}

.unclickable {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

ul.p-0 {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

.mode-toggle {
  position: absolute;
  bottom: 0;
  left: 0;
  display: flex;
  justify-content: center;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.equal-width-toggle {
  width: 100%;
  max-width: 450px;
  box-sizing: border-box;
}

.equal-width-btn {
  width: 100%;
  text-align: center;
  min-width: 0;
  padding: 12px 16px;
  height: auto;
  line-height: 1.2;
}

.circle-info {
  cursor: pointer;
  position: absolute;
  right: -3px;
  top: -3px;
}

/* Other styles remain the same */

.unclickable {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.list-item-hover:hover {
  background-color: #414141 !important;
}

.unclickable:hover {
  background-color: transparent !important;
}

.cursor-pointer {
  cursor: pointer !important;
}

.modes_container {
  background-color: #000000;
  overflow: visible;
}

.small {
  max-width: 450px;
}

::v-deep(.test-mode-text) {
  position: relative;
  top: -5px;
  font-size: 0.8rem;
}

.test-mode-text {
  transform: translate(30px, -5px);
  font-size: 0.7rem;
}

.clickable-course {
  background-color: #2a2a2a;
  position: relative;
  overflow: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.clickable-course::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background: linear-gradient(to bottom, white, #5b5b5b);
  opacity: 1;
}

.icon-click-effect {
  cursor: pointer;
  display: inline-block;
  transition: transform 0.2s ease;
}

.icon-click-effect:active {
  transform: scale(0.8);
}

.profile-btn {
  border-radius: 5px;
  background-color: #000000;
  transition: background-color 0.5s ease;
}

.profile-btn:hover {
  background-color: #4141415b;
}

.profile-btn:active {
  background-color: #1a1a1a;
}

.popover {
  width: 100%;
  max-width: 450px;
  top: -145px;
  left: transformX(-50%);
  background-color: transparent;
}
</style>
