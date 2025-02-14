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
            style="color: var(--color-white)"
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
        class="w-100 rounded text-white p-4 bruh"
        style="
          background-color: var(--color-background-dark);
          border: 1px solid var(--color-gray-shadow);
          margin: 5px;
          overflow-y: auto;
          max-height: calc(100vh - 60px);
        "
      >
        <h3 class="text-center mb-3 mt-4">Courses</h3>
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
                class="course-card p-3 position-relative"
                style="
                  background-color: var(--color-background-dark);
                  border: 1px solid var(--color-gray-shadow);
                  border-radius: 6px;
                "
                @click="goToCourseDashboard(course)"
              >
                <!-- Course Title & ID -->
                <h5>{{ course.courseName }}</h5>
                <p>ID: {{ course.courseId }}</p>
                <p>Subject: {{ course.subject }}</p>

                <!-- Assistant Status Badge -->
                <div class="assistant-status mb-2">
                  <span
                    class="badge"
                    :class="getStatusClass(course.assistantStatus)"
                  >
                    {{ course.assistantStatus }}
                  </span>
                </div>

                <!-- Assistant Types -->
                <div class="assistant-types d-flex gap-2">
                  <span
                    v-for="type in course.assistantTypes"
                    :key="type"
                    class="assistant-type-badge"
                  >
                    <font-awesome-icon
                      v-if="type === 'General'"
                      :icon="['fas', 'cogs']"
                      class="assistant-icon"
                    />
                    <font-awesome-icon
                      v-else-if="type === 'Quiz'"
                      :icon="['fas', 'question-circle']"
                      class="assistant-icon"
                    />
                    <font-awesome-icon
                      v-else-if="type === 'Exam'"
                      :icon="['fas', 'file-alt']"
                      class="assistant-icon"
                    />
                    {{ type }}
                  </span>
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
              <div class="add-course-card" @click="toggleCourseModal">
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
        <h3 class="text-center mb-4 text-white"><u>Delete Course</u></h3>
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
          placeholder="Confrim course name"
          required
        />
        <input
          v-model="confirmCourseId"
          class="login-input w-100 mb-2"
          placeholder="Confrim course ID"
          type="number"
          required
        />
        <button class="btn btn-danger w-100" @click="deleteCourse">
          Confirm Deletion
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

const courses = ref<
  Array<{
    subject: string;
    courseName: string;
    courseId: string;
    assistantStatus: "Active" | "Inactive" | "Activating";
    assistantTypes: Array<"General" | "Quiz" | "Exam">;
  }>
>([
  {
    courseId: "12345",
    courseName: "Data Science",
    subject: "Wirtschaftsinformatik",
    assistantStatus: "Active",
    assistantTypes: ["General", "Quiz"],
  },
  {
    courseId: "67890",
    courseName: "Web Development",
    subject: "Medieninformatik",
    assistantStatus: "Inactive",
    assistantTypes: ["Exam"],
  },
  {
    courseId: "23890",
    courseName: "Web security",
    subject: "Medieninformatik",
    assistantStatus: "Activating",
    assistantTypes: ["Exam"],
  },
]);

const isSearchFocused = ref(false);
const searchQuery = ref("");
const filteredCourses = computed(() => {
  return courses.value.filter(course => 
    course.courseName.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    course.courseId.includes(searchQuery.value)
  );
});

const searchInput = ref<HTMLInputElement | null>(null);
function focusInput() {
  searchInput.value?.focus();
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
    subject: subject.value,
    courseName: courseName.value,
    courseId: courseId.value,
    assistantStatus: "Inactive" as "Inactive", // Ensure the correct type
    assistantTypes: [] as Array<"General" | "Quiz" | "Exam">, // Enforce type for assistantTypes
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

const goToCourseDashboard = (course: {
  subject: string;
  courseName: string;
  courseId: string;
  assistantStatus: "Active" | "Inactive" | "Activating";
  assistantTypes: Array<"General" | "Quiz" | "Exam">;
}) => {
  router.push({
    name: "courseDashboard",
    params: { courseId: course.courseId },
  });
};
</script>

<style scoped>
.form-label {
  color: var(--color-white);
}

.navbar-container {
  background-color: var(--color-black);
}

.bruh {
  scrollbar-width: none;
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
.course-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}
.course-card:hover {
  transform: scale(1.02);
}

/* Add New Course Card Styling */
.add-course-card {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--color-gray-light);
  border-radius: 50%;
  height: 100px;
  width: 100px;
  margin: auto;
  transition: transform 0.2s ease;
  cursor: pointer;
}
.add-course-card:hover {
  transform: scale(1.05);
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
  padding: 0.4em 0.8em;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: bold;
}
.badge-success {
  background-color: green;
  color: white;
}
.badge-info {
  background-color: blue;
  color: white;
}
.badge-danger {
  background-color: red;
  color: white;
}

/* Assistant Type Badges */
.assistant-type-badge {
  background-color: var(--color-gray-medium);
  color: white;
  padding: 0.3em 0.6em;
  border-radius: 6px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Assistant Icons */
.assistant-icon {
  font-size: 1rem;
  margin-right: 5px;
}

.course-card .delete-icon {
  opacity: 0;
  transition: opacity 0.1s ease-in-out;
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

.search-bar {
  background-color: var(--color-gray-medium);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.5rem;
  padding-left: 2.6rem;
  width: 100%;
}

.search-bar:focus {
  outline: none;
}

.search-bar::placeholder {
  transition: color 0.2s ease;
}

.input-focused::placeholder {
  color: white !important;
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
</style>
