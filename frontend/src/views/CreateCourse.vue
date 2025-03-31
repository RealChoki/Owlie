<template>
  <div
    class="d-flex flex-column vh-100"
    style="background-color: var(--color-black)"
  >
    <!-- Navbar -->
    <div class="container-fluid navbar-container">
      <nav
        class="py-2 px-3 d-flex align-items-center justify-content-between mt-1"
      >
        <!-- Home Icon -->
        <button
          class="btn btn-link p-0 d-flex align-items-center"
          @click="handleHomeClick"
          aria-label="Home"
        >
          <font-awesome-icon
            class="icon-click-effect nav-icon-holder"
            :icon="['fas', 'home']"
            style="color: var(--color-gray-shadow)"
          />
        </button>
        <div class="nav-icon-holder">
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
    <div
      class="d-flex flex-grow-1 p-1"
      style="background-color: var(--color-black)"
    >
      <div
        class="w-100 rounded text-white p-4 bruh container-fluid"
        style="
          background-color: var(--color-background-dark);
          border: 1px solid var(--color-gray-shadow);
          margin: 5px;
          overflow-y: auto;
          max-height: calc(100vh - 60px);
        "
      >
        <h3 class="text-center my-3"><strong>Courses</strong></h3>
        <div class="d-flex justify-content-end">
          <div class="search-container">
            <input
              ref="searchInput"
              type="text"
              v-model="searchQuery"
              class="search-bar"
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
        </div>
        <div class="courses-grid mt-4">
          <div class="row">
            <div
              class="col-12 col-md-4 mb-4"
              v-for="course in filteredCourses"
              :key="course.courseId"
            >
              <div
                class="course-card p-3 position-relative d-flex justify-content-between cursor-pointer"
                style=""
                @click="goToCourseDashboard(course)"
              >
                <!-- Course Title & ID -->
                <div class="card-container">
                  <div>
                    <h5>{{ course.courseName }}</h5>
                    <p>ID: {{ course.courseId }}</p>
                    <p class="mb-0">Subject: {{ course.subject }}</p>
                  </div>
                  <div class="modes-container">
                    <div
                      v-for="mode in ['General', 'Exam', 'Quiz']"
                      :key="mode"
                      class="d-flex align-items-end"
                    >
                      <span
                        :class="[
                          'mode-badge',
                          getModeColorClass(mode, course.assistantStatuses),
                        ]"
                      >
                        {{ mode }}
                        <span class="mode-tooltip">
                          {{
                            getModeStatusText(mode, course.assistantStatuses)
                          }}
                        </span>
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Delete Button -->
                <font-awesome-icon
                  class="delete-icon"
                  :icon="['fas', 'trash']"
                  @click.stop="confirmDelete(course)"
                />
              </div>
            </div>
            <div class="col-12 col-md-4 mb-4">
              <div
                class="add-course-card p-3 d-flex align-items-center justify-content-center cursor-pointer"
                @click="toggleCourseModal"
              >
                <font-awesome-icon :icon="['fas', 'plus']" size="2x" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Delete Confirmation -->
    <div v-if="isDeletePopupVisible" class="modal-overlay">
      <div class="modal-content">
        <h3 class="text-center mb-4 text-white"><u>Delete a Course</u></h3>
        <p class="text-white">
          <strong><span class="text-red">Warning:</span></strong> Deleting
          <strong>{{ courseToDelete.courseName }}</strong> (Course ID:
          <strong>{{ courseToDelete.courseId }}</strong
          >) will permanently remove the course and all its associated
          assistants. This action cannot be undone. To proceed, please enter the
          course name and ID below:
        </p>
        <input
          v-model="confirmCourseName"
          class="login-input w-100 mb-2"
          placeholder="Confirm course name"
          required
        />
        <input
          v-model="confirmCourseId"
          class="login-input w-100 mb-2"
          placeholder="Confirm course ID"
          type="number"
          required
        />
        <button
          class="btn btn-danger w-100"
          @click="deleteCourse"
          :disabled="!canDelete"
        >
          Delete Course
        </button>
        <button
          class="btn btn-secondary w-100 mt-2"
          @click="isDeletePopupVisible = false"
        >
          Cancel
        </button>
      </div>
    </div>

    <!-- Modal for Course Form -->
    <div v-if="isCourseFormVisible" class="modal-overlay">
      <div class="modal-content">
        <h3 class="text-center mb-4 text-white"><u>Create a Course</u></h3>
        <form @submit.prevent="addCourse">
          <div class="mb-3">
            <label for="subjectSelectModal" class="form-label">Subject</label>
            <input
              id="subjectSelectModal"
              v-model="subjectQuery"
              type="text"
              class="login-input w-100"
              placeholder="Type to search..."
              @input="filterOptions"
              @focus="isFocused = true"
              @blur="isFocused = false"
            />
            <!-- Options dropdown -->
            <ul
              v-if="isFocused && subjectQuery && filteredOptions.length > 0"
              class="dropdown-menu w-100"
              :class="{
                show: isFocused && subjectQuery && filteredOptions.length > 0,
              }"
            >
              <li
                v-for="option in filteredOptions"
                :key="option"
                class="dropdown-item"
                @click="selectOption(option)"
              >
                {{ option }}
              </li>
            </ul>
          </div>
          <div class="mb-3">
            <label for="courseNameInputModal" class="form-label"
              >Course Name</label
            >
            <input
              type="text"
              id="courseNameInputModal"
              v-model="courseName"
              class="login-input w-100"
              placeholder="Enter course name"
              required
            />
          </div>
          <div class="mb-3">
            <label for="courseIdInputModal" class="form-label">Course ID</label>
            <input
              type="number"
              id="courseIdInputModal"
              v-model="courseId"
              class="login-input w-100"
              placeholder="Enter course ID"
              min="10000"
              max="99999"
              required
            />
          </div>
          <button type="submit" class="btn btn-action w-100">
            Create course
          </button>
          <button
            type="button"
            class="btn btn-secondary w-100 mt-2"
            @click="toggleCourseModal"
          >
            Cancel
          </button>
        </form>
      </div>
    </div>
    <!-- End Modal -->
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { ref, computed } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faHome,
  faPlus,
  faTrash,
  faCogs,
  faQuestionCircle,
  faFileAlt,
  faMagnifyingGlass,
} from "@fortawesome/free-solid-svg-icons";
import Profilemenu from "../widgets/ProfileMenu.vue"; // or correct path

library.add(
  faHome,
  faPlus,
  faTrash,
  faCogs,
  faQuestionCircle,
  faFileAlt,
  faMagnifyingGlass
);

const isProfileMenuVisible = ref(false);
const router = useRouter();

const courseName = ref("");
const courseId = ref("");

const courses = ref([
  {
    courseId: "12345",
    courseName: "Data Science",
    subject: "Wirtschaftsinformatik",
    assistantStatuses: {
      Active: ["General", "Exam", "Quiz"],
      Inactive: [],
      Activating: [],
    },
  },
  {
    courseId: "67890",
    courseName: "Integrierte Informations- und Kommunikationssysteme",
    subject: "Medieninformatik",
    assistantStatuses: {
      Active: [],
      Inactive: ["General"],
      Activating: ["Exam", "Quiz"],
    },
  },
  {
    courseId: "23890",
    courseName: "Web security",
    subject: "Medieninformatik",
    assistantStatuses: {
      Active: ["General"],
      Inactive: ["Quiz"],
      Activating: ["Exam"],
    },
  },
]);

const isSearchFocused = ref(false);
const searchQuery = ref("");
const filteredCourses = computed(() => {
  console.log("Filtering courses...");
  console.log(courses.value);
  return courses.value.filter(
    (course) =>
      course.courseName
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      course.courseId.includes(searchQuery.value)
  );
});

const searchInput = ref<HTMLInputElement | null>(null);
function focusInput() {
  searchInput.value?.focus();
}

function getModeColorClass(mode: string, statuses: any) {
  if (statuses.Active.includes(mode)) return "active";
  if (statuses.Activating.includes(mode)) return "activating";
  return "inactive";
}

function getModeStatusText(mode: string, statuses: any) {
  if (statuses.Active.includes(mode)) return "Active";
  if (statuses.Activating.includes(mode)) return "Activating";
  return "Inactive";
}

const options = ref(["Wirtschaftsinformatik", "Medieninformatik"]);
const subjectQuery = ref("");
const subject = ref("");
const filteredOptions = computed(() => {
  return options.value.filter((option) =>
    option.toLowerCase().includes(subjectQuery.value.toLowerCase())
  );
});

const selectOption = (option: string) => {
  subject.value = option;
  subjectQuery.value = option;
};

// Controls the visibility of the modal form
const isCourseFormVisible = ref(false);

const isDeletePopupVisible = ref(false);
const courseToDelete = ref<{
  subject: string;
  courseName: string;
  courseId: string;
} | null>(null);
const confirmCourseName = ref("");
const confirmCourseId = ref("");

const addCourse = () => {
  const newCourse = {
    courseId: courseId.value as string,
    courseName: courseName.value,
    subject: subject.value,
    assistantStatuses: {
      Active: [],
      Inactive: ["General", "Quiz", "Exam"], // Defaulting all to Inactive
      Activating: [],
    },
  };
  courses.value.push(newCourse);
  console.log("Form submitted with data:", newCourse);

  // Clear the input fields after submission
  courseName.value = "";
  courseId.value = "";

  // Hide the modal
  isCourseFormVisible.value = false;
  console.log(courses.value); // WTF??? press on profile pic
};

const handleHomeClick = () => {
  router.push("/");
};

const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
};

const toggleCourseModal = () => {
  isCourseFormVisible.value = !isCourseFormVisible.value;
  resetCourseModal();
};

const resetCourseModal = () => {
  courseName.value = "";
  courseId.value = "";
  subject.value = "";
  subjectQuery.value = "";
};

const confirmDelete = (course: {
  subject: string;
  courseName: string;
  courseId: string;
}) => {
  courseToDelete.value = course;
  confirmCourseName.value = "";
  confirmCourseId.value = "";
  isDeletePopupVisible.value = true;

  console.log(courses.value);
};

const deleteCourse = () => {
  if (
    courseToDelete.value &&
    confirmCourseName.value === courseToDelete.value.courseName &&
    confirmCourseId.value === courseToDelete.value.courseId
  ) {
    courses.value = courses.value.filter(
      (course) => course.courseId !== courseToDelete.value.courseId
    );
    isDeletePopupVisible.value = false;
  }
};

const getStatusClass = (status: string) => {
  switch (status) {
    case "Active":
      return "badge-success"; // Green
    case "Activating":
      return "badge-info"; // Blue
    case "Inactive":
      return "badge-danger"; // Red
    default:
      return "badge-secondary"; // Default gray
  }
};

const canDelete = computed(() => {
  return (
    courseToDelete.value &&
    confirmCourseName.value === courseToDelete.value.courseName &&
    confirmCourseId.value === courseToDelete.value.courseId
  );
});

const goToCourseDashboard = (course: {
  subject: string;
  courseName: string;
  courseId: string;
  assistantStatus: "Active" | "Inactive" | "Activating";
  assistantTypes: Array<"General" | "Quiz" | "Exam">;
}) => {
  router.push({
    name: 'courseDashboard',
    params: {
      courseId: course.courseId,
    }
  })
};
</script>

<style scoped>
.form-label {
  color: var(--color-white);
  margin-bottom: 0.1em;
}

.navbar-container {
  background-color: var(--color-black);
}

.bruh {
  scrollbar-width: none;
  padding-bottom: 1em !important;
  min-width: 305px;
}

.btn-action {
  background-color: green;
  color: var(--color-white);
  border-color: var(--color-gray-light);
}
.btn-action:hover {
  background-color: darkgreen; /* Darker green on hover */
  color: var(--color-white);
  border-color: var(--color-gray-light);
}
.btn-action:focus {
  background-color: darkgreen; /* Darker green on focus */
  color: var(--color-white);
  border-color: var(--color-gray-light);
}
.btn-action:active {
  background-color: #004d00; /* Even darker green on active */
  color: var(--color-white);
  border-color: var(--color-gray-light);
}
.btn-action:disabled {
  background-color: var(--color-disabled);
  border-color: var(--color-disabled);
}

.btn-danger:disabled {
  pointer-events: all !important; /* override Bootstrap */
  cursor: not-allowed !important;
}

.login-input {
  background-color: var(--color-gray-medium);
  color: var(--color-white);
  padding: 0.5rem;
  padding-left: 1rem;
  border: 1px solid var(--color-gray-light);
  border-radius: 6px;
}
.login-input:focus {
  outline: none;
}
.login-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.2s ease;
}

/* Courses Grid Styling */
.courses-grid h4 {
  text-align: center;
}

.courses-grid .row {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch; /* ensures all items stretch to match the tallest one */
}

.course-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: var(--color-background-dark);
  border: 1px solid var(--color-gray-shadow);
  border-radius: 6px;
  height: 100%; /* match the tallest card's height */
  transition: transform 0.15s ease;
}

.course-card:hover {
  transform: scale(1.01);
  border-color: var(--color-primary); /* Optional hover color */
}

.assistant-status {
  opacity: 0;
}

.course-card:hover .assistant-status {
  opacity: 1;
}
/* Add New Course Card Styling */
.add-course-card {
  border: 2px dashed var(--color-gray-light);
  border-radius: 6px; /* Match course card radius */
  height: 100%; /* Fill column height */
  min-height: 200px; /* Optional: Match card min-height if needed */
  transition: transform 0.2s ease;
}

.add-course-card:hover {
  transform: scale(1.01); /* Match course card hover effect */
  border-color: var(--color-primary); /* Optional hover color */
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background-color: var(--color-background-dark);
  padding: 2rem;
  border: 1px solid var(--color-gray-shadow);
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}

/* btn-secondary styling (if not already defined globally) */
.btn-secondary {
  background-color: var(--color-gray-medium);
  color: var(--color-white);
  border: 1px solid var(--color-gray-light);
}

/* Hide the default arrows in number input */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}

.delete-icon {
  position: absolute;
  top: 12px;
  right: 12px;
  color: rgb(255, 75, 75);
  cursor: pointer;
}

/* Assistant Status Badges */
.badge {
  padding: 0.4em 0.65em;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: bold;
}
.badge-success {
  background-color: #168f1a; /* less bright green */
  color: #fff;
}
.badge-info {
  background-color: #039cbe; /* subdued blue */
  color: #fff;
}
.badge-danger {
  background-color: #aa1b25; /* darker red */
  color: #fff;
}

/* Assistant Type Badges */
.assistant-type-badge {
  background-color: var(--color-gray-medium);
  color: white;
  padding: 0.2em 0.5em;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-top: 0.4em;
}

/* Assistant Icons */
.assistant-icon {
  font-size: 1rem;
  margin-right: 5px;
}

.course-card .delete-icon {
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}

.course-card:hover .delete-icon {
  opacity: 1;
}

.course-card:hover .delete-icon {
  opacity: 1;
}
.dropdown-menu {
  position: absolute;
  z-index: 1000;
  display: block;
  max-height: 200px;
  overflow-y: auto;
  margin-top: 0.25rem;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.175);
  background-color: var(--color-gray-medium);
  color: white;
}

.dropdown-item {
  color: white;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: var(--color-gray-medium);
  color: white;
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

.search-bar {
  background-color: var(--color-gray-medium);
  border: 1px solid transparent;
  color: white;
  border-radius: 20px;
  padding: 0.5rem;
  padding-left: 2.6rem;
  width: 100%;
}

.search-bar:focus {
  outline: none;
  border: 1px solid var(--color-gray-shadow);
}

.search-bar::placeholder {
  transition: color 0.2s ease;
}

.input-focused::placeholder {
  color: white !important;
}

.mode-badge {
  color: #fff;
  padding: 0.4em 0.65em;
  margin-right: 0.25rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: bold;
  position: relative;
  cursor: pointer;
}

/* Match each status to a color */
.mode-badge.active {
  background-color: #168f1a; /* Green */
}
.mode-badge.inactive {
  background-color: #aa1b25; /* Red */
}
.mode-badge.activating {
  background-color: #039cbe; /* Blue */
}

/* Tooltip style */
.mode-tooltip {
  display: none;
  position: absolute;
  bottom: calc(100% + 8px); /* Tooltip positioned above the target */
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--color-gray-light);
  color: #fff;
  padding: 0.25em 0.5em;
  border-radius: 4px;
  font-size: 0.65rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease-in-out; /* Add transition for opacity */
}

.mode-tooltip::after {
  content: "";
  position: absolute;
  bottom: -11px; /* Move the arrow beneath the tooltip */
  left: 50%;
  transform: translateX(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: var(--color-gray-light) transparent transparent transparent; /* Adjust the arrow color */
}

.mode-badge:hover .mode-tooltip {
  display: block;
  animation: fadeIn 0.3s forwards; /* Add animation for fade-in with delay */
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

.card-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100%;
}

.card-container h5 {
  word-wrap: break-word; /* Ensures long words break */
  word-break: break-word; /* Breaks long words */
  overflow-wrap: break-word; /* Alternative for better browser support */
}

.modes-container {
  display: flex;
}

@media (min-width: 768px) {
  .search-bar {
    width: 30vw;
    min-width: 200px;
    max-width: 400px;
  }
}

@media (max-width: 767px) {
  .search-container {
    width: 100%;
  }

  .add-course-card {
    min-height: 130px;
  }
}

@media (min-width: 768px) and (max-width: 1535px) {
  .card-container {
    flex-direction: column;
  }

  .modes-container {
    margin-top: 0.8em;
    justify-content: start;
  }
}

@media (max-width: 650px) {
  .card-container {
    flex-direction: column;
  }

  .modes-container {
    margin-top: 0.8em;
    justify-content: start;
  }

  .add-course-card {
    min-height: 170px;
  }
}
</style>
