import { ref } from 'vue'
import i18n from '@/i18n'

const t = i18n.global.t as (...args: any[]) => string;

const owlDisplayMessage = ref('')
const navbarCourseTitle = ref('')

const setOwlDisplayMessage = (message: string) => {
  owlDisplayMessage.value = message
}

const setNavbarCourseTitle = (course: string, mode: string) => {
  if (mode !== 'general') {
    const modeLabel = t(`navbar.courseTitleMode.${mode}`)
    navbarCourseTitle.value = `${course} (${modeLabel})`
  } else {
    navbarCourseTitle.value = course
  }
}

const clearOwlDisplayMessage = () => {
  owlDisplayMessage.value = ''
}

const clearNavbarCourseTitle = () => {
  navbarCourseTitle.value = ''
}

const displayAssistantNotFountMessage = () => {
  setOwlDisplayMessage(t('services.owlDisplayMsg.assistantNotFound'))
  setTimeout(() => setOwlDisplayMessage('(｡>﹏<)'), 2000)
  setTimeout(() => setOwlDisplayMessage(t('services.owlDisplayMsg.assistantNotFound')), 4000)
}

export {
  owlDisplayMessage,
  navbarCourseTitle,
  setOwlDisplayMessage,
  setNavbarCourseTitle,
  clearOwlDisplayMessage,
  clearNavbarCourseTitle,
  displayAssistantNotFountMessage
}
