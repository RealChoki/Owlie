import { reactive, ref } from "vue";

// Define the chat service's state
const chatState = reactive({
  messages: [] as string[],
});

// Make message a reactive ref
const message = ref('');

// Function to add a message (sendMessage)
export function sendMessage(messageToSend: string) {
  if (messageToSend.trim()) {
    chatState.messages.push(messageToSend); // Add the message to chatState.messages
    message.value = ""; // Clear the message input (reactively clear the ref)
  }
}

// Function to update the message state
export function setMessage(newMessage: string) {
  message.value = newMessage; // Set the reactive message value
}

// Function to get the chat messages
export function getMessages() {
  return chatState.messages; // Return the list of messages
}

// Function to get the current input message
export function getMessage() {
  return message.value; // Return the reactive message value
}

// Optional function to clear messages (if needed)
export function clearMessages() {
  chatState.messages.length = 0; // Clear the messages array
}

export function clearMessage() {
  message.value = ""; // Clear the message input (reactively clear the ref)
}

export default {
  sendMessage,
  setMessage,
  getMessages,
  getMessage,
  clearMessages,
};
