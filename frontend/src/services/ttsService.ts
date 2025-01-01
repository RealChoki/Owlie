import { ref } from "vue";
import { franc } from "franc-min";
import { getMessages } from "../services/chatService";

const availableVoices = ref<SpeechSynthesisVoice[]>([]);
const isTTSPlaying = ref(false);
let utterance: SpeechSynthesisUtterance | null = null;

const femaleVoicesMap: { [key: string]: string } = {
    "en-US": "Microsoft Zira - English (United States)",
    "de-DE": "Microsoft Katja - German (Germany)",
    "fr-FR": "Microsoft Hortense - French (France)",
    "es-ES": "Microsoft Helena - Spanish (Spain)",
  };

const loadVoices = () => {
    availableVoices.value = window.speechSynthesis.getVoices();
  };

  function detectLanguage(text: string): string {
    const langCode = franc(text, { only: ["deu", "eng", "fra", "spa"] });
    console.log("Detected language code:", langCode);
  
    switch (langCode) {
      case "deu":
        return "de-DE";
      case "eng":
        return "en-US";
      case "fra":
        return "fr-FR";
      case "spa":
        return "es-ES";
      default:
        console.warn(
          `Language detection failed for text: "${text}". Defaulting to 'de-DE'.`
        );
        return "de-DE"; // Fallback language
    }
  }

  function readLatestAssistantMessage() {
    if (!isTTSPlaying.value) {
      console.log("readLatestAssistantMessage called");
      const messages = getMessages();
      const assistantMessages = messages.filter(
        (message) => message.role === "assistant"
      );
      console.log("Assistant Messages:", assistantMessages);
      if (assistantMessages.length > 0) {
        const latestMessage = assistantMessages[assistantMessages.length - 1];
        console.log("Latest Assistant Message:", latestMessage.content);
        const detectedLang = detectLanguage(latestMessage.content);
        console.log("Detected Language:", detectedLang);
  
        utterance = new SpeechSynthesisUtterance(latestMessage.content);
  
        // Set language based on detection
        utterance.lang = detectedLang;
        utterance.pitch = 1.1;
        utterance.rate = 1.3;
        utterance.volume = 1;
  
        // Log available voices
        console.log(
          "Available Voices:",
          availableVoices.value.map((voice) => voice.name)
        );
  
        // Select female voice based on detected language
        const selectedVoiceName = femaleVoicesMap[detectedLang];
        const selectedVoice = availableVoices.value.find(
          (voice) => voice.name === selectedVoiceName
        );
  
        if (selectedVoice) {
          utterance.voice = selectedVoice;
          console.log("Selected voice:", selectedVoice.name);
        } else {
          console.warn(
            `No female voice found for language ${detectedLang}. Using default voice.`
          );
        }
  
        utterance.onend = () => {
          isTTSPlaying.value = false;
          console.log("TTS playback ended.");
        };
  
        window.speechSynthesis.cancel(); // Clear any pending speeches
        window.speechSynthesis.speak(utterance);
        isTTSPlaying.value = true;
        console.log("TTS playback started.");
      } else {
        console.log("No assistant messages to read.");
      }
    }
  }

  function stopTTS() {
    if (utterance) {
      window.speechSynthesis.cancel();
      isTTSPlaying.value = false;
      console.log("TTS stopped");
    }
  }
  
  function toggleTTS() {
    if (isTTSPlaying.value) {
      stopTTS();
    } else {
      readLatestAssistantMessage();
    }
  }

export { loadVoices, readLatestAssistantMessage, stopTTS, toggleTTS, availableVoices, isTTSPlaying };
