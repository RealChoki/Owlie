<template>
  <div class="sidebar py-3 px-3 vh-100">
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
        class="magnifying-glass"
        :class="{ 'text-white': isSearchFocused }"
        style="cursor: pointer"
        @click="focusInput"
      />
      <img
        src="../assets/icons/MenuClose.png"
        class="ms-3 icon-click-effect"
        style="cursor: pointer"
        @click="closeSidebar"
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
            { 'unclickable': !isCourseClickable(course), 'cursor-pointer': isCourseClickable(course), 'selected-course': isCourseClicked(course) },
          ]"
          @click="isCourseClickable(course) ? selectCourse(course) : null; handleCourseClick(course)"
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
      <div class="d-flex gap-2 text-white">
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
          base-color="var(--color-gray-medium)"
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
  isOpenSidebar: Boolean,
});

const emit = defineEmits(["closeSidebar"]);

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);

const selectedMode = ref(getAssistantMode() || 'general');
const courseClicked = ref<{ course: string; mode: string } | null>(null);
const showInfo = ref(false);


const clickableCourses = ref<string[]>(["Grundlagen der Programmierung",  "Statistik"]);

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
  if (!isCourseClickable(course)) {
    return;
  }
  console.log("Selected course:", course);
  courseClicked.value = { course, mode: selectedMode.value };

  const modeName = selectedMode.value;
  const courseName = course;

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
  const currentCourse = getAssistantCourse();
  const currentMode = getAssistantMode();
  if (currentCourse && currentMode) {
    courseClicked.value = { course: currentCourse, mode: currentMode };
    selectedMode.value = currentMode;
  }
});
</script>

<style scoped>
.sidebar {
  background-color: var(--color-black);
  height: 100vh;
  overflow-y: auto;
  min-width: 305px;
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
  content: '';
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
  transform: translate(
    30px,
    -5px
  );
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
  content: '';
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
