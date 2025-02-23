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
      <div class="right-side w-100 rounded pt-3 px-3">
        <!-- Assistants Tab -->
        <div class="non-scrollable-header w-100">
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
          </div>
          <!-- Configuration Panel for the Selected Assistant Mode -->
          <div class="scrollable-content">
            <div v-if="activeModeIndex !== -1" class="p-3 rounded">
              <div class="d-flex align-items-center justify-content-between mb-2 text-white">
                <h5>{{ assistantModes[activeModeIndex].name }} Assistant</h5>

                <span :class="getAssistantStatusClass(assistantModes[activeModeIndex].status)">
                  {{ assistantModes[activeModeIndex].status }}
                </span>
              </div>
              <!-- Moodle Toggle -->
              <div class="form-check form-switch mb-2">
                <input
                  class="form-check-input cursor-pointer"
                  type="checkbox"
                  v-model="assistantModes[activeModeIndex].moodleEnabled"
                  :id="assistantModes[activeModeIndex].name + '-moodleSwitch'"
                />
                <label
                  class="form-check-label text-white cursor-pointer"
                  :for="assistantModes[activeModeIndex].name + '-moodleSwitch'"
                >
                  Enable Moodle Tool
                </label>
              </div>
              <!-- File Upload -->
              <div class="mb-2 cursor-pointer">
                <label class="text-white mb-1">Upload Files:</label>
                <label
                  for="file"
                  class="costume-file-upload"
                  @dragover.prevent="handleDragOver"
                  @dragleave="handleDragLeave"
                  @drop.prevent="handleFileDrop"
                  :class="{ 'drag-over': isDragging }"
                >
                  <div class="icon">
                    <!-- Default state: No dragging -->
                    <template v-if="!isDropped">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#4e4e4e">
                        <path
                          d="M13 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.0799 5 6.2V17.8C5 18.9201 5 19.4802 5.21799 19.908C5.40973 20.2843 5.71569 20.5903 6.09202 20.782C6.51984 21 7.0799 21 8.2 21H12M13 3L19 9M13 3V7.4C13 7.96005 13 8.24008 13.109 8.45399C13.2049 8.64215 13.3578 8.79513 13.546 8.89101C13.7599 9 14.0399 9 14.6 9H19M19 9V12M17 19H21M19 17V21"
                          stroke="#4e4e4e"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        ></path>
                      </svg>
                    </template>

                    <!-- Dragging with valid file format -->
                    <template v-else-if="isDragValid">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#4caf50">
                        <path
                          d="M15 19L17 21L21 17M13 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.0799 5 6.2V17.8C5 18.9201 5 19.4802 5.21799 19.908C5.40973 20.2843 5.71569 20.5903 6.09202 20.782C6.51984 21 7.0799 21 8.2 21H12M13 3L19 9M13 3V7.4C13 7.96005 13 8.24008 13.109 8.45399C13.2049 8.64215 13.3578 8.79513 13.546 8.89101C13.7599 9 14.0399 9 14.6 9H19M19 9V13.5"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        ></path>
                      </svg>
                    </template>

                    <!-- Dragging with invalid file format -->
                    <template v-else>
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#aa1b25">
                        <path
                          d="M17 17L21 21M21 17L17 21M13 3H8.2C7.0799 3 6.51984 3 6.09202 3.21799C5.71569 3.40973 5.40973 3.71569 5.21799 4.09202C5 4.51984 5 5.0799 5 6.2V17.8C5 18.9201 5 19.4802 5.21799 19.908C5.40973 20.2843 5.71569 20.5903 6.09202 20.782C6.51984 21 7.0799 21 8.2 21H13M13 3L19 9M13 3V7.4C13 7.96005 13 8.24008 13.109 8.45399C13.2049 8.64215 13.3578 8.79513 13.546 8.89101C13.7599 9 14.0399 9 14.6 9H19M19 9V14"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        ></path>
                      </svg>
                    </template>
                  </div>

                  <div class="text">
                    <span>{{ dragText }}</span>
                  </div>
                  <input id="file" type="file" multiple :accept="computedAccept" @change="onFilesSelected" />
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
                  <div
                    v-for="(link, index) in lectureLinks"
                    :key="index"
                    class="lecture-link d-flex align-items-center"
                  >
                    <span
                      class="mode-badge shortened-link"
                      :class="{
                        'text-info': link.status === 'transcribing',
                        'text-success': link.status === 'completed',
                        'text-danger': link.status === 'failed'
                      }"
                    >
                      {{ shortenLink(link.url) }}
                      <span class="mode-tooltip">
                        <a :href="link.url" target="_blank" rel="noopener noreferrer">
                          {{ shortenLink(link.url, 60) }}
                        </a>
                      </span>
                    </span>
                    <v-progress-linear
                      v-if="link.transcribing"
                      :model-value="link.progress"
                      color="light-green-darken-4"
                      height="10"
                      striped
                      class="ms-2"
                      style="width: 200px"
                    />
                    <div class="d-flex align-items-center">
                      <font-awesome-icon class="fa-lg" :icon="['fas', 'pen-to-square']" />
                      <button class="btn btn-danger btn-sm ms-2" @click="removeLectureLink(index)">Remove</button>
                    </div>
                  </div>
                </div>
                <button class="btn btn-action mt-3" @click="transcribeAllLectures">Transcribe Lectures</button>
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
              <!-- Display transcribed text -->
              <div v-if="transcribedText" class="mt-3 text-white">
                <h5>Transcribed Lecture:</h5>
                <p>{{ transcribedText }}</p>
              </div>
            </div>
            <button class="btn btn-action w-100 mt-3" @click="saveAssistants">Save Assistants</button>
          </div>
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
    moodleEnabled: true,
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

function onFilesSelected(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files) {
    const selectedFiles = Array.from(input.files)
    // Use activeModeIndex to know which mode to update.
    const index = activeModeIndex.value
    const existingFiles = assistantModes.value[index].files.map((file) => file.name)
    const newFiles = selectedFiles.filter((file) => !existingFiles.includes(file.name))
    assistantModes.value[index].files = [...assistantModes.value[index].files, ...newFiles]
  }
}

const acceptedExtensions = [
  '.c',
  '.cpp',
  '.cs',
  '.css',
  '.doc',
  '.docx',
  '.go',
  '.html',
  '.java',
  '.js',
  '.json',
  '.md',
  '.pdf',
  '.php',
  '.pptx',
  '.py',
  '.rb',
  '.sh',
  '.tex',
  '.ts',
  '.txt'
]

const acceptedMimeTypes = [
  'text/x-c',
  'text/x-c++',
  'text/x-csharp',
  'text/css',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/x-golang',
  'text/html',
  'text/x-java',
  'text/javascript',
  'application/json',
  'text/markdown',
  'application/pdf',
  'text/x-php',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  'text/x-python',
  'text/x-script.python',
  'text/x-ruby',
  'application/x-sh',
  'text/x-tex',
  'application/typescript',
  'text/plain'
]

const computedAccept = computed(() => [...acceptedExtensions, ...acceptedMimeTypes].join(', '))

const isDragging = ref(false)
const isDropped = ref(false)
const isDragValid = ref(false)
const isFileInvalid = ref(false)
const dragText = computed(() => {
  if (!isDropped.value) {
    return 'Drop file to upload'
  }
  if (isFileInvalid.value) {
    return 'Invalid file type'
  }
  return 'Valid file type'
})

function handleDragOver(event) {
  event.preventDefault() // Prevent default browser behavior
  isDragging.value = true // Set dragging state
  isDragValid.value = true // Reset drag validity
}

function handleDragLeave(event) {
  isDragging.value = false
  isDragValid.value = false // Reset drag validity
}

function handleFileDrop(event: DragEvent) {
  event.preventDefault() // Prevent default browser behavior
  isDragging.value = false
  isDropped.value = true

  const files = event.dataTransfer?.files
  if (files) {
    // Filter the files to only include accepted types
    const selectedFiles = Array.from(files).filter((file) => {
      const fileExt = '.' + file.name.split('.').pop()?.toLowerCase() // Get file extension
      return acceptedExtensions.includes(fileExt) || acceptedMimeTypes.includes(file.type)
    })

    // Check if any of the dropped files are invalid
    const hasInvalidFiles = Array.from(files).some((file) => {
      const fileExt = '.' + file.name.split('.').pop()?.toLowerCase() // Get file extension
      return !acceptedExtensions.includes(fileExt) && !acceptedMimeTypes.includes(file.type)
    })

    // Set isDragValid based on whether any invalid files were dropped
    isDragValid.value = !hasInvalidFiles
    isFileInvalid.value = hasInvalidFiles
    isDragging.value = true

    // Reset drag state after 1 second
    setTimeout(() => {
      isDragging.value = false
      isDragValid.value = false
      isFileInvalid.value = false
      isDropped.value = false
    }, 1000)

    // Add new files to the existing files list (if they don't already exist)
    const existingFiles = assistantModes.value[activeModeIndex.value].files.map((file) => file.name)
    const newFiles = selectedFiles.filter((file) => !existingFiles.includes(file.name))

    assistantModes.value[activeModeIndex.value].files = [
      ...assistantModes.value[activeModeIndex.value].files,
      ...newFiles
    ]
  } else {
    isDragValid.value = false
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
const lectureLinks = ref<LectureLinkItem[]>([]) // Instead of a plain string[]
const urlPattern = new RegExp('^(https?:\\/\\/)', 'i')

interface LectureLinkItem {
  url: string
  progress: number
  transcribing: boolean
  transcribedText: string
  status?: 'failed' | 'completed' | 'transcribing' | 'pending'
}

// Updated addLectureLink to push link objects
function addLectureLink() {
  if (!urlPattern.test(newLectureLink.value)) {
    alert('Please enter a valid URL (including http:// or https://).')
    return
  }
  if (lectureLinks.value.some((link) => link.url === newLectureLink.value)) {
    alert('This link is already added.')
    return
  }
  lectureLinks.value.push({
    url: newLectureLink.value,
    progress: 0,
    transcribing: false,
    transcribedText: '',
    status: 'pending' // Added default status
  })
  newLectureLink.value = ''
}

// Remove link object
function removeLectureLink(index: number) {
  lectureLinks.value.splice(index, 1)
}

// Transcribe all links in sequence
async function transcribeAllLectures() {
  if (lectureLinks.value.length === 0) {
    return alert('Please add at least one lecture link.')
  }

  for (const link of lectureLinks.value) {
    // Skip already completed lectures
    if (link.status === 'completed') continue

    link.transcribing = true
    link.status = 'transcribing'
    link.progress = 0
    const updateInterval = Math.floor(Math.random() * 500) + 500

    const intervalId = window.setInterval(() => {
      if (link.progress < 99) {
        const increment = Math.random() * 0.4 + 0.9
        link.progress = Math.min(link.progress + increment, 99)
      }
    }, updateInterval)

    try {
      const response = await axios.post('http://localhost:8000/api/transcribe_lecture', { lecture_url: link.url })
      link.transcribedText = response.data.transcribed_text

      await new Promise((resolve) => {
        const finalInterval = window.setInterval(() => {
          if (link.progress < 100) {
            const finalIncrement = Math.random() * 1.8 + 2.5
            link.progress = Math.min(link.progress + finalIncrement, 100)
          } else {
            clearInterval(finalInterval)
            resolve(null)
          }
        }, 300)
      })
      link.status = 'completed'
    } catch (error) {
      console.error(error)
      link.status = 'failed'
      alert(`Sorry, we could not transcribe the lecture at ${link.url}. Please check the link or try again later.`)
    } finally {
      link.transcribing = false
      clearInterval(intervalId)
    }
  }
}

function shortenLink(link: string, maxLength = 50) {
  return link.length > maxLength ? link.slice(0, maxLength) + '...' : link
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

.form-check-input:checked {
  background-color: var(--color-gray-lighter);
  border-color: var(--color-white);
}

.form-check-input:checked::before {
  background-color: black;
  border-color: black;
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
  height: calc(100vh - 60px);
  overflow: auto; /* Prevent entire right-side from scrolling */
}

.non-scrollable-header {
}

.scrollable-content {
  overflow-y: auto;
  padding-bottom: 1rem; /* Add spacing at bottom */
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

.file {
  list-style-type: disc !important;
  list-style-position: inside;
  padding-left: 20px;
}

.file li {
  list-style-type: disc !important;
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

.shortened-link {
  color: #fff;
  padding: 0.4em 0.65em;
  margin-right: 0.25rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: bold;
  position: relative;
  cursor: pointer;
  background-color: var(--color-gray-medium);
}

.shortened-link .mode-tooltip {
  display: none;
  position: absolute;
  bottom: calc(100%);
  left: 100%;
  transform: translateX(-55%);
  background-color: var(--color-gray-light);
  color: #fff;
  padding: 0.4em 0.6em;
  border-radius: 4px;
  font-size: 0.65rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.shortened-link .mode-tooltip a {
  color: #fff;
}

.shortened-link .mode-tooltip::after {
  content: '';
  position: absolute;
  bottom: -11px;
  /* Move the arrow near the tooltip’s start or middle, adjust as preferred */
  left: 15%;
  transform: translateX(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: var(--color-gray-light) transparent transparent transparent;
}

.shortened-link:hover .mode-tooltip {
  display: block;
  animation: fadeIn 0.3s forwards;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
