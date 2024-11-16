import { reactive } from 'vue'
import axios from 'axios'

const chatState = reactive({
  messages: [] as string[],
  currentMessage: '' as string
})

export async function sendMessage(messageToSend: string) {
  if (messageToSend.trim()) {
    try {
      // Save the user's message in the chat state
      chatState.messages.push(messageToSend);
      chatState.currentMessage = '';

      // Send the message to the Fastify backend
      const response = await axios.post('http://localhost:3000/chat', {
        message: messageToSend,
      });

      // Save the assistant's response in the chat state
      chatState.messages.push(response.data.response);

      // Log the assistant response
      console.log('Assistant response:', response.data.response);
    } catch (error) {
      console.error('Error sending message:', error);
    }
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
