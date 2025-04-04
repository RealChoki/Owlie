import { computed, reactive, ref, watch } from 'vue'
import { getHeartCountLS, setHeartCountLS, getUserMessageTokensLS, setUserMessageTokensLS } from '../services/localStorageService'

import { getAssistantId, getAssistantThreadId } from '../services/openaiService'
import websocketService from '../services/websocketService'

// Reactive state
const chatState = reactive({
  messages: [] as { content: string; role: string; index: number; id?: string; isComplete?: boolean }[],
  currentUserInput: '' as string,
  thinking: false as boolean,
  currentThreadId: '' as string,
  currentRunId: '' as string
})

// Reactive references
export const heartCount = ref(getHeartCountLS())
export const userMessageTokens = ref(getUserMessageTokensLS())
export const nextHeartMilestone = ref(Math.floor(userMessageTokens.value / 1000) * 1000);

// Watchers to update local storage
watch(heartCount, (newValue) => {
  setHeartCountLS(newValue)
})

watch(userMessageTokens, (newValue) => {
  setUserMessageTokensLS(newValue)
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
  userMessageTokens.value = 10000
  setHeartCountLS(heartCount.value)
  setUserMessageTokensLS(userMessageTokens.value)
}

// async function sendToThread(content: string) {
//   const assistant_id = getAssistantId();
//   if (!assistant_id) {
//     throw new Error('Assistant ID not found.');
//   }

//   chatState.thinking = true;
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
//   chatState.thinking = false;
// }


async function sendToThread(content: string) {
  const assistant_id = getAssistantId();
  const threadId = getAssistantThreadId();

  if (!assistant_id || !threadId) {
    throw new Error('Assistant ID or Thread ID not found.');
  }

  // Initialize WebSocket connection if not already connected
  websocketService.connectWebSocket();
  chatState.thinking = true;

  // Prepare the initial message for the chat state
  const initialMessage = {
    content: '',
    role: 'assistant',
    index: chatState.messages.length,
    isComplete: false,
  };
  chatState.messages.push(initialMessage);
  const lastMessageIndex = chatState.messages.length - 1;

  // Prepare the payload to send over WebSocket
  const payload = JSON.stringify({
    thread_id: threadId,
    assistant_id: assistant_id,
    message: content,
  });

  // Send the payload to the WebSocket server
  websocketService.sendMessage(payload);

  // Subscribe to WebSocket messages
  websocketService.onMessage((data: string) => {
    try {
      if (data) {
        chatState.thinking = false;
      }
      // Handle the incoming message
      if (data.startsWith('Error:')) {
        // Handle errors from the server
        console.error(data);
        chatState.thinking = false;
        chatState.messages[lastMessageIndex].isComplete = true;
        return;
      }

      if (data === "˘DONE˘") {
        chatState.messages[lastMessageIndex].isComplete = true;
        return;
      }

      // Append the chunk to the last message
      chatState.messages[lastMessageIndex].content += data;
    } catch (error) {
      console.error('Error processing WebSocket message:', error);
      chatState.thinking = false;
      chatState.messages[lastMessageIndex].isComplete = true;
    }
  });
}

// async function sendToThread(content: string) {
//   const assistant_id = getAssistantId()
//   const threadId = getAssistantThreadId()

//   if (!assistant_id || !threadId) {
//     throw new Error('Assistant ID or Thread ID not found.')
//   }

//   chatState.currentThreadId = threadId
//   chatState.thinking = true

//   const url = `http://localhost:8000/api/threads/${threadId}/stream?assistant_id=${assistant_id}&message=${content}`
//   const response = await fetch(url)
//   if (!response.ok) {
//     throw new Error('Failed to connect to the backend')
//   }

//   if (!response.body) {
//     throw new Error('Response body is null')
//   }

//   const reader = response.body.getReader()
//   const decoder = new TextDecoder()
//   let done = false

//   const initialMessage = {
//     content: '',
//     role: 'assistant',
//     index: chatState.messages.length,
//     isComplete: false
//   }
//   chatState.messages.push(initialMessage)
//   const lastMessageIndex = chatState.messages.length - 1

//   let runIdReceived = false
//   chatState.thinking = false


//   while (!done && initialMessage.isComplete === false) {
//     const { value, done: readerDone } = await reader.read()
//     done = readerDone
//     const chunk = decoder.decode(value, { stream: true })

//     if (!runIdReceived && chunk.startsWith("run_id: ")) {
//       const runId = chunk.split(": ")[1].trim()
//       console.log(`Received run_id: ${runId}`)
//       runIdReceived = true
//       chatState.currentRunId = runId
      
//     } else {
//       chatState.messages[lastMessageIndex].content += chunk
//     }
//   }
//   chatState.currentRunId = ''
//   chatState.messages[lastMessageIndex].isComplete = true
// }

export async function cancelAssistantResponse() {
  const lastMessageIndex = chatState.messages.length - 1
  chatState.messages[lastMessageIndex].isComplete = true
  const threadId = getAssistantThreadId();
  const runId = chatState.currentRunId;
  const url = `http://localhost:8000/api/threads/${threadId}/runs/${runId}/cancel`;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const result = await response.json();
    console.log(result.message);
  } catch (error) {
    console.error("Failed to stop the thread:", error);
  }
}

function handleSendMessageError(error: any) {
  console.error('Error sending message:', error)
  addAssistantMessage('An error occurred. Please try again later.')
}

// Message handling functions
function addUserMessage(content: string) {
  chatState.messages.push({ content, role: 'user', index: chatState.messages.length })
  chatState.currentUserInput = ''
}

function addAssistantMessage(content: string) {
  chatState.messages.push({ content, role: 'assistant', index: chatState.messages.length })
}

function consumeHalfHeart() {
  heartCount.value = Math.max(heartCount.value - 0.5, 0)
  console.log(`[sendMessage] Consumed half a heart. New heartCount: ${heartCount.value}`)
}

// Exported functions
export async function sendMessage(
  content: string,
  fileContents?: Array<{ name: string; content: string | ArrayBuffer | null }>
) {
  console.log('[sendMessage] Sending user message and hidden file data')

  addUserMessage(content)

  if (heartCount.value <= 0) {
    addAssistantMessage(getRandomNoHeartsMessage())
    return
  }

  chatState.currentUserInput = ''

  try {
    // Append file content silently
    let payload = content
    if (fileContents && fileContents.length > 0) {
      payload += '\n\n[Hidden File Data]\n'
      fileContents.forEach((file) => {
        payload += `Filename: ${file.name}\nContent:\n${file.content}\n\n`
      })
    }
    console.log('Sending payload:', payload)

    updateTokensAndConsume(payload);

    await sendToThread(payload)
  } catch (error) {
    // handleSendMessageError(error)
  }
}

export async function resendMessage(index: number) {
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
      // handleSendMessageError(error)
    }
  }
}

function deleteMessagesFromIndex(index: number): void {
  chatState.messages.splice(index)
}

export function getMessages() {
  return chatState.messages
}

export const currentUserInput = computed({
  get: getCurrentUserInput,
  set: setCurrentUserInput,
});

export function getCurrentUserInput() {
  return chatState.currentUserInput
}

export function setCurrentUserInput(newMessage: string) {
  chatState.currentUserInput = newMessage
}

export function clearMessages(resetCount: boolean = true) {
  chatState.messages.length = 0
  if (resetCount) {
    resetCounts()
  }
  chatState.thinking = false
  chatState.currentUserInput = ''
}

export const isCurrentAssistantResponseComplete = computed({
  get: getIsCurrentAssistantResponseComplete,
  set: setIsCurrentAssistantResponseComplete
})

function getIsCurrentAssistantResponseComplete() {
  if (chatState.messages.length === 0) {
    return true
  }
  const lastMessage = chatState.messages[chatState.messages.length - 1]
  return lastMessage.isComplete
}

function setIsCurrentAssistantResponseComplete(value: boolean) {
  const lastMessage = chatState.messages[chatState.messages.length - 1]
  lastMessage.isComplete = value
}

export function getThinking() {
  return chatState.thinking
}

export function estimateOpenAITokens(text: string): number {
  return Math.ceil(text.split(/\s+/).join(' ').length * 1.3);
}

function updateTokensAndConsume(payload: string) {
  const tokenUsage = payload.length;
  userMessageTokens.value -= tokenUsage;
  setUserMessageTokensLS(userMessageTokens.value);

  while (userMessageTokens.value < nextHeartMilestone.value) {
    consumeHalfHeart();
    nextHeartMilestone.value -= 1000;
  }

  console.log(`Tokens used: ${tokenUsage}, Remaining tokens: ${userMessageTokens.value}`);
}

export default {
  sendMessage,
  getMessages,
  clearMessages,
  getThinking,
}
