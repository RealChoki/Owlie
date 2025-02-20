<!-- filepath: vsls:/frontend/src/views/CourseDashboard.vue -->
<template>
  <div class="d-flex flex-column vh-100" style="background-color: var(--color-black)">
    <!-- Navbar -->
    <div class="container-fluid navbar-container">
      <nav class="py-2 px-3 d-flex align-items-center justify-content-between">
        <!-- Home Icon -->
        <button class="btn btn-link p-0 d-flex align-items-center" @click="handleHomeClick" aria-label="Home">
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
        <Profilemenu v-if="isProfileMenuVisible" :origin="'Nav-EditQuiz'" @toggleProfileMenu="toggleProfileMenu" />
      </nav>
    </div>

    <!-- Main Content -->
    <div class="d-flex flex-grow-1">
      <!-- Sidebar -->
      <div class="sidebar py-3 px-3">
        <h3>Dashboard</h3>
        <!-- Vertical Tabs Navigation -->
        <div class="tabs-container text-white mb-3">
          <ul class="p-0 mt-1">
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'assistants' }"
              class="list-item-hover py-2 rounded text-white cursor-pointer"
              @click="activeTab = 'assistants'"
            >
              Assistants
            </li>
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'usage' }"
              class="list-item-hover py-2 rounded text-white cursor-pointer"
              @click="activeTab = 'usage'"
            >
              Usage
            </li>
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'stats' }"
              class="list-item-hover py-2 rounded text-white cursor-pointer"
              @click="activeTab = 'stats'"
            >
              Stats
            </li>
          </ul>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-side w-100 d-flex flex-column align-items-center rounded pt-3 px-3">
        <!-- Assistants Tab -->
        <div v-if="activeTab === 'assistants'" class="assistants-tab w-100">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h3 class="text-white mb-0">Data Science</h3>
              <span class="text-white small">(ID: 67437)</span>
            </div>

            <!-- Sub-tabs for Assistant Modes -->
            <div class="rounded">
              <ul class="tabs-list list-unstyled text-white d-flex flex-row m-0">
                <li
                  :class="{
                    'tab-item-active': activeAssistantMode === 'General',
                    'tab-item-inactive': activeAssistantMode !== 'General'
                  }"
                  class="tab-item cursor-pointer tab-left-rounded px-4 py-2"
                  @click="activeAssistantMode = 'General'"
                >
                  General
                </li>
                <li
                  :class="{
                    'tab-item-active': activeAssistantMode === 'Quiz',
                    'tab-item-inactive': activeAssistantMode !== 'Quiz'
                  }"
                  class="tab-item cursor-pointer tab-middle px-4 py-2"
                  @click="activeAssistantMode = 'Quiz'"
                >
                  Quiz
                </li>
                <li
                  :class="{
                    'tab-item-active': activeAssistantMode === 'Exam',
                    'tab-item-inactive': activeAssistantMode !== 'Exam'
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
          <div v-if="activeModeIndex !== -1" class="p-3 rounded">
            <div class="d-flex align-items-center justify-content-between mb-2 text-white">
              <u
                ><strong>{{ assistantModes[activeModeIndex].name }} Assistant</strong></u
              >
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
              <label class="form-check-label text-white" :for="assistantModes[activeModeIndex].name + '-moodleSwitch'">
                Enable Moodle Tool
              </label>
            </div>
            <!-- File Upload -->
            <div class="mb-2 cursor-pointer">
              <label class="text-white mb-1">Upload Files:</label>

            <!-- From Uiverse.io by csemszepp -->
            <label
              for="file"
              class="costume-file-upload"
              @dragover.prevent="handleDragOver"
              @dragleave="handleDragLeave"
              @drop.prevent="handleFileDrop"
              :class="{ 'drag-over': isDragging }"
            >
              <div class="icon">
                <template v-if="!isDragging">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#4e4e4e">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                      <path
                        d="M13 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.0799 5 6.2V17.8C5 18.9201 5 19.4802 5.21799 19.908C5.40973 20.2843 5.71569 20.5903 6.09202 20.782C6.51984 21 7.0799 21 8.2 21H12M13 3L19 9M13 3V7.4C13 7.96005 13 8.24008 13.109 8.45399C13.2049 8.64215 13.3578 8.79513 13.546 8.89101C13.7599 9 14.0399 9 14.6 9H19M19 9V12M17 19H21M19 17V21"
                        stroke="#4e4e4e"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </g>
                  </svg>
                </template>
                <template v-else>
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#4e4e4e">
                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                    <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                    <g id="SVGRepo_iconCarrier">
                      <path
                        d="M15 19L17 21L21 17M13 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.0799 5 6.2V17.8C5 18.9201 5 19.4802 5.21799 19.908C5.40973 20.2843 5.71569 20.5903 6.09202 20.782C6.51984 21 7.0799 21 8.2 21H12M13 3L19 9M13 3V7.4C13 7.96005 13 8.24008 13.109 8.45399C13.2049 8.64215 13.3578 8.79513 13.546 8.89101C13.7599 9 14.0399 9 14.6 9H19M19 9V13.5"
                        stroke="#4caf50"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      ></path>
                    </g>
                  </svg>
                </template>
              </div>
              <div class="text">
                <span>Drag to upload file</span>
              </div>
              <input
                id="file"
                type="file"
                multiple
                accept="
      .c, .cpp, .cs, .css, .doc, .docx, .go, .html, .java, .js, .json, .md, .pdf, .php, .pptx, .py, .rb, .sh, .tex, .ts, .txt,
      text/x-c, text/x-c++, text/x-csharp, text/css, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, 
      text/x-golang, text/html, text/x-java, text/javascript, application/json, text/markdown, application/pdf, 
      text/x-php, application/vnd.openxmlformats-officedocument.presentationml.presentation, text/x-python, text/x-script.python, 
      text/x-ruby, application/x-sh, text/x-tex, application/typescript, text/plain
    "
                @change="(e) => onFilesSelected(e, activeModeIndex)"
              />
            </label>

            </div>

            <ul class="file mt-2 text-white">
              <li
                v-for="(file, fileIndex) in assistantModes[activeModeIndex].files"
                :key="file.name"
                class="d-flex justify-content-between pt-1 pb-1 align-items-center"
              >
                <span>{{ file.name }} ({{ formatFileSize(file.size) }})</span>
                <font-awesome-icon
                  class="text-danger fa-lg cursor-pointer"
                  :icon="['fas', 'square-xmark']"
                  @click="removeFile(activeModeIndex, fileIndex)"
                />
              </li>
            </ul>
            <!-- Lecture Links -->
            <div class="mb-2">
              <label class="text-white mb-1">Lecture Links:</label>
              <div class="d-flex">
                <input type="text" v-model="newLectureLink" placeholder="Enter lecture link" class="w-100" />
                <button class="btn btn-primary ms-2" @click="addLectureLink">Add</button>
              </div>
              <div class="mt-2">
                <div v-for="(link, index) in lectureLinks" :key="index" class="lecture-link">
                  {{ link }}
                  <button class="btn btn-danger btn-sm ms-2" @click="removeLectureLink(index)">Remove</button>
                </div>
              </div>
              <button class="btn btn-action mt-3" @click="transcribeLecture">Transcribe Lecture</button>
              <button class="btn btn-secondary mt-3" @click="transcribeLecture">Edit transcriptions</button>
            </div>
            <!-- Instructions Field -->
            <div class="mb-2">
              <label class="text-white mb-1">Instructions:</label>
              <textarea
                v-model="assistantModes[activeModeIndex].instructions"
                placeholder="Enter instructions for this assistant"
                class="w-100"
              ></textarea>
            </div>

            <!-- Progress Bar -->
            <div v-if="transcribing" class="my-2 w-100">
              <div class="progress">
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  :style="{ width: transcribeProgress + '%' }"
                >
                  {{ transcribeProgress }}%
                </div>
              </div>
            </div>

            <!-- Display transcribed text -->
            <div v-if="transcribedText" class="mt-3 text-white">
              <h5>Transcribed Lecture:</h5>
              <p>{{ transcribedText }}</p>
            </div>
          </div>
          <button class="btn btn-action w-100 mt-3" @click="saveAssistants">Save Assistants</button>
        </div>

        <!-- Usage Tab -->
        <div v-else-if="activeTab === 'usage'" class="usage-tab w-100 mt-3">
          <h3 class="text-white">Usage</h3>
          <p class="text-white">Display usage analytics and student activity data here.</p>
        </div>

        <!-- Stats Tab -->
        <div v-else-if="activeTab === 'stats'" class="stats-tab w-100 mt-3">
          <h3 class="text-white">Stats</h3>
          <p class="text-white">Show charts, graphs, and detailed statistics here.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMagnifyingGlass, faHome, faPenToSquare, faSquareXmark } from '@fortawesome/free-solid-svg-icons'
import Profilemenu from '../widgets/Profilemenu.vue'
import axios from 'axios'

library.add(faMagnifyingGlass, faHome, faPenToSquare, faSquareXmark)

const router = useRouter()

const searchQuery = ref('')
const isSearchFocused = ref(false)
const searchInput = ref<HTMLInputElement | null>(null)
function focusInput() {
  searchInput.value?.focus()
}

// Sidebar Tabs
const activeTab = ref<'assistants' | 'usage' | 'stats'>('assistants')

// Dummy course data (replace with actual fetch logic if needed)
const course = ref({
  courseName: 'Sample Course'
})

// Assistant Modes Configuration
type AssistantStatus = 'Active' | 'Inactive' | 'Activating'
interface AssistantMode {
  name: 'General' | 'Quiz' | 'Exam'
  status: AssistantStatus
  moodleEnabled: boolean
  files: File[]
  links: string
  instructions: string
}
const assistantModes = ref<AssistantMode[]>([
  {
    name: 'General',
    status: 'Active',
    moodleEnabled: false,
    files: [],
    links: '',
    instructions: `You are an AI tutor specializing in Data Science. Your role is to assist students by providing clear, structured explanations, code examples, and step-by-step guidance on various Data Science topics. You should:
- Explain concepts in an easy-to-understand manner, adapting to the student's level (beginner, intermediate, advanced).
- Provide Python code snippets with explanations for data analysis, machine learning, and visualization.
- Assist with assignments and projects by guiding (but not solving) problems, encouraging critical thinking.
- Offer best practices for coding, debugging, and optimizing data science workflows.
- Use real-world examples, datasets, and case studies to enhance learning.
- Stay engaging, interactive, and patient, ensuring students grasp the material fully.
- If needed, break down complex concepts into simpler subtopics, using analogies or visuals where helpful.
- Encourage students to experiment, ask questions, and apply concepts through coding exercises.

Always ensure explanations are accurate, up-to-date, and aligned with industry standards.
`
  },
  {
    name: 'Quiz',
    status: 'Inactive',
    moodleEnabled: false,
    files: [],
    links: '',
    instructions: ''
  },
  {
    name: 'Exam',
    status: 'Activating',
    moodleEnabled: false,
    files: [],
    links: '',
    instructions: ''
  }
])

// Active Assistant Mode Sub-tab
const activeAssistantMode = ref<'General' | 'Quiz' | 'Exam'>('General')
const activeModeIndex = computed(() =>
  assistantModes.value.findIndex((mode) => mode.name === activeAssistantMode.value)
)

function getAssistantStatusClass(status: AssistantStatus) {
  switch (status) {
    case 'Active':
      return 'text-success'
    case 'Activating':
      return 'text-info'
    case 'Inactive':
      return 'text-danger'
    default:
      return 'text-muted'
  }
}

function onFilesSelected(event: Event, index: number) {
  const input = event.target as HTMLInputElement
  if (input.files) {
    const selectedFiles = Array.from(input.files)
    const existingFiles = assistantModes.value[index].files.map((file) => file.name)
    const newFiles = selectedFiles.filter((file) => !existingFiles.includes(file.name))
    assistantModes.value[index].files = [...assistantModes.value[index].files, ...newFiles]
  }
}

const isDragging = ref(false)

function handleDragOver(event) {
  event.preventDefault() // Prevent default browser behavior
  isDragging.value = true // Set dragging state
}

function handleDragLeave(event) {
  isDragging.value = false // Remove dragging state
}

function handleFileDrop(event: DragEvent) {
  isDragging.value = false // Remove dragging state

  const files = event.dataTransfer?.files
  if (files) {
    const selectedFiles = Array.from(files)
    const existingFiles = assistantModes.value[activeModeIndex.value].files.map((file) => file.name)
    const newFiles = selectedFiles.filter((file) => !existingFiles.includes(file.name))
    assistantModes.value[activeModeIndex.value].files = [
      ...assistantModes.value[activeModeIndex.value].files,
      ...newFiles
    ]
  }
}

function removeFile(index: number, fileIndex: number) {
  assistantModes.value[index].files.splice(fileIndex, 1)
}

function formatFileSize(size: number) {
  const i = Math.floor(Math.log(size) / Math.log(1024))
  return parseFloat((size / Math.pow(1024, i)).toFixed(2)) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i]
}

function saveAssistants() {
  console.log('Assistant Modes Configuration:', assistantModes.value)
  alert('Assistants configuration saved!')
  // Place your API call or further navigation logic here.
}

// Profile Menu and Navbar handlers
const isProfileMenuVisible = ref(false)
function toggleProfileMenu() {
  isProfileMenuVisible.value = !isProfileMenuVisible.value
}
function handleHomeClick() {
  router.push('/')
}

// Transcription related data and methods
const transcribing = ref(false)
const transcribeProgress = ref(0)
const transcribedText = ref('')
const newLectureLink = ref('')
const lectureLinks = ref<string[]>([])

function addLectureLink() {
  if (newLectureLink.value) {
    lectureLinks.value.push(newLectureLink.value)
    newLectureLink.value = ''
  }
}

function removeLectureLink(index: number) {
  lectureLinks.value.splice(index, 1)
}

async function transcribeLecture() {
  if (lectureLinks.value.length === 0) {
    return alert('Please add at least one lecture link.')
  }

  try {
    transcribing.value = true
    transcribeProgress.value = 25 // Example progress update

    const response = await axios.post('http://localhost:8000/api/transcribe_lecture', {
      lecture_url: lectureLinks.value.join(',')
    })

    transcribedText.value = response.data.transcribed_text
    transcribeProgress.value = 100 // Done
  } catch (error) {
    console.error(error)
    alert('Transcription failed')
  } finally {
    transcribing.value = false
  }
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
  min-width: 225px;
  max-width: 225px;
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

/* Remove line on hover; show only on selected items */
.list-item-hover {
  position: relative;
  list-style-type: none;
  transition: background-color 0.5s ease, color 0.5s ease;
  padding-left: 0.8em !important;
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
  transition: width 0.5s ease, opacity 0.5s ease;
  opacity: 0;
}

/* Sidebar item when selected */
.selected-sidebar-item {
  background-color: var(--color-gray-medium);
  position: relative;
  overflow: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}
.selected-sidebar-item::before {
  width: 5px;
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

/* Example of a selected course approach */
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

.assistant-config-panel .file {
  list-style-type: disc;
  padding-left: 20px;
}

.assistant-config-panel .file li {
  list-style-position: inside;
}

.progress {
  height: 1.5rem;
}

.progress-bar {
  background-color: green;
}

input,
textarea {
  background-color: var(--color-gray-medium);
  color: var(--color-white);
  padding: 0.5rem;
  padding-left: 1rem;
  border: 1px solid var(--color-gray-light);
  border-radius: 6px;
}

input:focus,
textarea:focus {
  outline: none;
}

input::placeholder,
textarea::placeholder {
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.2s ease;
}

.lecture-link {
  background-color: var(--color-gray-medium);
  color: var(--color-white);
  padding: 0.5rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* From Uiverse.io by csemszepp */
.costume-file-upload {
  height: 120px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: space-between;
  gap: 10px;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--color-gray-light);
  background-color: var(--color-gray-medium);
  padding: 1.5rem;
  border-radius: 10px;
}

.costume-file-upload:hover,
.costume-file-upload.drag-over {
  border-color: var(--color-gray-shadow);
}

.costume-file-upload .icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.costume-file-upload .icon svg {
  height: 50px;
}

.costume-file-upload .text {
  display: flex;
  align-items: center;
  justify-content: center;
}

.costume-file-upload .text span {
  font-weight: 400;
  color: #e8e8e8;
}

.costume-file-upload input {
  display: none;
}

</style>
