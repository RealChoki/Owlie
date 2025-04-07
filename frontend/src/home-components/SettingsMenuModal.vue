<template>
  <div class="modal fade" id="settingsModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content" style="background: var(--settings-bg)">
        <div
          class="modal-header d-flex justify-content-between align-items-center"
          style="border-color: var(--settings-seperator-color)"
        >
          <h5 class="modal-title" style="color: var(--text-color)">
            <b> {{ $t('profileMenu.settingsModal.title') }} </b>
          </h5>
          <font-awesome-icon
            class="fa-2x cursor-pointer"
            style="color: var(--text-color)"
            :icon="['fas', 'xmark']"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>

        <div class="modal-body">
          <div class="settings-option mb-1">
            <label class="theme-label scroll-down" @click="handleThemeOpened">
              {{ $t('profileMenu.settingsModal.themeLabel') }}
            </label>
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
            <label class="language-label scroll-down" @click="handleLanguageOpened">{{
              $t('profileMenu.settingsModal.languageLabel')
            }}</label>
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
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import CustomSelect from '@/home-components/CustomSelect.vue'
import { setLanguageLS, getLanguageLS } from '@/services/localStorageService'
import { useTheme } from '@/services/themeService'
import { useI18n } from 'vue-i18n'
import i18n from '@/i18n'

const { t } = useI18n()

defineEmits(['close'])

const { theme } = useTheme()
const language = ref(getLanguageLS())

// Refs to control the open state for each select:
const themeSelectOpen = ref(false)
const languageSelectOpen = ref(false)

const themeOptions = [
  { value: 'dark', label: t('profileMenu.settingsModal.customSelect.theme.dark') },
  { value: 'light', label: t('profileMenu.settingsModal.customSelect.theme.light') }
]

const languageOptions = [
  { value: 'auto', label: t('profileMenu.settingsModal.customSelect.language.system') },
  { value: 'en', label: t('profileMenu.settingsModal.customSelect.language.en') },
  { value: 'de', label: t('profileMenu.settingsModal.customSelect.language.de') }
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
    if (!themeLabel?.contains(e.target as Node) && !themeSelect?.contains(e.target as Node)) {
      themeSelectOpen.value = false
    }
  }
  if (languageSelectOpen.value) {
    if (!languageLabel?.contains(e.target as Node) && !languageSelect?.contains(e.target as Node)) {
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

watch(language, (newLanguage) => {
  if (newLanguage !== 'auto'){
    setLanguageLS(newLanguage)
    i18n.global.locale.value = newLanguage
  }
  if (newLanguage === 'auto') {
    const systemLanguage = navigator.language.split('-')[0]
    const userLanguage = systemLanguage || 'en'
    setLanguageLS('auto')
    i18n.global.locale.value = userLanguage
  }

})
</script>

<style scoped>
.settings-option {
  color: var(--text-color);
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
