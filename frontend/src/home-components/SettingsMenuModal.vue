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
            <label class="text-white theme-label" @click="handleThemeOpened">Theme</label>
            <div class="theme-select">
              <CustomSelect
                v-model="theme"
                :options="themeOptions"
                :isOpen="themeSelectOpen"
                @opened="handleThemeOpened"
                @closed="themeSelectOpen = false"
              />
            </div>
          </div>

          <div class="settings-option">
            <label class="text-white language-label" @click="handleLanguageOpened">Language</label>
            <div class="language-select">
              <CustomSelect
                v-model="language"
                :options="languageOptions"
                :isOpen="languageSelectOpen"
                @opened="handleLanguageOpened"
                @closed="languageSelectOpen = false"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faXmark, faChevronDown, faChevronUp } from '@fortawesome/free-solid-svg-icons'
import CustomSelect from '@/home-components/CustomSelect.vue'
import { setThemeLS, getThemeLS, setLanguageLS, getLanguageLS } from '@/services/localStorageService'

library.add(faXmark, faChevronDown, faChevronUp)
defineEmits(['close'])

const theme = ref(getThemeLS()) 
const language = ref(getLanguageLS())

// Refs to control the open state for each select:
const themeSelectOpen = ref(false)
const languageSelectOpen = ref(false)

const themeOptions = [
  { value: 'dark', label: 'Dark' },
  { value: 'light', label: 'Light' }
]

const languageOptions = [
  { value: 'auto', label: 'Auto-detect' },
  { value: 'en', label: 'English' },
  { value: 'de', label: 'German' }
]

function handleThemeOpened() {
  themeSelectOpen.value = true
  languageSelectOpen.value = false
}

function handleLanguageOpened() {
  languageSelectOpen.value = true
  themeSelectOpen.value = false
}

// Global click handler to close selects when clicking outside their label/select container:
function handleDocumentClick(e: MouseEvent) {
  const themeLabel = document.querySelector('.theme-label')
  const themeSelect = document.querySelector('.theme-select')
  const languageLabel = document.querySelector('.language-label')
  const languageSelect = document.querySelector('.language-select')

  if (themeSelectOpen.value) {
    if (
      !themeLabel?.contains(e.target as Node) &&
      !themeSelect?.contains(e.target as Node)
    ) {
      themeSelectOpen.value = false
    }
  }
  if (languageSelectOpen.value) {
    if (
      !languageLabel?.contains(e.target as Node) &&
      !languageSelect?.contains(e.target as Node)
    ) {
      languageSelectOpen.value = false
    }
  }
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
})

// Watch for theme changes and save to localStorage
watch(theme, (newTheme) => {
  if (newTheme === 'light') {
    document.documentElement.classList.add('light-theme')
  } else {
    document.documentElement.classList.remove('light-theme')
  }
  setThemeLS(newTheme) // Save the selected theme to localStorage
})

// Watch for language changes and save to localStorage
watch(language, (newLanguage) => {
  setLanguageLS(newLanguage) // Save the selected language to localStorage
})
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