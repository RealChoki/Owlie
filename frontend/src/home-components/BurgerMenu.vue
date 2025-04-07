<template>
  <div class="burger-menu py-3 px-3 rounded shadow-sm">
    <div class="search-container">
      <input
        ref="searchInput"
        type="text"
        v-model="searchQuery"
        class="burger-menu-search-bar w-100"
        :placeholder="$t('sidebar.searchPlaceholder')"
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
        :class="{ 'input-focused': isSearchFocused }"
        maxlength="50"
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
        @click="closeBurgerMenu"
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
          @click="
            isCourseClickable(course) ? selectCourse(course) : null;
            handleCourseClick(course)
          "
        >
          <p class="m-0 py-2 px-2 d-flex align-items-start position-relative">
            <span class="course-name position-relative">
              {{ course }}
              <span
                v-if="selectedMode !== 'general'"
                class="mode-text text-secondary small position-absolute top-0 end-0"
              >
                ({{ $t(`sidebar.courseTitleMode.${selectedMode}`) }})
              </span>
            </span>
          </p>
        </li>
      </ul>
    </div>

    <div class="mode-toggle d-flex flex-column align-items-center modes-container p-3 pt-2">
      <div class="d-flex gap-2" style="color: var(--text-color)">
        <h6 class="m-0">{{ $t('sidebar.modeSelectTitleBurger') }}</h6>
      </div>
      <div v-if="showInfo" class="small mt-1 text-warning text-center max-width-450">
        <div v-if="selectedMode === 'general'">
          {{ $t('sidebar.modeGeneralDescription') }}
        </div>
        <div v-if="selectedMode === 'quiz'">
          {{ $t('sidebar.modeQuizDescription') }}
        </div>
        <div v-if="selectedMode === 'exam'">
          {{ $t('sidebar.modeExamDescription') }}
        </div>
      </div>

      <div class="d-flex justify-content-center mt-2 w-100 position-relative max-width-450">
        <v-btn-toggle
          v-model="selectedMode"
          mandatory
          rounded="x2"
          base-color="var(--mode-selector-bg)"
          class="equal-width-toggle"
        >
          <v-btn value="general" class="equal-width-btn"> {{ $t('sidebar.modeGeneral') }} </v-btn>
          <v-btn
            value="quiz"
            class="equal-width-btn"
            style="border-left: var(--mode-selector-border); border-right: var(--mode-selector-border)"
            >{{ $t('sidebar.modeQuiz') }}</v-btn
          >
          <v-btn value="exam" class="equal-width-btn">{{ $t('sidebar.modeExam') }}</v-btn>
        </v-btn-toggle>
        <font-awesome-icon
          :icon="['fas', 'circle-info']"
          class="circle-info cursor-pointer"
          style="color: var(--info-icon-bg)"
          @click="toggleInfo"
        />
      </div>

      <button
        ref="profileBtn"
        class="max-width-450 mt-2 d-flex align-items-center w-100 p-2 text-dark border-0 profile-btn"
        type="button"
        aria-haspopup="menu"
        @click="toggleProfileMenu"
        :style="{ backgroundColor: isProfileMenuVisible ? 'var(--profile-btn-selected-bg)' : '' }"
      >
        <div class="me-2 ms-1">
          <font-awesome-icon
            class="cursor-pointer icon-click-effect"
            :icon="['fas', 'user-circle']"
            style="color: var(--text-color)"
          />
        </div>
        <div class="text-start text-truncate" style="color: var(--text-color)">
          <span>Your profile</span>
        </div>
      </button>
      <ProfileMenu
        v-if="isProfileMenuVisible"
        :origin="'BurgerMenu'"
        @toggleProfileMenu="toggleProfileMenu"
        @openSettings="openSettings"
        :style="{ width: buttonWidth + 'px' }"
      />
    </div>
    <SettingsMenuModal />
  </div>
</template>

<script setup lang="ts">
import SettingsMenuModal from '@/home-components/SettingsMenuModal.vue'
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { VBtn, VBtnToggle } from 'vuetify/components'
import { useThread } from '../hooks/useThread'
import { clearMessages } from '../services/chatService'
import { fetchAssistantIds, courses } from '../services/courseService'
import { getAssistantCourse, getAssistantMode, setAssistantCourse, setAssistantMode } from '../services/openaiService'
import { setNavbarCourseTitle } from '../services/homeService'
import ProfileMenu from '@/widgets/ProfileMenu.vue'
import { stopTTS } from '../services/ttsService'
import * as bootstrap from 'bootstrap'

const props = defineProps({
  isBurgerMenuOpen: Boolean
})

const emit = defineEmits(['closeBurgerMenu'])

const showSettings = ref(false)
function openModal(modalId: string) {
  const modalElement = document.getElementById(modalId)
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

function openSettings() {
  showSettings.value = true
  openModal('settingsModal')
}

const searchQuery = ref('')
const isSearchFocused = ref(false)
const searchInput = ref<HTMLInputElement | null>(null)

const selectedMode = ref(getAssistantMode() || 'general')
const courseClicked = ref<{ course: string; mode: string } | null>(null)
const showInfo = ref(false)

function toggleMode() {
  if (selectedMode.value === 'general') {
    selectedMode.value = 'quiz'
  } else if (selectedMode.value === 'quiz') {
    selectedMode.value = 'exam'
  } else {
    selectedMode.value = 'general'
  }
}

const clickableCourses = ref<string[]>(['Grundlagen der Programmierung'])

const profileBtn = ref<HTMLElement | null>(null)
const buttonWidth = ref(0)
const updatetoggleProfileMenuWidth = () => {
  if (profileBtn.value) {
    buttonWidth.value = profileBtn.value.offsetWidth
  }
}

const isProfileMenuVisible = ref(false)
const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value
  if (showInfo.value) {
    toggleInfo()
  }
}

function isCourseClickable(course: string): boolean {
  // temp code
  if (course === 'Grundlagen der Programmierung' && selectedMode.value === 'exam') {
    return false // Exclude this course and 'exam' mode
  }
  // end temp code

  return clickableCourses.value.includes(course)
}

// Generate dynamic classes for courses
const courseClass = (course: string) => ({
  unclickable: !isCourseClickable(course),
  'cursor-pointer': isCourseClickable(course),
  'selected-course': isCourseClicked(course)
})

function handleCourseClick(course: string) {
  if (!isCourseClickable(course)) {
    return
  }
  setNavbarCourseTitle(course, selectedMode.value)
}

function isCourseClicked(course: string): boolean {
  return (
    courseClicked.value !== null &&
    course === courseClicked.value.course &&
    selectedMode.value === courseClicked.value.mode
  )
}

const filteredCourses = computed(() => {
  const query = searchQuery.value.toLowerCase()
  const filtered = courses.value.filter((course) => course.toLowerCase().includes(query))

  const clickable = filtered.filter(isCourseClickable)
  const unclickable = filtered.filter((course) => !isCourseClickable(course))

  return [...clickable, ...unclickable.sort()]
})

const { clearThread, initializeThread } = useThread(ref(undefined), () => {})

async function selectCourse(course: string) {
  if (!isCourseClickable(course)) {
    return
  }
  console.log('Selected course:', course)
  setTimeout(() => {
    closeBurgerMenu()
  }, 350)
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
      return
    }
  } else {
    console.log('Same course and mode selected. No action taken.')
  }
}

function closeBurgerMenu() {
  emit('closeBurgerMenu')
}

function focusInput() {
  searchInput.value?.focus()
}

function toggleInfo() {
  showInfo.value = !showInfo.value
}

function handleResize() {
  if (window.innerWidth >= 768) {
    emit('closeBurgerMenu')
  }
  updatetoggleProfileMenuWidth()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  handleResize() // Initial check
  const currentCourse = getAssistantCourse()
  const currentMode = getAssistantMode()
  if (currentCourse && currentMode) {
    courseClicked.value = { course: currentCourse, mode: currentMode }
    selectedMode.value = currentMode
  }
})

// Remove the resize handler when the component is unmounted
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.burger-menu {
  background-color: var(--sidebar-bg);
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  width: 80vw;
  z-index: 10;
  min-width: 305px;
  padding-right: 10px !important;
}

.course-list-container {
  max-height: 82vh;
  overflow-y: auto;
  scrollbar-width: none;
}

.burger-menu-search-bar {
  background-color: var(--course-search-bg);
  color: var(--text-color);
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
  padding-bottom: 0.75em;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  transition: color 0.2s ease;
}

.input-focused::placeholder {
  color: var(--text-color) !important;
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

.max-width-450 {
  width: 100%;
  max-width: 450px;
  box-sizing: border-box;
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

.equal-width-toggle {
  display: flex;
  justify-content: center;
  align-items: stretch;
  width: 100%;
}

.circle-info {
  position: absolute;
  top: -4px;
  right: -4px;
}

/* Other styles remain the same */

.unclickable {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.unclickable:hover {
  background-color: transparent !important;
}

.modes-container {
  background-color: var(--sidebar-bg);
  overflow: visible;
}

.mode-text {
  transform: translate(32px, -5px);
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

.profile-btn {
  border-radius: 5px;
  background-color: var(--sidebar-bg);
  transition: background-color 0.5s ease;
}

.profile-btn:hover {
  background-color: var(--profile-btn-hover-bg);
}
</style>
