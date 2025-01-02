import filesService from '../services/filesService';
import { ref, watch, type Ref } from 'vue';
import { createNewThread, fetchThread } from "../api/restService";
import { runFinishedStates } from "./constants";
import type { RunStatus, Thread, ThreadMessage, CreateThreadResponse } from "../api/restService";
import { getAssistantId ,setAssistantThreadId, removeAssistantThreadId, getAssistantThreadId } from '../services/openaiService';
import { getThreadIdLS, setOldThreadIdLS } from '../services/localStorageService';

export const useThread = (
  run: Ref<RunStatus | undefined>,
  setRun: (data: RunStatus | undefined) => void
) => {
  const threadId = ref<string | undefined>(undefined);
  const thread = ref<Thread | undefined>(undefined);
  const actionMessages = ref<ThreadMessage[]>([]);
  const messages = ref<ThreadMessage[]>([]);

  const initializeThread = async () => {
    threadId.value = undefined; // Reset threadId to force new thread creation
    const assistant_id = getAssistantId();
    if (!assistant_id) {
      console.error('Assistant ID is not available.');
      return;
    }

    const data: CreateThreadResponse | undefined = await createNewThread();
    if (data) {
      setRun(data);
      threadId.value = data.thread_id;
      setAssistantThreadId(data.thread_id)
      console.log(getAssistantThreadId());
      console.log(`Created new thread ${data.thread_id}`);
    }
  };

  watch(run, () => {
    if (!run.value || !runFinishedStates.includes(run.value.status ?? "completed")) {
      return;
    }

    console.log(`Retrieving thread ${run.value.thread_id}`);
    fetchThread(run.value.thread_id).then(threadData => {
      if (threadData) {
        thread.value = threadData;
      }
    });
  });

  watch([thread, actionMessages], () => {
    if (!thread.value) {
      return;
    }
    console.log(`Transforming thread into messages`);

    let newMessages = [...thread.value.messages, ...actionMessages.value]
      .sort((a, b) => a.created_at - b.created_at)
      .filter(message => message.hidden !== true);
    messages.value = newMessages;
  });

  const setActionMessages = (newMessages: ThreadMessage[]) => {
    actionMessages.value = newMessages;
  };
  
  const clearThread = () => {
    setOldThreadIdLS(getThreadIdLS());
    filesService.resetFileService();
    removeAssistantThreadId();
    threadId.value = undefined;
    thread.value = undefined;
    setRun(undefined);
    messages.value = [];
    actionMessages.value = [];
    console.log("Thread has been cleared");
  };

  return {
    initializeThread,
    threadId,
    messages,
    actionMessages,
    setActionMessages,
    clearThread
  };
};