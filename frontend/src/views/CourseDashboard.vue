<template>
  <div class="d-flex flex-column vh-100" style="background-color: var(--color-black)">
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
            style="color: var(--color-gray-shadow);"
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
        <!-- Search Bar -->
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
        <!-- Vertical Tabs Navigation -->
        <div class="tabs-container text-white mb-3">
          <ul class="list-unstyled">
            <li
              :class="{ 'active-tab': activeTab === 'assistants' }"
              class="cursor-pointer mb-2"
              @click="activeTab = 'assistants'"
            >
              Assistants
            </li>
            <li
              :class="{ 'active-tab': activeTab === 'usage' }"
              class="cursor-pointer mb-2"
              @click="activeTab = 'usage'"
            >
              Usage
            </li>
            <li
              :class="{ 'active-tab': activeTab === 'stats' }"
              class="cursor-pointer mb-2"
              @click="activeTab = 'stats'"
            >
              Stats
            </li>
          </ul>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-side w-100 d-flex flex-column align-items-center rounded pt-3 px-3">
        <h2 class="text-white">{{ course.courseName }} Dashboard</h2>
        <!-- Assistants Tab -->
        <div v-if="activeTab === 'assistants'" class="assistants-tab w-100 mt-3">
          <!-- Sub-tabs for Assistant Modes -->
          <div class="assistant-mode-tabs mb-3">
            <ul class="list-unstyled d-flex flex-row gap-3">
              <li
                :class="{ 'active-subtab': activeAssistantMode === 'General' }"
                class="cursor-pointer"
                @click="activeAssistantMode = 'General'"
              >
                General
              </li>
              <li
                :class="{ 'active-subtab': activeAssistantMode === 'Quiz' }"
                class="cursor-pointer"
                @click="activeAssistantMode = 'Quiz'"
              >
                Quiz
              </li>
              <li
                :class="{ 'active-subtab': activeAssistantMode === 'Exam' }"
                class="cursor-pointer"
                @click="activeAssistantMode = 'Exam'"
              >
                Exam
              </li>
            </ul>
          </div>
          <!-- Configuration Panel for the Selected Assistant Mode -->
          <div v-if="activeModeIndex !== -1" class="assistant-config-panel p-3 border rounded">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <strong>{{ assistantModes[activeModeIndex].name }} Assistant</strong>
              <span :class="getAssistantStatusClass(assistantModes[activeModeIndex].status)">
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
              <label class="form-check-label" :for="assistantModes[activeModeIndex].name + '-moodleSwitch'">
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faMagnifyingGlass,
  faHome,
  faPenToSquare,
} from '@fortawesome/free-solid-svg-icons';
import Profilemenu from '../widgets/Profilemenu.vue';

library.add(faMagnifyingGlass, faHome, faPenToSquare);

const router = useRouter();

const searchQuery = ref('');
const isSearchFocused = ref(false);
const searchInput = ref<HTMLInputElement | null>(null);
function focusInput() {
  searchInput.value?.focus();
}

// Sidebar Tabs
const activeTab = ref<'assistants' | 'usage' | 'stats'>('assistants');

// Dummy course data (replace with actual fetch logic if needed)
const course = ref({
  courseName: 'Sample Course',
});

// Assistant Modes Configuration
type AssistantStatus = 'Active' | 'Inactive' | 'Activating';
interface AssistantMode {
  name: 'General' | 'Quiz' | 'Exam';
  status: AssistantStatus;
  moodleEnabled: boolean;
  files: File[];
  links: string;
  instructions: string;
}
const assistantModes = ref<AssistantMode[]>([
  { name: 'General', status: 'Active', moodleEnabled: false, files: [], links: '', instructions: '' },
  { name: 'Quiz', status: 'Inactive', moodleEnabled: false, files: [], links: '', instructions: '' },
  { name: 'Exam', status: 'Activating', moodleEnabled: false, files: [], links: '', instructions: '' },
]);

// Active Assistant Mode Sub-tab
const activeAssistantMode = ref<'General' | 'Quiz' | 'Exam'>('General');
const activeModeIndex = computed(() =>
  assistantModes.value.findIndex(mode => mode.name === activeAssistantMode.value)
);

function getAssistantStatusClass(status: AssistantStatus) {
  switch (status) {
    case 'Active':
      return 'text-success';
    case 'Activating':
      return 'text-info';
    case 'Inactive':
      return 'text-danger';
    default:
      return 'text-muted';
  }
}

function onFilesSelected(event: Event, index: number) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    assistantModes.value[index].files = Array.from(input.files);
  }
}

function saveAssistants() {
  console.log('Assistant Modes Configuration:', assistantModes.value);
  alert('Assistants configuration saved!');
  // Place your API call or further navigation logic here.
}

// Profile Menu and Navbar handlers
const isProfileMenuVisible = ref(false);
function toggleProfileMenu() {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
}
function handleHomeClick() {
  router.push('/');
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
}
.sidebar-search-bar {
  background-color: var(--color-gray-medium);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.5rem;
  padding-left: 2.6rem;
}
.input-focused::placeholder {
  color: white !important;
}
.search-container {
  position: relative;
  margin-bottom: 1rem;
}
.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-gray-shadow);
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
.active-tab {
  font-weight: bold;
  text-decoration: underline;
}

/* Assistant Mode Sub-tabs */
.assistant-mode-tabs ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  gap: 1rem;
}
.assistant-mode-tabs li {
  cursor: pointer;
  padding: 0.5rem;
  border-bottom: 2px solid transparent;
}
.active-subtab {
  font-weight: bold;
  border-color: var(--color-white);
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
</style>
