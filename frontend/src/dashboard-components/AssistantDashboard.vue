<template>
  <div class="non-scrollable-header w-100">
    <div class="assistants-tab w-100">
      <div class="mb-3">
        <div class="d-flex justify-content-between align-items-center">
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
            class="custome-file-upload"
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
            <div v-for="(link, index) in lectureLinks" :key="index" class="lecture-link d-flex align-items-center">
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPenToSquare, faSquareXmark } from '@fortawesome/free-solid-svg-icons'
import axios from 'axios'

library.add(faPenToSquare, faSquareXmark)

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
  links: string
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
const assistantModes = ref<AssistantMode[]>([
  { name: 'General', status: 'Active', moodleEnabled: true, files: [], links: '', instructions: '' },
  { name: 'Quiz', status: 'Inactive', moodleEnabled: false, files: [], links: '', instructions: '' },
  { name: 'Exam', status: 'Activating', moodleEnabled: false, files: [], links: '', instructions: '' }
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

function saveAssistants() {
  console.log('Assistant Modes Configuration:', assistantModes.value)
  alert('Assistants configuration saved!')
}

// ---------------------------------
// 3. File Handling (Upload & Drag-Drop)
// ---------------------------------
const isDragging = ref(false)
const isDropped = ref(false)
const isDragValid = ref(false)
const isFileInvalid = ref(false)

const acceptedExtensions = ['.c', '.cpp', '.cs', '.css', '.docx', '.pdf', '.py', '.ts', '.txt']
const acceptedMimeTypes = ['application/pdf', 'text/plain', 'text/css']

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
const lectureLinks = ref<LectureLinkItem[]>([])

const urlPattern = new RegExp('^(https?:\\/\\/)', 'i')

function addLectureLink() {
  if (!urlPattern.test(newLectureLink.value)) return alert('Invalid URL format.')
  if (lectureLinks.value.some((link) => link.url === newLectureLink.value)) return alert('Link already added.')

  lectureLinks.value.push({
    url: newLectureLink.value,
    progress: 0,
    transcribing: false,
    transcribedText: '',
    status: 'pending'
  })
  newLectureLink.value = ''
}

function removeLectureLink(index: number) {
  lectureLinks.value.splice(index, 1)
}

async function transcribeAllLectures() {
  if (lectureLinks.value.length === 0) return alert('Add at least one lecture link.')

  for (const link of lectureLinks.value) {
    if (link.status === 'completed') continue

    link.transcribing = true
    link.status = 'transcribing'
    link.progress = 0

    try {
      const response = await axios.post('http://localhost:8000/api/transcribe_lecture', { lecture_url: link.url })
      link.transcribedText = response.data.transcribed_text
      link.status = 'completed'
    } catch (error) {
      link.status = 'failed'
      alert(`Failed to transcribe: ${link.url}`)
    } finally {
      link.transcribing = false
    }
  }
}

function shortenLink(link: string, maxLength = 50) {
  return link.length > maxLength ? link.slice(0, maxLength) + '...' : link
}
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

.non-scrollable-header {
}

.scrollable-content {
  overflow-y: auto;
  padding-bottom: 1rem; /* Add spacing at bottom */
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
.custome-file-upload {
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

.custome-file-upload:hover,
.custome-file-upload.drag-over {
  border-color: var(--color-gray-shadow);
}

.custome-file-upload .icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.custome-file-upload .icon svg {
  height: 50px;
}

.custome-file-upload .text {
  display: flex;
  align-items: center;
  justify-content: center;
}

.custome-file-upload .text span {
  font-weight: 400;
  color: #e8e8e8;
}

.custome-file-upload input {
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
