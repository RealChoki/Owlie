import { reactive, ref, computed } from 'vue'
import axios from 'axios'
import {
  getAssistantId,
  getAssistantThreadId,
  restoreOldAssistantId,
  getOldAssistantId,
  updateAssistantIdAndStoreOldId,
  removeAssistantThreadId,
  getAssistantMode,
  getAssistantCourse
} from '../services/openaiService'

const acceptedFileTypes = [
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

const fileState = reactive({
  files: [] as string[],
  currentFile: '' as string,
  isTempAssistant: false as boolean
})

//only uploading one file at a time
// use File Set instead of array
export async function uploadFiles(filesToUpload: File[]) {
  try {
    // Save the file names in the file state
    filesToUpload.forEach((file) => fileState.files.push(file.name))
    fileState.currentFile = ''

    // Create FormData to send files
    const formData = new FormData()
    for (const file of filesToUpload) {
      formData.append('files', file)
    }

    formData.append('thread_id', getAssistantThreadId())
    formData.append('current_course', getAssistantCourse().replace(/ /g, '_'))
    formData.append('current_mode', getAssistantMode())

    if (fileState.isTempAssistant) {
      formData.append('assistant_id', getAssistantId())
    }

    // Send the files to the FastAPI backend
    console.log('Uploading files:', filesToUpload)
    console.log('Uploading formdata:', formData)

    const response = await axios.post('http://localhost:8000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Log the server response
    console.log('Server response:', response.data)
    if (!fileState.isTempAssistant) {
      updateAssistantIdAndStoreOldId(response.data.temporary_assistant_id)

      fileState.isTempAssistant = true
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error uploading files:', error.message)
      console.error('Error details:', error.toJSON())
    } else {
      console.error('Unexpected error:', error)
    }
  }
}

export function fetchQuizFiles() {
  return axios.get('http://localhost:8000/api/quiz_files')
}

export function fetchQuizFile(quizFile: string) {
  return axios.get(`http://localhost:8000/api/quiz_files/${quizFile}`)
}

export function postQuizFile(quizFile: string, data: any) {
  return axios.post(`http://localhost:8000/api/quiz_files/${quizFile}`, data)
}

export function getFiles() {
  return fileState.files
}

export function getCurrentFile() {
  return fileState.currentFile
}

export function setCurrentFile(newFile: string) {
  fileState.currentFile = newFile
}

export function clearFiles() {
  fileState.files.length = 0
}

export async function resetFileService() {
  const oldThreadId = getAssistantThreadId()

  if (oldThreadId) {
    try {
      // Call the backend API to delete the temporary assistant and vector store
      await axios.post('http://localhost:8000/api/delete_temp_assistant', {
        old_thread_id: oldThreadId
      })
    } catch (error) {
      console.error('Error deleting tempassistant:', error)
    } finally {
      removeAssistantThreadId()
    }
  }

  // Reset the file state
  fileState.files.length = 0
  fileState.currentFile = ''
  fileState.isTempAssistant = false

  // Restore the old assistant ID if it exists
  const oldAssistantId = getOldAssistantId()
  if (oldAssistantId) {
    restoreOldAssistantId()
  }
}

export const fileCount = ref(0)
export const uploadedFiles = ref<Set<File>>(new Set())
export const isDragging = ref(false)
export const computedAcceptedFileTypes = computed(() => [...acceptedFileTypes, ...acceptedMimeTypes])

export function triggerFileInput(fileInputRef: HTMLInputElement | null) {
  if (fileInputRef) {
    fileInputRef.click()
  }
}

export function onFilesSelected(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const files = Array.from(input.files)

    files.forEach((file) => {
      const fileExtension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase()
      if (!acceptedFileTypes.includes(fileExtension)) {
        return
      }

      // Check if a file with the same name and size already exists in the set
      const fileExists = Array.from(uploadedFiles.value).some(
        (existingFile) => existingFile.name === file.name && existingFile.size === file.size
      )

      if (!fileExists) {
        uploadedFiles.value.add(file)
        fileCount.value = uploadedFiles.value.size
      }
    })
  }
  console.log('Choosen files:', uploadedFiles.value)
}

export function removeFile(fileToRemove: File) {
  uploadedFiles.value.delete(fileToRemove)
  fileCount.value = uploadedFiles.value.size
}

export function resetFileCount() {
  fileCount.value = 0
  uploadedFiles.value.clear()
}

export default {
  uploadFiles,
  removeFile,
  getFiles,
  getCurrentFile,
  setCurrentFile,
  clearFiles,
  resetFileService,
  fileCount,
  uploadedFiles,
  onFilesSelected,
  resetFileCount,
  triggerFileInput,
  computedAcceptedFileTypes
}
