<template>
  <div class="burger-menu py-3 px-3 rounded shadow-sm">
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
        maxlength="50"
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
        @click="closeBurgerMenu"
      />
    </div>

    <!-- Scrollable Course List -->
    <div class="course-list-container">
      <ul class="p-0 mt-1">
        <li
          v-for="(course, index) in filteredCourses"
          :key="index"
          class="list-item-hover rounded text-white py-1"
          :class="courseClass(course)"
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
      class="mode-toggle d-flex flex-column align-items-center modes-container p-3 pt-2"
    >
      <div class="d-flex gap-2 text-white">
        <h6 class="m-0">Switch mode to:</h6>
      </div>
      <div
        v-if="showInfo"
        class="small mt-1 text-warning text-center max-width-450"
      >
        Quiz mode: A quiz feature that assesses knowledge, tracks performance,
        and provides personalized feedback.
      </div>

      <div
        class="d-flex justify-content-center mt-2 w-100 position-relative max-width-450"
      >
        <v-btn
          @click="toggleMode"
          class="equal-width-btn max-width-450 text-white"
          base-color="var(--color-gray-medium)"

        >
          {{ selectedMode === "general" ? "Quiz" : "General" }}
        </v-btn>
        <font-awesome-icon
          :icon="['fas', 'circle-info']"
          class="circle-info text-white cursor-pointer"
          @click="toggleInfo"
        />
      </div>

      <button
        ref="profileBtn"
        class="max-width-450 mt-2 d-flex align-items-center w-100 p-2 text-dark border-0 profile-btn"
        type="button"
        aria-haspopup="menu"
        @click="toggleProfileMenu"
        :style="{ backgroundColor: isProfileMenuVisible ? '#41414160' : '' }"
      >
        <div class="me-2">
          <div
            class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle pfp-container"
          >
            <img
              alt="User"
              src="https://scontent-ber1-1.cdninstagram.com/v/t51.2885-19/461621119_507240088873650_7983337688478167496_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=103&ccb=1-7&_nc_sid=bf7eb4&_nc_ohc=kHBp3yUY_PwQ7kNvgFeKn_N&_nc_zt=24&_nc_ht=scontent-ber1-1.cdninstagram.com&oh=00_AYBQT7SUl2ZHW8UjAiqcHAlemBrR3CEeujwiaKBKIERGCQ&oe=676F6C48"
              class="img-fluid rounded-circle"
            />
          </div>
        </div>
        <div class="text-start text-truncate text-white">
          <span>David Svoboda</span>
        </div>
      </button>
      <ProfileMenu
        v-if="isProfileMenuVisible"
        :origin="'BurgerMenu'"
        @toggleProfileMenu="toggleProfileMenu"
        :style="{ width: buttonWidth + 'px' }"
        />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  onMounted,
  onUnmounted,
  watch,
  nextTick,
} from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faMagnifyingGlass,
  faCircleInfo,
  faUserCircle,
  faGear,
  faRightFromBracket,
  faInfoCircle,
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
import ProfileMenu from "@/widgets/ProfileMenu.vue";
import { stopTTS } from "../services/ttsService";

library.add(
  faMagnifyingGlass,
  faCircleInfo,
  faUserCircle,
  faGear,
  faRightFromBracket,
  faInfoCircle
);

const props = defineProps({
  isBurgerMenuOpen: Boolean,
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

const profileBtn = ref<HTMLElement | null>(null);
const buttonWidth = ref(0);
const updatetoggleProfileMenuWidth = () => {
  if (profileBtn.value) {
    buttonWidth.value = profileBtn.value.offsetWidth;
  }
};

const isProfileMenuVisible = ref(false);
const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
    if (showInfo.value) {
    toggleInfo();
  }
};

function isCourseClickable(course: string): boolean {
  return clickableCourses.value.includes(course);
}

// Generate dynamic classes for courses
const courseClass = (course: string) => ({
  unclickable: !isCourseClickable(course),
  "cursor-pointer": isCourseClickable(course),
  "selected-course": isCourseClicked(course),
});

function handleCourseClick(course: string) {
  if (!isCourseClickable(course)) {
    return;
  }
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
  if (!isCourseClickable(course)) {return;}
  console.log("Selected course:", course);
  setTimeout(() => {
    closeBurgerMenu();
  }, 350);
  courseClicked.value = { course, mode: selectedMode.value };

  const modeName = selectedMode.value;
  const courseName = course;
  const currentMode = getAssistantMode();
  const currentCourse = getAssistantCourse();

  if (course !== currentCourse || modeName !== currentMode) {
    console.log("Course or mode changed. Resetting thread and messages.");
    stopTTS();
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
  updatetoggleProfileMenuWidth();
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
.burger-menu {
  background-color: var(--color-black);
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
  background-color: var(--color-gray-medium);
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
  padding-bottom: 0.75em;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  color: var(--color-gray-shadow);
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
  width: 100%;
  text-align: center;
  min-width: 0;
  padding: 12px 16px;
  height: auto;
  line-height: 1.2;
  text-transform: none;
  letter-spacing: 0.5px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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
  background-color: var(--color-black);
  overflow: visible;
}

.test-mode-text {
  transform: translate(30px, -5px);
  font-size: 0.7rem;
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





.profile-btn {
  border-radius: 5px;
  background-color: var(--color-black);
  transition: background-color 0.5s ease;
}

.profile-btn:hover {
  background-color: #41414149;
}

</style>
