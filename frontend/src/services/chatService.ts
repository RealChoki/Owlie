import { reactive, ref } from 'vue';
import axios from 'axios';

const chatState = reactive({
  messages: [] as { content: string; role: string; id?: string}[],
  currentMessage: '' as string
});

export const messageCount = ref(0);
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
}(0);


export async function sendMessage(messageToSend: string) {
  if (messageToSend.trim()) {
    try {
      // Create a new user message object
      const userMessage = {
        content: messageToSend,
        role: 'user',
      };
      console.log(userMessage)

      // Save the user's message in the chat state
      chatState.messages.push(userMessage);
      chatState.currentMessage = '';
      messageCount.value += 1; // Increment message count

      const threadData = localStorage.getItem('newThreadData');
      let threadId = '';
      if (threadData) {
        try {
          const parsedData = JSON.parse(threadData);
          threadId = parsedData.thread_id;
        } catch (error) {
          console.error('Error parsing thread data from localStorage:', error);
        }
      }
      if (!threadId) {
        throw new Error('Thread ID not found in localStorage');
      }

      const response = await axios.post(`http://localhost:8000/api/threads/thread_kTRd04hCNoBqIkbyQK2Pxixm/run_and_get_latest`, {
        content: messageToSend
      });

      console.log(response.data.latest_message.content)
      const assistantMessage = {
        content: response.data.latest_message.content,
        role: 'assistant',
      };

      chatState.messages.push(assistantMessage);
    } catch (error) {
      console.error('Error sending message:', error);
    }
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

export function clearMessages() {
  chatState.messages.length = 0;
  messageCount.value = 0;
}

export default {
  sendMessage,
  getMessages,
  getCurrentMessage,
  setCurrentMessage,
  clearMessages
};
