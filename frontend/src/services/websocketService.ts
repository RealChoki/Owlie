const websocketUrl = "ws://localhost:8000/ws";

let socket: WebSocket | null = null;
let messageCallback: ((data: string) => void) | null = null;

// Initialize WebSocket connection
function connectWebSocket(url = websocketUrl) {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    socket = new WebSocket(url);

    socket.onmessage = (event) => {
      if (messageCallback) {
        messageCallback(event.data);
      }
    };

    socket.onopen = () => {
      console.log("WebSocket connected!");
    };


    socket.onclose = () => {
      console.log("WebSocket closed.");
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }
}

// Send a message over WebSocket
function sendMessage(message: string) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(message);
  } else {
    console.error("WebSocket is not open.");
  }
}

// Subscribe to WebSocket messages
function onMessage(callback: (data: string) => void) {
  messageCallback = callback; // Replace previous callback
}

function offMessage() {
  messageCallback = null; // Clear callback
}

export default {
  connectWebSocket,
  sendMessage,
  onMessage,
  offMessage,
};