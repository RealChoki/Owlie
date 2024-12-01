import { reactive, ref, watch } from 'vue';
import axios from 'axios';

const chatState = reactive({
  messages: [] as { content: string; role: string; id?: string }[],
  currentMessage: '' as string,
  thinking: false as boolean,
});

export const heartCount = ref(5); // Initialize with total hearts
export const messageCount = ref(0); // Track number of user messages

const storedHeartCount = localStorage.getItem('heartCount');
if (storedHeartCount !== null) {
  heartCount.value = parseFloat(storedHeartCount);
} else {
  heartCount.value = 5;
}

const storedMessageCount = localStorage.getItem('messageCount');
if (storedMessageCount !== null) {
  messageCount.value = parseInt(storedMessageCount, 10);
} else {
  messageCount.value = 0;
}

watch(heartCount, (newValue) => {
  localStorage.setItem('heartCount', newValue.toString());
});

watch(messageCount, (newValue) => {
  localStorage.setItem('messageCount', newValue.toString());
});

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

function getRandomNoHeartsMessage() {
  const randomIndex = Math.floor(Math.random() * noHeartsMessages.length);
  return noHeartsMessages[randomIndex];
}

export async function sendMessage(messageToSend: string) {
  console.log(`[sendMessage] Attempting to send message. Current heartCount: ${heartCount.value}, messageCount: ${messageCount.value}`);

  if (!messageToSend.trim()) {
    return;
  }

  // Save the user's message in the chat state
  const userMessage = {
    content: messageToSend,
    role: 'user',
  };
  chatState.messages.push(userMessage);
  chatState.currentMessage = '';

  if (heartCount.value <= 0) {
    console.log(`[sendMessage] No hearts left. Sending noHeartsMessage.`);
    // If no hearts left, respond with a random noHeartsMessage
    const assistantMessage = {
      content: getRandomNoHeartsMessage(),
      role: 'assistant',
    };
    chatState.messages.push(assistantMessage);
    return;
  }

  messageCount.value += 1; // Increment message count

  // Check if 3 messages have been sent to consume half a heart
  if (messageCount.value >= 3) {
    heartCount.value -= 0.5; // Consume half a heart
    messageCount.value = 0; // Reset message count
    console.log(`[sendMessage] Consumed half a heart. New heartCount: ${heartCount.value}`);
    
    // Ensure heartCount doesn't go negative
    if (heartCount.value < 0) {
      heartCount.value = 0;
    }
  }

  chatState.thinking = true;

  try {
    const threadId = localStorage.getItem('thread_id');
    if (!threadId) {
      throw new Error('Thread ID not found in localStorage');
    }

    console.log('Sending message to thread:', threadId);
    const response = await axios.post(`http://localhost:8000/api/threads/${threadId}/send_and_wait`, {
      content: messageToSend,
    });

    const assistantMessage = {
      content: response.data.content,
      role: 'assistant',
    };
    chatState.messages.push(assistantMessage);
    console.log(`[sendMessage] Assistant responded. Current heartCount: ${heartCount.value}`);
  } catch (error) {
    console.error('Error sending message:', error);
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
    heartCount.value = 5; // Reset to total hearts
    messageCount.value = 0; // Reset message count
    localStorage.setItem('heartCount', heartCount.value.toString());
    localStorage.setItem('messageCount', messageCount.value.toString());
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
  messageCount, // Exporting messageCount
};
