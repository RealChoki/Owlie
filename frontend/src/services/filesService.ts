import { reactive } from 'vue'
import axios from 'axios'
import { getThreadIdLS, getVectorStoreIdLS, getCurrentModeLS, getCurrentModuleLS  } from './localStorageService';

const fileState = reactive({
  files: [] as string[],
  currentFile: '' as string
})

export async function uploadFiles(filesToUpload: File[]) {
  try {
    // Save the file names in the file state
    filesToUpload.forEach(file => fileState.files.push(file.name));
    fileState.currentFile = '';

    // Create FormData to send files
    const formData = new FormData();
    for (const file of filesToUpload) {
      formData.append('files', file);
    }

    formData.append('thread_id', getThreadIdLS());
    formData.append('vector_store_id',  getVectorStoreIdLS());
    formData.append('current_module', getCurrentModuleLS().replace(/ /g, '_'));
    formData.append('current_mode',  getCurrentModeLS());

    // Send the files to the FastAPI backend
    console.log('Uploading files:', filesToUpload);
    console.log('Uploading formdata:', formData);

    const response = await axios.post('http://localhost:8000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // Log the server response
    console.log('Server response:', response.data);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error uploading files:', error.message);
      console.error('Error details:', error.toJSON());
    } else {
      console.error('Unexpected error:', error);
    }
  }
}

// filesService.ts:46 Unexpected error: TypeError: Cannot read properties of null (reading 'files')
//     at uploadFiles (filesService.ts:23:21)
//     at handleFileChange (FooterInput.vue:164:7)


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

export default {
  uploadFiles,
  getFiles,
  getCurrentFile,
  setCurrentFile,
  clearFiles
}