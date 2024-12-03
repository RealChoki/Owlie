import { ref, watch, type Ref } from 'vue';
import { createNewThread, fetchThread } from "../api/restService";
import { runFinishedStates } from "./constants";
import type { RunStatus, Thread, ThreadMessage, CreateThreadResponse } from "../api/restService";

export const useThread = (
  run: Ref<RunStatus | undefined>,
  setRun: (data: RunStatus | undefined) => void
) => {
  const threadId = ref<string | undefined>(undefined);
  const thread = ref<Thread | undefined>(undefined);
  const actionMessages = ref<ThreadMessage[]>([]);
  const messages = ref<ThreadMessage[]>([]);

  // onMounted(() => {
  //   if (threadId.value === undefined) {
  //     const localThreadId = localStorage.getItem("thread_id");
  //     if (localThreadId) {
  //       console.log(`Resuming thread ${localThreadId}`);
  //       threadId.value = localThreadId;
  //       fetchThread(localThreadId).then(data => {
  //         if (data) {
  //           thread.value = data;
  //         }
  //       });
  //     } else {
  //       console.log("Creating new thread");
  //       createNewThread().then((data: CreateThreadResponse | undefined) => {
  //         if (data) {
  //           setRun(data);
  //           threadId.value = data.thread_id;
  //           localStorage.setItem("thread_id", data.thread_id);
  //           console.log(`Created new thread ${data.thread_id}`);
  //         }
  //       });
  //     }
  //   }
  // });

  const initializeThread = async () => {
    threadId.value = undefined; // Reset threadId to force new thread creation
    const assistant_id = localStorage.getItem('assistant_id');
    if (!assistant_id) {
      console.error('Assistant ID is not available.');
      return;
    }

    console.log("Creating new thread");
    const data: CreateThreadResponse | undefined = await createNewThread();
    if (data) {
      setRun(data);
      threadId.value = data.thread_id;
      localStorage.setItem("thread_id", data.thread_id);
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
    localStorage.removeItem("thread_id");
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