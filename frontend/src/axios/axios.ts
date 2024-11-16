import axios from 'axios';

export async function sendMessage(messageToSend: string) {
  if (messageToSend.trim()) {
    try {
      // Send the message to the Fastify backend
      const response = await axios.post('http://localhost:3000/chat', {
        message: messageToSend
      });

      // Process the response as needed
      console.log('Assistant response:', response.data.response);

    } catch (error) {
      console.error('Error sending message:', error);
    }
  }
}
