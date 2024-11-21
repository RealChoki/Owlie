import { reactive } from 'vue'
import axios from 'axios'

const fileState = reactive({
  files: [] as string[],
  currentFile: '' as string
})

export async function uploadFiles(filesToUpload: File[]) {
  if (filesToUpload.length > 0) {
    try {
      // Save the file names in the file state
      filesToUpload.forEach(file => fileState.files.push(file.name));
      fileState.currentFile = '';

      // Create FormData to send files
      const formData = new FormData();
      filesToUpload.forEach(file => formData.append('files', file));

      // Send the files to the Fastify backend
      const response = await axios.post('http://localhost:3000/upload', formData, {
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

export default {
  uploadFiles,
  getFiles,
  getCurrentFile,
  setCurrentFile,
  clearFiles
}