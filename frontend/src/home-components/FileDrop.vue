<template>
  <div class="file-drop-container">
    <label
      for="file"
      class="custom-file-upload"
      style="min-height: 20vh"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
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
      <input id="file" type="file" multiple />
    </label>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  isDragging,
  uploadedFiles,
  computedAcceptedFileTypes,
  readNonPdfFile,
  readPdfFile,
  fileCount
} from '../services/filesService'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const isDragValid = ref(false)
const isFileInvalid = ref(false)
const isDropped = ref(false)

interface ExtendedFile extends File {
  content?: string | ArrayBuffer | null
}

const dragText = computed(() => {
  if (!isDropped.value) return t('owlie.fileDrop.title')
  return isFileInvalid.value ? t('owlie.fileDrop.invalid') : t('owlie.fileDrop.valid')
})

function handleDragOver(event: DragEvent) {
  isDragging.value = true
  isDragValid.value = true
}

function handleDragLeave() {
  isDragging.value = false
  isDragValid.value = false
}

function handleFileDrop(event: DragEvent) {
  event.preventDefault()
  setTimeout(() => {
    isDragging.value = false
  }, 500)
  isDropped.value = true

  const files = event.dataTransfer?.files
  if (files) {
    const acceptedTypes = computedAcceptedFileTypes.value

    const selectedFiles = Array.from(files).filter((file) => {
      const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
      return acceptedTypes.includes(fileExt) || acceptedTypes.includes(file.type)
    })

    const hasInvalidFiles = Array.from(files).some((file) => {
      const fileExt = '.' + file.name.split('.').pop()?.toLowerCase()
      return !acceptedTypes.includes(fileExt) && !acceptedTypes.includes(file.type)
    })

    isDragValid.value = !hasInvalidFiles
    isFileInvalid.value = hasInvalidFiles

    setTimeout(() => {
      isDragging.value = isDragValid.value = isFileInvalid.value = isDropped.value = false
    }, 1000)

    const fileSet = uploadedFiles.value

    selectedFiles.forEach(async (file) => {
      const fileAlreadyExists = Array.from(fileSet).some((existingFile) => existingFile.name === file.name)

      if (!fileAlreadyExists) {
        const typedFile = file as ExtendedFile

        try {
          if (file.name.toLowerCase().endsWith('.pdf')) {
            // Handle PDF files
            const pdfText = await readPdfFile(file)
            typedFile.content = pdfText as string | ArrayBuffer
          } else {
            // Handle non-PDF files
            typedFile.content = (await readNonPdfFile(file)) as string | ArrayBuffer
          }

          fileSet.add(typedFile)
          fileCount.value = uploadedFiles.value.size
        } catch (error) {
          console.error('Error reading file:', file.name, error)
        }
      }
    })

    console.log('Chosen files:', uploadedFiles.value)
  } else {
    isDragValid.value = false
  }
}
</script>

<style scoped>
.file-drop-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.custom-file-upload {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: space-between;
  gap: 10px;
  align-items: center;
  justify-content: center;
  border: 2px dashed var(--file-drop-border-dark);
  background-color: var(--file-drop-bg);
  opacity: 0.95;
  padding: 1.5rem;
  border-radius: 10px;
}

.custom-file-upload:hover,
.custom-file-upload.drag-over {
  border-color: var(--file-drop-border-light);
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
</style>
