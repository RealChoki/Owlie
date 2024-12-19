import { reactive } from 'vue';
import axios from 'axios';
import {
  getCurrentModeLS,
  getCurrentModuleLS,
} from './localStorageService';
import { getAssistant, deleteOldAssistantIdAndUpdateAssistantId, getOldAssistantId, setNewAssistantIdAndSetOldAssistantId, removeAssistantThreadId } from '../services/openaiService';


const fileState = reactive({
  files: [] as string[],
  currentFile: '' as string,
  isTempAssistant: false as boolean
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

    formData.append('thread_id', getAssistant().threadId);
    formData.append('current_module', getCurrentModuleLS().replace(/ /g, '_'));
    formData.append('current_mode',  getCurrentModeLS());
    
    if (fileState.isTempAssistant) {
      formData.append('assistant_id', getAssistant().id);
    }
    
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
    if(!fileState.isTempAssistant){
      setNewAssistantIdAndSetOldAssistantId(response.data.temporary_assistant_id);

      fileState.isTempAssistant = true;
    }
    
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error uploading files:', error.message);
      console.error('Error details:', error.toJSON());
    } else {
      console.error('Unexpected error:', error);
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

export async function resetFileService() {
  const oldThreadId = getAssistant().threadId;

  if (oldThreadId) {
    try {
      // Call the backend API to delete the temporary assistant and vector store
      await axios.post('http://localhost:8000/api/delete_temp_assistant', {
        old_thread_id: oldThreadId,
      });
    } catch (error) {
      console.error('Error deleting tempassistant:', error);
    } finally {
      // Clear relevant entries from local storage
      removeAssistantThreadId();
    }
  }

  // Reset the file state
  fileState.files.length = 0;
  fileState.currentFile = '';
  fileState.isTempAssistant = false;

  // Restore the old assistant ID if it exists
  const oldAssistantId = getOldAssistantId();
  if (oldAssistantId) {
    deleteOldAssistantIdAndUpdateAssistantId()
  }
}

// delete old assistant function, use mode, and module to 
// try {
//   const selectedModuleValue = getSelectedModuleLS();
//   await fetchAssistantIds(
//     selectedModuleValue?.replace(/ /g, '_'),
//     getCurrentModeLS()
//   );
//   await initializeThread();
// } catch (error) {
//   console.error('Error during initialization:', error);
// }

export default {
  uploadFiles,
  getFiles,
  getCurrentFile,
  setCurrentFile,
  clearFiles,
  resetFileService
}