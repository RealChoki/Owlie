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
        class="magnifying-glass cursor-pointer"
        :style="{
          color: isSearchFocused ? 'var(--magnifying-glass-icon-active)' : 'var(--magnifying-glass-icon-inactive)'
        }"
        @click="focusInput"
      />
      <svg
        width="30"
        height="30"
        viewBox="0 0 100 100"
        xmlns="http://www.w3.org/2000/svg"
        class="ms-3 icon-click-effect cursor-pointer"
        @click="closeSidebar"
      >
        <rect x="0" y="15" width="33" height="12" rx="4" fill="var(--burger-menu-icon-close)" />
        <rect x="0" y="44" width="66" height="12" rx="4" fill="var(--burger-menu-icon-close)" />
        <rect x="0" y="73" width="100" height="12" rx="4" fill="var(--burger-menu-icon-close)" />
      </svg>
    </div>

    <!-- Scrollable Course List -->
    <div class="course-list-container">
      <ul class="p-0 mt-1">
        <li
          v-for="(course, index) in filteredCourses"
          :key="index"
          class="list-item-hover rounded py-1"
          :class="courseClass(course)"
          @click="onCourseClick(course)"
        >
          <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
            <span class="course-name position-relative">
              {{ course }}
              <span
                v-if="selectedMode !== 'general'"
                class="mode-text text-secondary small position-absolute top-0 end-0"
              >
                ({{ selectedMode.charAt(0).toUpperCase() + selectedMode.slice(1) }})
              </span>
            </span>
          </p>
        </li>
      </ul>
    </div>

    <div class="mode-toggle d-flex flex-column align-items-center modes-container p-3 pt-2">
      <div class="d-flex gap-2" style="color: var(--text-color)">
        <h6 class="m-0">
          Select a mode
          <font-awesome-icon
            :icon="['fas', 'circle-info']"
            class="circle-info cursor-pointer"
            @click="toggleInfo"
            style="color: var(--info-icon-bg)"
          />
        </h6>
      </div>
      <div v-if="showInfo" class="small mt-1 text-warning text-center">
        <div v-if="selectedMode === 'general'">
          An open learning environment for exploring course material, asking questions, and understanding concepts at
          your own pace.
        </div>
        <div v-if="selectedMode === 'quiz'">
          A quiz feature that assesses knowledge, tracks performance, and provides personalized feedback.
        </div>
        <div v-if="selectedMode === 'exam'">
          A mock exam experience using professor-uploaded materials, where realistic exam-style questions are generated
          for focused practice.
        </div>
      </div>

      <div class="toggle-btn-container d-flex justify-content-center mt-2 w-100">
        <v-btn-toggle
          v-model="selectedMode"
          mandatory
          rounded="x2"
          base-color="var(--mode-selector-bg)"
          class="equal-width-toggle"
        >
          <v-btn value="general" class="equal-width-btn">General</v-btn>
          <v-btn
            value="quiz"
            class="equal-width-btn"
            style="border-left: var(--mode-selector-border); border-right: var(--mode-selector-border)"
            >Quiz</v-btn
          >
          <v-btn value="exam" class="equal-width-btn">Exam</v-btn>
        </v-btn-toggle>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { VBtn, VBtnToggle } from 'vuetify/components'
import { useThread } from '../hooks/useThread'
import { clearMessages } from '../services/chatService'
import { fetchAssistantIds, courses } from '../services/courseService'
import { getAssistantCourse, getAssistantMode, setAssistantCourse, setAssistantMode } from '../services/openaiService'
import { setNavbarCourseTitle } from '../services/homeService'
import { stopTTS } from '../services/ttsService'

const props = defineProps({
  isSidebarOpen: Boolean
})

const emit = defineEmits(['closeSidebar'])

// Refs
const searchQuery = ref('')
const isSearchFocused = ref(false)
const searchInput = ref<HTMLInputElement | null>(null)

const selectedMode = ref(getAssistantMode() || 'general')
const courseClicked = ref<{ course: string; mode: string } | null>(null)
const showInfo = ref(false)

const clickableCourses = ref<string[]>(['Grundlagen der Programmierung'])

// Computed
const filteredCourses = computed(() => {
  const query = searchQuery.value.toLowerCase()
  const filtered = courses.value.filter((course) => course.toLowerCase().includes(query))
  const clickable = filtered.filter(isCourseClickable)
  const unclickable = filtered.filter((course) => !isCourseClickable(course))

  return [...clickable, ...unclickable.sort()]
})

// Main methods
function isCourseClickable(course: string): boolean {
  // temp code
  if (course === 'Grundlagen der Programmierung' && selectedMode.value === 'exam') {
    return false // Exclude this course and 'exam' mode
  }
  // end temp code

  return clickableCourses.value.includes(course)
}

const isCourseClicked = (course: string): boolean =>
  courseClicked.value !== null &&
  course === courseClicked.value.course &&
  selectedMode.value === courseClicked.value.mode

// Generate dynamic classes for courses
const courseClass = (course: string) => ({
  unclickable: !isCourseClickable(course),
  'cursor-pointer': isCourseClickable(course),
  'selected-course': isCourseClicked(course)
})

const onCourseClick = (course: string) => {
  if (!isCourseClickable(course)) return
  setNavbarCourseTitle(course, selectedMode.value)
  selectCourse(course)
}

const { clearThread, initializeThread } = useThread(ref(undefined), () => {})

async function selectCourse(course: string) {
  if (!isCourseClickable(course)) return
  console.log('Selected course:', course)
  courseClicked.value = { course, mode: selectedMode.value }

  const modeName = selectedMode.value
  const courseName = course
  const currentMode = getAssistantMode()
  const currentCourse = getAssistantCourse()

  if (course !== currentCourse || modeName !== currentMode) {
    console.log('Course or mode changed. Resetting thread and messages.')
    stopTTS()
    clearThread()
    clearMessages(false)
    setAssistantCourse(course)
    setAssistantMode(modeName)

    try {
      await fetchAssistantIds(courseName, modeName)
      await initializeThread()
    } catch (error) {
      console.error('Error initializing thread:', error)
    }
  } else {
    console.log('Same course and mode selected. No action taken.')
  }
}

// Utility
function closeSidebar() {
  emit('closeSidebar')
}

function focusInput() {
  searchInput.value?.focus()
}

function toggleInfo() {
  showInfo.value = !showInfo.value
}

// Lifecycle
onMounted(() => {
  const currentCourse = getAssistantCourse()
  const currentMode = getAssistantMode()

  if (currentCourse && currentMode) {
    courseClicked.value = { course: currentCourse, mode: currentMode }
    selectedMode.value = currentMode
  }
})
</script>

<style scoped>
.sidebar {
  background-color: var(--sidebar-bg);
  height: 100vh;
  overflow-y: auto;
  min-width: 309px;
  position: relative;
  z-index: 1000;
  padding-right: 10px !important;
}

.sidebar-search-bar {
  background-color: var(--course-search-bg);
  color: var(--text-color);
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
  color: var(--text-color) !important;
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
  padding-bottom: 0.75em;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
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
  color: var(--text-color);
}

.list-item-hover:hover {
  background-color: var(--course-hover-bg);
}

.list-item-hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: var(--course-sidebar-gradient);
  opacity: 0;
  transition: width 0.5s ease, opacity 0.5s ease;
}

.unclickable {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.modes-container {
  background-color: var(--sidebar-bg);
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
  text-transform: none;
  letter-spacing: 0.5px;
  color: var(--text-color);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.equal-width-btn:hover {
  background-color: var(--mode-selector-bg-hover) !important;
}

.equal-width-btn.v-btn--active {
  background-color: var(--mode-selector-bg-selected) !important;
}

.mode-text {
  transform: translate(30px, -5px);
  font-size: 0.7rem;
}

.selected-course {
  background-color: var(--course-selected-bg);
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
  background: var(--course-sidebar-gradient);
  opacity: 1;
}
</style>
