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

    <!-- Main Content -->
    <div class="d-flex flex-grow-1">
      <!-- Sidebar -->
      <div class="sidebar py-3 px-3">
        <h3>Dashboard</h3>
        <!-- Vertical Tabs Navigation -->
        <div class="tabs-container text-white mb-3">
          <ul class="p-o mt-1">
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'assistants' }"
              class="list-item-hover py-2 rounded text-white py-1 cursor-pointer"
              @click="activeTab = 'assistants'"
            >
              Assistants
            </li>
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'usage' }"
              class="list-item-hover py-2 rounded text-white py-1 cursor-pointer"
              @click="activeTab = 'usage'"
            >
              Usage
            </li>
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'stats' }"
              class="list-item-hover py-2 rounded text-white py-1 cursor-pointer"
              @click="activeTab = 'stats'"
            >
              Stats
            </li>
          </ul>
        </div>
      </div>

      <!-- Right Content -->
      <div
        class="right-side w-100 d-flex flex-column align-items-center rounded pt-3 px-3"
      >
        <!-- Assistants Tab -->
        <div v-if="activeTab === 'assistants'" class="assistants-tab w-100">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h3 class="text-white mb-0">Data Science</h3>
              <span class="text-white small">(ID: 67437)</span>
            </div>

            <!-- Sub-tabs for Assistant Modes -->
            <div class="rounded">
              <ul
                class="tabs-list list-unstyled text-white d-flex flex-row m-0"
              >
                <li
                  :class="{
                    'tab-item-active': activeAssistantMode === 'General',
                    'tab-item-inactive': activeAssistantMode !== 'General',
                  }"
                  class="tab-item cursor-pointer tab-left-rounded px-4 py-2"
                  @click="activeAssistantMode = 'General'"
                >
                  General
                </li>
                <li
                  :class="{
                    'tab-item-active': activeAssistantMode === 'Quiz',
                    'tab-item-inactive': activeAssistantMode !== 'Quiz',
                  }"
                  class="tab-item cursor-pointer tab-middle px-4 py-2"
                  @click="activeAssistantMode = 'Quiz'"
                >
                  Quiz
                </li>
                <li
                  :class="{
                    'tab-item-active': activeAssistantMode === 'Exam',
                    'tab-item-inactive': activeAssistantMode !== 'Exam',
                  }"
                  class="tab-item cursor-pointer tab-right-rounded px-4 py-2"
                  @click="activeAssistantMode = 'Exam'"
                >
                  Exam
                </li>
              </ul>
            </div>
          </div>
          <hr class="text-white" />
          <!-- Configuration Panel for the Selected Assistant Mode -->
          <div
            v-if="activeModeIndex !== -1"
            class="assistant-config-panel p-3 rounded"
          >
            <div class="d-flex align-items-center justify-content-between mb-2">
              <strong
                >{{ assistantModes[activeModeIndex].name }} Assistant</strong
              >
              <span
                :class="
                  getAssistantStatusClass(
                    assistantModes[activeModeIndex].status
                  )
                "
              >
                {{ assistantModes[activeModeIndex].status }}
              </span>
            </div>
            <!-- Moodle Toggle -->
            <div class="form-check form-switch mb-2">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="assistantModes[activeModeIndex].moodleEnabled"
                :id="assistantModes[activeModeIndex].name + '-moodleSwitch'"
              />
              <label
                class="form-check-label"
                :for="assistantModes[activeModeIndex].name + '-moodleSwitch'"
              >
                Enable Moodle Tool
              </label>
            </div>
            <!-- File Upload -->
            <div class="mb-2">
              <label class="text-white mb-1">Upload Files:</label>
              <input
                type="file"
                multiple
                @change="(e) => onFilesSelected(e, activeModeIndex)"
                class="form-control form-control-sm"
              />
            </div>
            <!-- Lecture Links -->
            <div class="mb-2">
              <label class="text-white mb-1">Lecture Links:</label>
              <input
                type="text"
                v-model="assistantModes[activeModeIndex].links"
                placeholder="Enter lecture links separated by commas"
                class="form-control form-control-sm"
              />
            </div>
            <!-- Instructions Field -->
            <div class="mb-2">
              <label class="text-white mb-1">Instructions:</label>
              <textarea
                v-model="assistantModes[activeModeIndex].instructions"
                placeholder="Enter instructions for this assistant"
                class="form-control"
              ></textarea>
            </div>
          </div>
          <button class="btn btn-action w-100 mt-3" @click="saveAssistants">
            Save Assistants
          </button>
        </div>

        <!-- Usage Tab -->
        <div v-else-if="activeTab === 'usage'" class="usage-tab w-100 mt-3">
          <h3 class="text-white">Usage</h3>
          <p class="text-white">
            Display usage analytics and student activity data here.
          </p>
        </div>

        <!-- Stats Tab -->
        <div v-else-if="activeTab === 'stats'" class="stats-tab w-100 mt-3">
          <h3 class="text-white">Stats</h3>
          <p class="text-white">
            Show charts, graphs, and detailed statistics here.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faMagnifyingGlass,
  faHome,
  faPenToSquare,
} from "@fortawesome/free-solid-svg-icons";
import Profilemenu from "../widgets/Profilemenu.vue";

library.add(faMagnifyingGlass, faHome, faPenToSquare);

const router = useRouter();

const searchQuery = ref("");
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);
function focusInput() {
  searchInput.value?.focus();
}

// Sidebar Tabs
const activeTab = ref<"assistants" | "usage" | "stats">("assistants");

// Dummy course data (replace with actual fetch logic if needed)
const course = ref({
  courseName: "Sample Course",
});

// Assistant Modes Configuration
type AssistantStatus = "Active" | "Inactive" | "Activating";
interface AssistantMode {
  name: "General" | "Quiz" | "Exam";
  status: AssistantStatus;
  moodleEnabled: boolean;
  files: File[];
  links: string;
  instructions: string;
}
const assistantModes = ref<AssistantMode[]>([
  {
    name: "General",
    status: "Active",
    moodleEnabled: false,
    files: [],
    links: "",
    instructions: "",
  },
  {
    name: "Quiz",
    status: "Inactive",
    moodleEnabled: false,
    files: [],
    links: "",
    instructions: "",
  },
  {
    name: "Exam",
    status: "Activating",
    moodleEnabled: false,
    files: [],
    links: "",
    instructions: "",
  },
]);

// Active Assistant Mode Sub-tab
const activeAssistantMode = ref<"General" | "Quiz" | "Exam">("General");
const activeModeIndex = computed(() =>
  assistantModes.value.findIndex(
    (mode) => mode.name === activeAssistantMode.value
  )
);

function getAssistantStatusClass(status: AssistantStatus) {
  switch (status) {
    case "Active":
      return "text-success";
    case "Activating":
      return "text-info";
    case "Inactive":
      return "text-danger";
    default:
      return "text-muted";
  }
}

function onFilesSelected(event: Event, index: number) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    assistantModes.value[index].files = Array.from(input.files);
  }
}

function saveAssistants() {
  console.log("Assistant Modes Configuration:", assistantModes.value);
  alert("Assistants configuration saved!");
  // Place your API call or further navigation logic here.
}

// Profile Menu and Navbar handlers
const isProfileMenuVisible = ref(false);
function toggleProfileMenu() {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
}
function handleHomeClick() {
  router.push("/");
}
</script>

<style scoped>
/* Navbar */
.navbar-container {
  background-color: var(--color-black);
}

/* Sidebar */
.sidebar {
  background-color: var(--color-black);
  min-width: 305px;
  max-width: 305px;
  padding: 1rem;
  color: white;
  padding-right: 10px !important;
}

.input-focused::placeholder {
  color: white !important;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-gray-shadow);
}

.selected-sidebar-item {
  background-color: var(--color-gray-medium);
  position: relative;
  overflow: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.selected-sidebar-item::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background: linear-gradient(to bottom, white, var(--color-gray-shadow));
  opacity: 1;
}

/* Tabs */
.tabs-container ul {
  padding: 0;
  margin: 0;
  list-style: none;
}
.tabs-container li {
  cursor: pointer;
  padding: 0.5rem;
}

/* Assistant Mode Sub-tabs */
.tabs-list {
  margin: 0;
  padding: 0;
  display: flex;
}

.tab-item {
  font-size: 0.875rem; /* Smaller font size */
  border-radius: 6px; /* Smaller border radius */
  transition: all 0.2s ease-in-out;
}

.tab-item-active {
  background-color: var(--color-gray-light);
  color: var(--color-white);
  font-weight: bold;
}

.tab-item-inactive {
  background-color: var(--color-gray-dark);
  color: var(--color-white);
}

.tab-left-rounded {
  border-radius: 10px 0 0 10px;
}

.tab-middle {
  border-radius: 0;
}

.tab-right-rounded {
  border-radius: 0 10px 10px 0;
}

/* Right Content */
.right-side {
  background-color: var(--color-background-dark);
  border: 1px solid var(--color-gray-shadow);
  margin: 5px;
  padding: 1rem;
  overflow-y: auto;
}

/* Assistants Tab Styles */
.assistant-modes {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.assistant-mode,
.assistant-config-panel {
  background-color: var(--color-gray-dark);
}
.btn-action {
  background-color: green;
  color: var(--color-white);
  border: none;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
}
.btn-action:hover {
  background-color: darkgreen;
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
</style>
