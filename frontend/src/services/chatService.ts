import { reactive, ref, watch } from 'vue';
import axios from 'axios';
import { 
  getHeartCountLS,
  setHeartCountLS,
  getMessageCountLS,
  setMessageCountLS
} from '../services/localStorageService';

import { getAssistantId, getAssistantThreadId } from '../services/openaiService';

// Reactive state
const chatState = reactive({
  messages: [] as { content: string; role: string; id?: string }[],
  currentMessage: '' as string,
  thinking: false as boolean,
  currentThreadId: '' as string,
});

// Reactive references
export const heartCount = ref(getHeartCountLS());
export const messageCount = ref(getMessageCountLS());

// Watchers to update local storage
watch(heartCount, (newValue) => {
  setHeartCountLS(newValue);
});

watch(messageCount, (newValue) => {
  setMessageCountLS(newValue);
});

// No hearts messages
const noHeartsMessages = [
  "Zzzz... schnarch",
  "Ich bin gleich wieder da. Nur ein kurzes Nickerchen... zzzz...",
  "Was für eine wundervolle... zzz... Frage...",
  "Hoot. Ich bin gerade ein bisschen müde... zzzz...",
  "Zzzz... Oh, hast du mich geweckt? Nein, nein, alles gut. Hoot. Nur ein kleines Augenzwinkern... zzzz...",
  "Flügel ausstrecken, Kopf ins Gefieder, und... zzzz...",
  "Hoot. So ein schöner Mond heute, aber... zzzz...",
  "Psst. Ich bin eine Eule, Nachtaktivität ist meine Stärke... normalerweise... hoot... aber manchmal... schnarch zzzz..."
];

// Utility functions
function getRandomNoHeartsMessage() {
  const randomIndex = Math.floor(Math.random() * noHeartsMessages.length);
  return noHeartsMessages[randomIndex];
}

function resetCounts() {
  heartCount.value = 5;
  messageCount.value = 0;
  setHeartCountLS(heartCount.value);
  setMessageCountLS(messageCount.value);
}

async function sendToThread(content: string) {
  const assistant_id = getAssistantId();
  if (!assistant_id) {
    throw new Error('Assistant ID not found.');
  }
   
  const threadId = getAssistantThreadId();
  if (!threadId) {
    throw new Error(`Thread ID not found in assistantService. id: ${threadId}`);
  }

  chatState.currentThreadId = threadId;

  const response = await axios.post(`http://localhost:8000/api/threads/${threadId}/send_and_wait`, {
    content,
    assistant_id,
  });

  console.log('Received response:', response);

  if (getAssistantThreadId() == chatState.currentThreadId) {
    addAssistantMessage(response.data.content);
  } else {
    console.log('Received message from old thread. Ignoring.');
  }
}

function handleSendMessageError(error: any) {
  console.error('Error sending message:', error);
  addAssistantMessage('An error occurred. Please try again later.');
}

// Message handling functions
function addUserMessage(content: string) {
  chatState.messages.push({ content, role: 'user' });
  chatState.currentMessage = '';
}

function addAssistantMessage(content: string) {
  chatState.messages.push({ content, role: 'assistant' });
}

function incrementMessageCount() {
  messageCount.value += 1;
}

function consumeHalfHeart() {
  heartCount.value = Math.max(heartCount.value - 0.5, 0);
  messageCount.value = 0;
  console.log(`[sendMessage] Consumed half a heart. New heartCount: ${heartCount.value}`);
}

// Exported functions
export async function sendMessage(messageToSend: string) {
  console.log(`[sendMessage] Attempting to send message. Current heartCount: ${heartCount.value}, messageCount: ${messageCount.value}`);

  if (!messageToSend.trim()) {
    return;
  }

  addUserMessage(messageToSend);

  if (heartCount.value <= 0) {
    addAssistantMessage(getRandomNoHeartsMessage());
    return;
  }

  incrementMessageCount();

  if (messageCount.value >= 2) {
    consumeHalfHeart();
  }

  chatState.thinking = true;

  try {
    await sendToThread(messageToSend);
  } catch (error) {
    handleSendMessageError(error);
  } finally {
    chatState.thinking = false;
  }
}

export function getMessages() {
  return chatState.messages;
}

export function getCurrentMessage() {
  return chatState.currentMessage;
}

export function setCurrentMessage(newMessage: string) {
  chatState.currentMessage = newMessage;
}

export function clearMessages(resetCount: boolean = true) {
  chatState.messages.length = 0;
  if (resetCount) {
    resetCounts();
  }
  chatState.thinking = false;
  chatState.currentMessage = "";
}

export function getThinking() {
  return chatState.thinking;
}

export default {
  sendMessage,
  getMessages,
  getCurrentMessage,
  setCurrentMessage,
  clearMessages,
  getThinking,
  messageCount,
};