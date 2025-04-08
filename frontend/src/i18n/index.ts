import { createI18n } from 'vue-i18n'
import type { I18n } from 'vue-i18n'
import en from './en.json'
import de from './de.json'
import es from './es.json'
import fr from './fr.json'
import it from './it.json'
import pt from './pt.json'
import ru from './ru.json'
import zh from './zh.json'
import ja from './ja.json'  // Assuming you have a Japanese translation file
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
    de,
    es,
    fr,
    it,
    pt,
    ru,
    zh,
    ja
  }
})

export default i18n
