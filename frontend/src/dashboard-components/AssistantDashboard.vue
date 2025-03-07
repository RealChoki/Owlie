<template>
  <div class="w-100 px-1">
    <div class="w-100 test-container">
      <div class="non-scrollable-header pt-3">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h3 class="text-white mb-0">DataScience</h3>
            <span class="text-white small">(ID: 696969)</span>
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
      </div>
    </div>
    <!-- Configuration Panel for the Selected Assistant Mode -->
    <div class="content-below-header mb-4">
      <div v-if="activeModeIndex !== -1" class="p-3 rounded">
        <div class="d-flex align-items-center justify-content-between mb-2 text-white">
          <h5>{{ assistantModes[activeModeIndex].name }} Assistant</h5>

          <span :class="getAssistantStatusClass(assistantModes[activeModeIndex].status)">
            {{ assistantModes[activeModeIndex].status }}
          </span>
        </div>

        <div v-if="activeAssistantMode === 'General' || activeAssistantMode === 'Quiz'">
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
              style="user-select: none"
              :for="assistantModes[activeModeIndex].name + '-moodleSwitch'"
            >
              Enable Moodle Tool
            </label>
            <font-awesome-icon
              :icon="['fas', 'circle-info']"
              class="circle-info cursor-pointer text-light ms-1 small"
              @click="toggleModal('infoMoodleModal')"
            />
          </div>
          <!-- File Upload -->
          <div class="mb-2 cursor-pointer">
            <label for="file" class="text-white mb-1">Upload Files:</label>
            <font-awesome-icon
              :icon="['fas', 'circle-info']"
              class="circle-info cursor-pointer text-light ms-1 small"
              @click="toggleModal('infoFilesModal')"
            />
            <label
              for="file"
              class="custom-file-upload"
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
              class="d-flex ps-2 pt-1 pb-1 align-items-center file-hover"
            >
              <font-awesome-icon
                class="text-danger fa-lg cursor-pointer pe-3"
                :icon="['fas', 'square-xmark']"
                @click="removeFile(activeModeIndex, fileIndex)"
              />
              <span>{{ file.name }} ({{ formatFileSize(file.size) }})</span>
            </li>
          </ul>
          <!-- Lecture Links -->
          <div class="mb-2">
            <label for="lecture-links" class="text-white mb-1">Lecture Links:</label>
            <div class="d-flex">
              <input
                id="lecture-links"
                type="text"
                v-model="newLectureLink"
                placeholder="Enter lecture link"
                class="w-100"
                @keyup.enter="addLectureLink"
                style="border-top-right-radius: 0; border-bottom-right-radius: 0"
              />
              <button
                class="btn btn-outline-primary"
                @click="addLectureLink"
                style="border-top-left-radius: 0; border-bottom-left-radius: 0"
              >
                <font-awesome-icon :icon="['fas', 'plus']" />
              </button>
            </div>
            <div class="mt-2">
              <div
                v-for="(link, index) in assistantModes[activeModeIndex].links"
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
                      {{ shortenLink(link.url, 75) }}
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
                  style="width: 250px"
                />
                <div class="d-flex align-items-center">
                  <font-awesome-icon
                    v-if="link.status === 'completed'"
                    @click="toggleTranscriptionModal(link)"
                    class="fa-lg cursor-pointer"
                    :icon="['fas', 'pen-to-square']"
                  />
                  <button class="btn btn-danger btn-sm ms-2" @click="removeLectureLink(index)">
                    <font-awesome-icon :icon="['fas', 'trash']" />
                  </button>
                </div>
              </div>
            </div>
            <button
              v-if="assistantModes[activeModeIndex].links.length"
              class="btn-primary btn mb-2"
              @click="transcribeAllLectures"
            >
            Transcribe Videos
            <font-awesome-icon :icon="['fas', 'closed-captioning']" />
            </button>
          </div>
          <!-- Instructions Field -->
          <div class="mb-2">
            <label for="instructions" class="text-white mb-1">Instructions:</label>
            <textarea
              id="instructions"
              v-model="assistantModes[activeModeIndex].instructions"
              placeholder="Assistant instructions"
              class="w-100"
            ></textarea>
          </div>
          <!-- Display transcribed text -->
          <div v-if="transcribedText" class="mt-3 text-white">
            <h5>Transcribed Lecture:</h5>
            <p>{{ transcribedText }}</p>
          </div>
        </div>

        <div v-else>
          <div class="mb-2 cursor-pointer">
            <label for="file" class="text-white mb-1">Upload Mock Exam:</label>
            <font-awesome-icon
              :icon="['fas', 'circle-info']"
              class="circle-info cursor-pointer text-light ms-1 small"
              @click="toggleInfoFiles"
            />
            <label
              for="file"
              class="custom-file-upload"
              style="min-height: 20vh"
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
              class="d-flex ps-2 pt-1 pb-1 align-items-center file-hover"
            >
              <font-awesome-icon
                class="text-danger fa-lg cursor-pointer"
                :icon="['fas', 'square-xmark']"
                @click="removeFile(activeModeIndex, fileIndex)"
              />
              <span>{{ file.name }} ({{ formatFileSize(file.size) }})</span>
            </li>
          </ul>
          <div class="mb-2">
            <label for="instructions" class="text-white mb-1">Instructions:</label>
            <textarea
              id="instructions"
              v-model="assistantModes[activeModeIndex].instructions"
              placeholder="Assistant instructions"
              class="w-100"
            ></textarea>
          </div>
        </div>
        <div class="d-flex save-btns">
          <button
            v-if="assistantModes[activeModeIndex].status !== 'Activating'"
            @click="toggleAssistantModeStatus"
            :class="[
              'btn',
              'cursor-pointer',
              'me-2',
              'text-white',
              assistantModes[activeModeIndex].status === 'Active' ? 'border-danger' : 'border-success',
              assistantModes[activeModeIndex].status === 'Active' ? 'hover:bg-danger' : 'hover:bg-success'
            ]"
          >
            {{ assistantModes[activeModeIndex].status === 'Active' ? 'Deactivate' : 'Activate' }}
          </button>

          <button class="btn-primary btn save-assistant-btn py-2" @click="saveAssistant">
            Save Assistant
            <font-awesome-icon :icon="['fas', 'cloud-arrow-up']" />
          </button>
        </div>
      </div>
    </div>
  </div>

  <InfoMoodleModal />
  <InfoFilesModal :acceptedExtensions="acceptedExtensions" :acceptedMimeTypes="acceptedMimeTypes" />
  <TranscriptionModal :link="selectedLink" />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as bootstrap from 'bootstrap'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faPenToSquare,
  faSquareXmark,
  faXmark,
  faTrash,
  faCircleInfo,
  faPlus,
  faCloudArrowUp,
  faClosedCaptioning
} from '@fortawesome/free-solid-svg-icons'
import axios from 'axios'
import InfoMoodleModal from './assistant-dashboard-components/InfoMoodleModal.vue'
import InfoFilesModal from './assistant-dashboard-components/InfoFilesModal.vue'
import TranscriptionModal from './assistant-dashboard-components/TranscriptionModal.vue'

library.add(faPenToSquare, faSquareXmark, faXmark, faTrash, faCircleInfo, faPlus, faCloudArrowUp, faClosedCaptioning)

// Assistant Modes Configuration
// ---------------------------------
// 1. Types & Interfaces
// ---------------------------------
type AssistantStatus = 'Active' | 'Inactive' | 'Activating'

interface AssistantMode {
  name: 'General' | 'Quiz' | 'Exam'
  status: AssistantStatus
  moodleEnabled: boolean
  files: File[]
  links: LectureLinkItem[]
  instructions: string
}

interface LectureLinkItem {
  url: string
  progress: number
  transcribing: boolean
  transcribedText: string
  status?: 'failed' | 'completed' | 'transcribing' | 'pending'
}

// ---------------------------------
// 2. Assistant Modes Management
// ---------------------------------
const sharedAssistantFiles = ref<any[]>([])
const sharedAssistantLinks = ref<any[]>([])

const assistantModes = ref<AssistantMode[]>([
  {
    name: 'General',
    status: 'Active',
    moodleEnabled: true,
    files: sharedAssistantFiles.value,
    links: sharedAssistantLinks.value,
    instructions: ''
  },
  {
    name: 'Quiz',
    status: 'Inactive',
    moodleEnabled: false,
    files: sharedAssistantFiles.value,
    links: sharedAssistantLinks.value,
    instructions: ''
  },
  { name: 'Exam', status: 'Activating', moodleEnabled: false, files: [], links: [], instructions: '' }
])

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

function toggleAssistantModeStatus() {
  const currentMode = assistantModes.value[activeModeIndex.value]

  // Toggle the status between 'Active' and 'Inactive'
  if (currentMode.status === 'Active') {
    currentMode.status = 'Inactive'
  } else {
    currentMode.status = 'Active'
  }
}

const saveAssistant = async () => {
  const index = activeModeIndex.value
  const payload = {
    assistant_mode: activeAssistantMode.value,
    instructions: assistantModes.value[index].instructions,
    transcribed_text: transcribedText.value,
    files: assistantModes.value[index].files.map((file) => file.name)
  }
  try {
    const response = await axios.post('http://localhost:8000/api/assistants/create', payload)
    console.log('Assistant created:', response.data)
    alert('Assistant created successfully!')
  } catch (error) {
    console.error('Failed to save assistant', error)
    alert('Failed to create assistant')
  }
}

// ---------------------------------
// 3. File Handling (Upload & Drag-Drop)
// ---------------------------------
const isDragging = ref(false)
const isDropped = ref(false)
const isDragValid = ref(false)
const isFileInvalid = ref(false)

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

const dragText = computed(() => {
  if (!isDropped.value) return 'Drop file to upload'
  return isFileInvalid.value ? 'Invalid file type' : 'Valid file type'
})

function handleDragOver(event: DragEvent) {
  event.preventDefault()
  isDragging.value = true
  isDragValid.value = true
}

function handleDragLeave() {
  isDragging.value = false
  isDragValid.value = false
}

function handleFileDrop(event: DragEvent) {
  event.preventDefault()
  isDragging.value = false
  isDropped.value = true

  const files = event.dataTransfer?.files
  if (files) {
    const selectedFiles = Array.from(files).filter((file) => {
      const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
      return acceptedExtensions.includes(fileExt) || acceptedMimeTypes.includes(file.type)
    })

    const hasInvalidFiles = Array.from(files).some((file) => {
      const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
      return !acceptedExtensions.includes(fileExt) && !acceptedMimeTypes.includes(file.type)
    })

    isDragValid.value = !hasInvalidFiles
    isFileInvalid.value = hasInvalidFiles

    setTimeout(() => {
      isDragging.value = isDragValid.value = isFileInvalid.value = isDropped.value = false
    }, 1000)

    const existingFiles = assistantModes.value[activeModeIndex.value].files.map((file) => file.name)
    const newFiles = selectedFiles.filter((file) => !existingFiles.includes(file.name))
    assistantModes.value[activeModeIndex.value].files.push(...newFiles)
  } else {
    isDragValid.value = false
  }
}

function onFilesSelected(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files) {
    const selectedFiles = Array.from(input.files)
    const index = activeModeIndex.value
    const existingFiles = assistantModes.value[index].files.map((file) => file.name)
    const newFiles = selectedFiles.filter((file) => !existingFiles.includes(file.name))
    assistantModes.value[index].files.push(...newFiles)
  }
}

function removeFile(index: number, fileIndex: number) {
  assistantModes.value[index].files.splice(fileIndex, 1)
}

function formatFileSize(size: number) {
  const i = Math.floor(Math.log(size) / Math.log(1024))
  return parseFloat((size / Math.pow(1024, i)).toFixed(2)) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i]
}

// ---------------------------------
// 4. Lecture Link Handling (Transcription)
// ---------------------------------
const transcribing = ref(false)
const transcribeProgress = ref(0)
const transcribedText = ref('')
const newLectureLink = ref('')

const urlPattern = new RegExp('^(https?:\\/\\/)', 'i')

function addLectureLink() {
  if (!urlPattern.test(newLectureLink.value)) {
    return alert('Invalid URL format.')
  }

  const activeMode = assistantModes.value[activeModeIndex.value]

  if (activeMode.links.some((link) => link.url === newLectureLink.value)) {
    return alert('Link already added.')
  }

  activeMode.links.push({
    url: newLectureLink.value,
    progress: 0,
    transcribing: false,
    transcribedText: '',
    status: 'pending'
  })

  newLectureLink.value = ''
}

function startRandomProgressAnimation(link: LectureLinkItem) {
  link.progress = 0

  const intervalId = setInterval(() => {
    // Randomly move progress in small steps
    const randomIncrement = Math.floor(Math.random() * 3) + 1 // Smaller increments
    link.progress += randomIncrement

    // Cap at 95 so there's room for a final jump
    if (link.progress >= 95) {
      link.progress = 95
      clearInterval(intervalId)
    }
  }, Math.floor(Math.random() * 1000) + 500) // Slower and more varied intervals
}

function removeLectureLink(index: number) {
  assistantModes.value[activeModeIndex.value].links.splice(index, 1)
}

async function transcribeAllLectures() {
  const activeMode = assistantModes.value[activeModeIndex.value]

  if (activeMode.links.length === 0) {
    return alert('Add at least one lecture link.')
  }

  for (const link of activeMode.links) {
    if (link.status === 'completed') continue

    // Start random animation
    startRandomProgressAnimation(link)

    link.transcribing = true
    link.status = 'transcribing'
    link.progress = 0

    try {
      const response = await axios.post('http://localhost:8000/api/transcribe_lecture', {
        lecture_url: link.url,
        university: 'Harvard',
        course_id: '66666',
        mode: activeMode.name.toLowerCase()
      })

      link.transcribedText = response.data.transcribed_text
      link.status = 'completed'
    } catch (error) {
      link.status = 'failed'
      alert(`Failed to transcribe: ${link.url}`)
    } finally {
      link.transcribing = false

      // Final jump to 100
      link.progress = 100
    }
  }
}

function shortenLink(link: string, maxLength = 50) {
  return link.length > maxLength ? link.slice(0, maxLength) + '...' : link
}

// ---------------------------------
// 5. Info Modal
// ---------------------------------
function toggleModal(modalId: string) {
  const modalElement = document.getElementById(modalId)
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

const selectedLink = ref<{ url: string } | null>({ url: '' })

const toggleTranscriptionModal = (link: { url: string }) => {
  selectedLink.value = link
  toggleModal('transcriptionModal') // Use the generic modal function
}

// ---------------------------------
// 6. Fixed Header Width
// ---------------------------------
function setHeaderWidth() {
  const header = document.querySelector('.non-scrollable-header') as HTMLElement
  const parent = document.querySelector('.test-container') as HTMLElement

  if (header && parent) {
    const parentWidth = parent.offsetWidth // Get the width of the parent
    header.style.width = `${parentWidth}px` // Set the width of the header
  }
}

// Call the function on page load and window resize
window.addEventListener('load', setHeaderWidth)
window.addEventListener('resize', setHeaderWidth)
onMounted(setHeaderWidth)
</script>

<style scoped>
.form-check-input:checked {
  background-color: var(--color-gray-lighter);
  border-color: var(--color-white);
}

.form-check-input:checked::before {
  background-color: black;
  border-color: black;
}

.form-check-input:focus {
  box-shadow: 0 0 0 0.25rem rgba(167, 167, 167, 0.5);
  color: white;
  border-color: white;
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

/* Fixed header */
.non-scrollable-header {
  position: fixed;
  background-color: var(--color-background-dark);
  z-index: 1;
  padding-bottom: 1em;
  border-bottom: 1px solid #333;
}

/* Add padding to content to prevent overlap */
.content-below-header {
  padding-top: 90px; /* Adjust based on header height */
}

.hover\:bg-danger:hover {
  background-color: red !important;
}

.hover\:bg-success:hover {
  background-color: green !important;
}

.file {
  list-style-type: disc !important;
  list-style-position: inside;
  padding-left: 0; /* Remove padding */
}

.file li {
  list-style-type: disc !important;
  list-style-position: inside;
}

.file-hover:hover {
  background-color: var(--color-gray-dark);
  border-radius: 6px;
  cursor: default;
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
.custom-file-upload {
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

.custom-file-upload:hover,
.custom-file-upload.drag-over {
  border-color: var(--color-gray-shadow);
}

.custom-file-upload .icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-file-upload .icon svg {
  height: 50px;
}

.custom-file-upload .text {
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-file-upload .text span {
  font-weight: 400;
  color: #e8e8e8;
}

.custom-file-upload input {
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
  left: 80%;
  transform: translateX(-50%);
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

.save-assistant-btn {
  width: 160px !important;
  min-width: 150px;
  max-width: 200px;
}
</style>
