import { createI18n } from 'vue-i18n'
import type { I18n } from 'vue-i18n'
import en from './en.json'
import de from './de.json'
import { getLanguageLS } from '@/services/localStorageService'  // Assuming you have this function to get from localStorage

const storedLanguage = getLanguageLS()

const systemLanguage = navigator.language.split('-')[0]  // 'en', 'de', etc.

const initialLanguage = storedLanguage || systemLanguage || 'en'

const i18n: I18n = createI18n({
  legacy: false,
  locale: initialLanguage,
  fallbackLocale: 'en',
  messages: {
    en,
    de
  }
})

export default i18n
