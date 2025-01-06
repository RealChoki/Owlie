import { ref } from 'vue'
import { franc } from 'franc-min'
import { getMessages } from '../services/chatService'

const availableVoices = ref<SpeechSynthesisVoice[]>([])
// const isTTSPlaying = ref(false)
let utterance: SpeechSynthesisUtterance | null = null

const femaleVoicesMap: { [key: string]: string } = {
  'en-US': 'Microsoft Zira - English (United States)',
  'de-DE': 'Microsoft Katja - German (Germany)',
  'fr-FR': 'Microsoft Hortense - French (France)',
  'es-ES': 'Microsoft Helena - Spanish (Spain)'
}

const loadVoices = () => {
  availableVoices.value = window.speechSynthesis.getVoices()
}

function detectLanguage(text: string): string {
  const langCode = franc(text, { only: ['deu', 'eng', 'fra', 'spa'] })
  console.log('Detected language code:', langCode)

  switch (langCode) {
    case 'deu':
      return 'de-DE'
    case 'eng':
      return 'en-US'
    case 'fra':
      return 'fr-FR'
    case 'spa':
      return 'es-ES'
    default:
      console.warn(`Language detection failed for text: "${text}". Defaulting to 'de-DE'.`)
      return 'de-DE' // Fallback language
  }
}

function readAssistantMessage(content: string, onEnd: () => void) {
  if (!utterance) {
    console.log('readAssistantMessage called')
    console.log('Message Content:', content)

    const detectedLang = detectLanguage(content)
    console.log('Detected Language:', detectedLang)

    utterance = new SpeechSynthesisUtterance(content)

    // Set language based on detection
    utterance.lang = detectedLang
    utterance.pitch = 1.1
    utterance.rate = 1.3
    utterance.volume = 1

    // Log available voices
    console.log(
      'Available Voices:',
      availableVoices.value.map((voice) => voice.name)
    )

    // Select female voice
    const selectedVoiceName = femaleVoicesMap[detectedLang]
    const selectedVoice = availableVoices.value.find(
      (voice) => voice.name === selectedVoiceName
    )

    if (selectedVoice) {
      utterance.voice = selectedVoice
      console.log('Selected voice:', selectedVoice.name)
    } else {
      console.warn(`No female voice found for language ${detectedLang}. Using default voice.`)
    }

    utterance.onend = () => {
      onEnd()
      utterance = null // Reset utterance after playback ends
      console.log('TTS playback ended.')
    }

    window.speechSynthesis.cancel() // Clear pending
    window.speechSynthesis.speak(utterance)
    console.log('TTS playback started.')
  }
}

function stopTTS() {
  if (utterance) {
    window.speechSynthesis.cancel()
    utterance = null // Reset utterance when TTS is stopped
    console.log('TTS stopped')
  }
}

function toggleTTS(content: string, onEnd: () => void) {
  if (utterance) {
    window.speechSynthesis.cancel()
  } else {
    readAssistantMessage(content, onEnd)
  }
}

export { loadVoices, stopTTS, toggleTTS }
