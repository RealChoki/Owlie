<template>
  <div class="modal fade" id="transcriptionModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog custom-modal">
      <div class="modal-content">
        <div class="modal-header d-flex justify-content-between align-items-center">
          <h5 class="modal-title"><b>Edit Transcriptions</b></h5>
          <font-awesome-icon
            class="fa-2x cursor-pointer text-white"
            :icon="['fas', 'xmark']"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body pb-3 pt-2">
          <div class="textarea-container position-relative w-100 flex-grow-1">
            <h6 class="text-white mt-2 mb-3">
              <a :href="transcribeFileURL" class="text-white cursor-pointer" target="_blank">
                {{ transcribeFileURL }}
              </a>
            </h6>

            <textarea
              v-model="file.content"
              class="w-100 p-3 rounded file-textarea"
              ref="textareaRef"
              :readonly="!file.isEditMode"
              @input="adjustHeight"
            ></textarea>

            <button
              class="btn btn-edit bg-white position-absolute bottom-0 end-0 mx-3 my-3 icon-click-effect"
              @click="toggleEdit"
            >
              <span v-if="file.isEditMode"> Save </span>
              <span v-else>
                Edit
                <font-awesome-icon
                  :icon="['fas', 'pen-to-square']"
                  class="cursor-pointer"
                  style="color: var(--color-gray-shadow)"
                />
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faXmark } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'

library.add(faXmark)

// Props to receive link object
const props = defineProps({
  link: {
    type: Object as () => { url: string } | null,
    required: true
  }
})

// Reactive state for transcribed file data
const transcribeFileURL = ref('')
const file = ref<{ title: string; content: string; isEditMode: boolean }>({
  title: '',
  content: '',
  isEditMode: false
})

const textareaRef = ref<HTMLElement | null>(null)

// Adjust the height of the textarea dynamically
const adjustHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`
    if (parseInt(textareaRef.value.style.height) < 150) {
      textareaRef.value.style.height = '150px'
    }
  }
}

// Toggle edit mode for transcription
const toggleEdit = () => {
  file.value.isEditMode = !file.value.isEditMode
  adjustHeight()
  if (file.value.isEditMode) {
    textareaRef.value?.focus()
  } else {
    updateTranscribedFile(file.value.title, file.value.content)
    adjustHeight()
  }
}

// Sanitize the file name URL
const sanitizeFilename = (url: string) => {
  url = url.replace(/^https?:\/\//, '')  // Remove the protocol part (http:// or https://)
  return url.replace(/[^a-zA-Z0-9_]/g, '_')  // Replace non-alphanumeric characters with '_'
}

// Fetch the transcription data from the server
const fetchTranscription = async (linkUrl: string) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/assistants/file/${sanitizeFilename(linkUrl)}`)
    file.value.title = response.data.title
    file.value.content = response.data.content
  } catch (error) {
    console.error('Failed to fetch transcription', error)
  } finally {
    setTimeout(() => {
      adjustHeight()
    }, 200)
  }
}

// Watch the link prop for changes and fetch transcription
watch(() => props.link, (newLink) => {
  if (newLink && newLink.url) {
    transcribeFileURL.value = newLink.url
    fetchTranscription(newLink.url)
  }
}, { immediate: true }) // Trigger fetch when component mounts or link changes

// Update the transcription file after edit
const updateTranscribedFile = async (fileName: string, content: string) => {
  return axios.put(`http://localhost:8000/api/assistants/file/${fileName}`, content)
}
</script>

<style scoped>
.modal-content {
  background-color: var(--color-gray-medium); /* Light background color */
  border: 1px solid var(--color-gray-shadow);
  border-radius: 8px;
}

.modal-header {
  border-bottom: 1px solid var(--color-gray-shadow);
}

.modal-title {
  color: var(--color-white);
}

.modal-body {
  color: var(--color-white);
  padding-bottom: 0;
}

.modal-body p {
  margin-bottom: 0;
}
/* edit transcription modal */

.textarea-container {
  max-width: 800px;
}

.file-textarea {
  background-color: var(--color-gray-dark);
  max-width: 100%;
  max-height: 80vh;
  min-height: 150px;
  border: none;
  outline: none;
  resize: none;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.btn-edit:hover {
  opacity: 0.2;
}

.custom-modal {
  min-width: 500px;
  width: 50%;
  max-width: unset !important; /* Override Bootstrap's max-width */
}
</style>
