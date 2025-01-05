import { reactive, ref, watch } from 'vue'
import { getHeartCountLS, setHeartCountLS, getMessageCountLS, setMessageCountLS } from '../services/localStorageService'

import { getAssistantId, getAssistantThreadId } from '../services/openaiService'

// Reactive state
const chatState = reactive({
  messages: [] as { content: string; role: string; index: number; id?: string; isComplete?: boolean }[],
  currentMessage: '' as string,
  thinking: false as boolean,
  currentThreadId: '' as string
})

// Reactive references
export const heartCount = ref(getHeartCountLS())
export const messageCount = ref(getMessageCountLS())

// Watchers to update local storage
watch(heartCount, (newValue) => {
  setHeartCountLS(newValue)
})

watch(messageCount, (newValue) => {
  setMessageCountLS(newValue)
})

// No hearts messages
const noHeartsMessages = [
  'Zzzz... schnarch',
  'Ich bin gleich wieder da. Nur ein kurzes Nickerchen... zzzz...',
  'Was für eine wundervolle... zzz... Frage...',
  'Hoot. Ich bin gerade ein bisschen müde... zzzz...',
  'Zzzz... Oh, hast du mich geweckt? Nein, nein, alles gut. Hoot. Nur ein kleines Augenzwinkern... zzzz...',
  'Flügel ausstrecken, Kopf ins Gefieder, und... zzzz...',
  'Hoot. So ein schöner Mond heute, aber... zzzz...',
  'Psst. Ich bin eine Eule, Nachtaktivität ist meine Stärke... normalerweise... hoot... aber manchmal... schnarch zzzz...'
]

// Utility functions
function getRandomNoHeartsMessage() {
  const randomIndex = Math.floor(Math.random() * noHeartsMessages.length)
  return noHeartsMessages[randomIndex]
}

function resetCounts() {
  heartCount.value = 5
  messageCount.value = 0
  setHeartCountLS(heartCount.value)
  setMessageCountLS(messageCount.value)
}

// async function sendToThread(content: string) {
//   const assistant_id = getAssistantId();
//   if (!assistant_id) {
//     throw new Error('Assistant ID not found.');
//   }

//   const threadId = getAssistantThreadId();
//   if (!threadId) {
//     throw new Error(`Thread ID not found in assistantService. id: ${threadId}`);
//   }

//   chatState.currentThreadId = threadId;

//   const response = await axios.post(`http://localhost:8000/api/threads/${threadId}/send_and_wait`, {
//     content,
//     assistant_id,
//   });

//   console.log('Received response:', response);

//   if (getAssistantThreadId() == chatState.currentThreadId) {
//     addAssistantMessage(response.data.content);
//   } else {
//     console.log('Received message from old thread. Ignoring.');
//   }
// }

async function sendToThread(content: string) {
  const assistant_id = getAssistantId()
  const threadId = getAssistantThreadId()

  if (!assistant_id || !threadId) {
    throw new Error('Assistant ID or Thread ID not found.')
  }

  chatState.currentThreadId = threadId
  chatState.thinking = true

  const url = `http://localhost:8000/api/threads/${threadId}/send_and_wait_stream?assistant_id=${assistant_id}&message=${content}`
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error('Failed to connect to the backend')
  }

  if (!response.body) {
    throw new Error('Response body is null')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let done = false

  const initialMessage = {
    content: '',
    role: 'assistant',
    index: chatState.messages.length,
    isComplete: false
  }
  chatState.thinking = false
  chatState.messages.push(initialMessage)
  const lastMessageIndex = chatState.messages.length - 1

  while (!done) {
    const { value, done: readerDone } = await reader.read()
    done = readerDone
    const chunk = decoder.decode(value, { stream: true })
    chatState.messages[lastMessageIndex].content += chunk
  }
  chatState.messages[lastMessageIndex].isComplete = true
}

function handleSendMessageError(error: any) {
  console.error('Error sending message:', error)
  addAssistantMessage('An error occurred. Please try again later.')
}

// Message handling functions
function addUserMessage(content: string) {
  chatState.messages.push({ content, role: 'user', index: chatState.messages.length })
  chatState.currentMessage = ''
}

function addAssistantMessage(content: string) {
  chatState.messages.push({ content, role: 'assistant', index: chatState.messages.length })
}

function incrementMessageCount() {
  messageCount.value += 1
}

function consumeHalfHeart() {
  heartCount.value = Math.max(heartCount.value - 0.5, 0)
  messageCount.value = 0
  console.log(`[sendMessage] Consumed half a heart. New heartCount: ${heartCount.value}`)
}

// Exported functions
export async function sendMessage(content: string) {
  console.log(
    `[sendMessage] Attempting to send message. Current heartCount: ${heartCount.value}, messageCount: ${messageCount.value}`
  )

  if (!content.trim()) {
    return
  }

  addUserMessage(content)

  if (heartCount.value <= 0) {
    addAssistantMessage(getRandomNoHeartsMessage())
    return
  }

  incrementMessageCount()

  if (messageCount.value >= 2) {
    consumeHalfHeart()
  }

  chatState.currentMessage = ''

  try {
    await sendToThread(content)
  } catch (error) {
    handleSendMessageError(error)
  } finally {
    chatState.thinking = false
  }
}

export async function resendMessage(index: number) {
  console.log(
    `[resendMessage] Attempting to resend message. Current heartCount: ${heartCount.value}, messageCount: ${messageCount.value}`
  )
  deleteMessagesFromIndex(index)
  const userIndex = index - 1
  if (userIndex >= 0 && chatState.messages[userIndex].role === 'user') {
    const userPrompt = chatState.messages[userIndex].content
    console.log('Re-sending prompt:', userPrompt)

    if (!userPrompt.trim()) {
      return
    }

    if (heartCount.value <= 0) {
      addAssistantMessage(getRandomNoHeartsMessage())
      return
    }

    console.log(chatState)
    console.log(chatState.messages)

    try {
      await sendToThread(userPrompt)
    } catch (error) {
      handleSendMessageError(error)
    }
  }
}

function deleteMessagesFromIndex(index: number): void {
  chatState.messages.splice(index)
}

export function getMessages() {
  return chatState.messages
}

export function getCurrentMessage() {
  return chatState.currentMessage
}

export function setCurrentMessage(newMessage: string) {
  chatState.currentMessage = newMessage
}

export function clearMessages(resetCount: boolean = true) {
  chatState.messages.length = 0
  if (resetCount) {
    resetCounts()
  }
  chatState.thinking = false
  chatState.currentMessage = ''
}

export function getThinking() {
  return chatState.thinking
}

export default {
  sendMessage,
  getMessages,
  getCurrentMessage,
  setCurrentMessage,
  clearMessages,
  getThinking,
  messageCount
}
