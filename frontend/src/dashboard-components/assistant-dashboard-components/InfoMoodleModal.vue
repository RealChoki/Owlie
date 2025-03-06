<template>
  <div class="modal fade" id="infoMoodleModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex justify-content-between align-items-center">
          <h5 class="modal-title"><b>Moodle Tool examples</b></h5>
          <font-awesome-icon
            class="fa-2x cursor-pointer text-white"
            :icon="['fas', 'xmark']"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body">
          <div v-for="(section, index) in modalSections" :key="index">
            <h5>{{ section.title }}:</h5>
            <div @click="openOverlay(section.image)" class="zoomable-container">
              <img
                :src="section.image"
                :alt="section.altText"
                class="img-fluid rounded mb-1 zoomable custom-adjust-img"
              />
            </div>
            <p class="small fst-italic">{{ section.description }}</p>
            <br />
          </div>
        </div>

        <!-- Overlay for Enlarged Image -->
        <div v-if="overlayImage" class="overlay" @click="closeOverlay">
          <img :src="overlayImage" alt="Enlarged" class="enlarged-img custom-adjust-img py-2" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faXmark } from '@fortawesome/free-solid-svg-icons'
import * as bootstrap from 'bootstrap'
import { library } from '@fortawesome/fontawesome-svg-core'

library.add(faXmark)

// Type definition for modal sections
interface ModalSection {
  title: string
  image: string
  altText: string
  description: string
}

// Reactive state for overlay image
const overlayImage = ref<string | null>(null)

// Array of modal sections
const modalSections: ModalSection[] = [
  {
    title: 'Lectures',
    image: '/assets/moodleSS/1.png',
    altText: 'Lecture Information',
    description: 'Access lecture-related materials, including video links and important resources.'
  },
  {
    title: 'Appointments',
    image: '/assets/moodleSS/3.png',
    altText: 'Appointment Information',
    description: 'View scheduled appointments with specific time and date details.'
  },
  {
    title: 'Homework',
    image: '/assets/moodleSS/4.png',
    altText: 'Homework Information',
    description: 'Find upcoming homework assignments with due dates and direct links to Moodle.'
  }
]

// Function to handle opening the modal
const toggleInfoMoodle = () => {
  const infoModalElement = document.getElementById('infoMoodleModal')
  if (infoModalElement) {
    const infoModal = new bootstrap.Modal(infoModalElement)

    // Adding event listeners when the modal is shown
    infoModalElement.addEventListener('shown.bs.modal', () => {
      window.addEventListener('keydown', handleKeydown)
    })

    // Removing event listeners when the modal is hidden
    infoModalElement.addEventListener('hidden.bs.modal', () => {
      window.removeEventListener('keydown', handleKeydown)
    })

    infoModal.show()
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    closeOverlay()
  }
}

const openOverlay = (imageSrc: string) => {
  overlayImage.value = imageSrc
}

const closeOverlay = () => {
  overlayImage.value = null
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.modal-content {
  background-color: var(--color-gray-medium);
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

.zoomable {
  cursor: zoom-in;
  transition: transform 0.2s ease-in-out;
  pointer-events: none;
}

.zoomable-container {
  cursor: zoom-in;
}

/* Overlay styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050; /* Bootstrap modal has z-index 1040 */
}

.enlarged-img {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
}

.custom-adjust-img {
  padding: 0.2em;
  background-color: #131213;
}
</style>
