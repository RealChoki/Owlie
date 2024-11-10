import { reactive } from 'vue'

const chatState = reactive({
  messages: [] as string[],
  currentMessage: '' as string
})

export function sendMessage(messageToSend: string) {
  if (messageToSend.trim()) {
    chatState.messages.push(messageToSend)
    chatState.currentMessage = ''
  }
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

export function clearMessages() {
  chatState.messages.length = 0
}

export default {
  sendMessage,
  getMessages,
  getCurrentMessage,
  setCurrentMessage,
  clearMessages
}
