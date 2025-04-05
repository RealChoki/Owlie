import { ref, watch, onMounted, computed } from 'vue'
import { setThemeLS, getThemeLS } from './localStorageService'

const theme = ref(getThemeLS())
export const useTheme = () => {
  console.log('Current theme:', theme.value)
  

  // Apply theme to the document on initial load
  const applyTheme = (newTheme: string) => {
    document.documentElement.setAttribute('data-theme', newTheme)
    setThemeLS(newTheme)
  }

  onMounted(() => {
    applyTheme(theme.value)
  })

  watch(theme, (newTheme) => {
    applyTheme(newTheme)
  })

  return { theme, applyTheme }
}

export const isDarkMode = computed(() => theme.value === 'dark')
