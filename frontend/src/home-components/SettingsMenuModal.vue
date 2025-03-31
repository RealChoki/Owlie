<template>
  <div class="modal fade" id="settingsModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content" style="background: var(--color-gray-dark)">
        <div
          class="modal-header d-flex justify-content-between align-items-center"
          style="border-color: var(--color-gray-lighter)"
        >
          <h5 class="modal-title text-white"><b>Settings</b></h5>
          <font-awesome-icon
            class="fa-2x cursor-pointer text-white"
            :icon="['fas', 'xmark']"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>

        <div class="modal-body">
          <div class="settings-option mb-1">
            <label class="text-white">Theme</label>
            <CustomSelect v-model="theme" :options="themeOptions" />
          </div>

          <div class="settings-option">
            <label class="text-white">Language</label>
            <CustomSelect v-model="language" :options="languageOptions" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faXmark, faChevronDown, faChevronUp } from '@fortawesome/free-solid-svg-icons'
import CustomSelect from '@/home-components/CustomSelect.vue'

library.add(faXmark, faChevronDown, faChevronUp)
defineEmits(['close'])

const theme = ref('dark')
const language = ref('auto')

const activeSelect = ref<string | null>(null)

const themeOptions = [
  { value: 'dark', label: 'Dark' },
  { value: 'light', label: 'Light' }
]

const languageOptions = [
  { value: 'auto', label: 'Auto-detect' },
  { value: 'en', label: 'English' },
  { value: 'de', label: 'German' }
]
</script>

<style scoped>
.settings-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.settings-modal {
  background: var(--color-gray-medium);
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  text-align: center;
}

.long-hr {
  width: calc(100% + 40px);
  margin: 0 -20px;
  border: 1px solid var(--color-gray-lighter);
}

.settings-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5em 0;
}

.settings-option:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
</style>
