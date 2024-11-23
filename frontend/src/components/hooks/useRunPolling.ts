import { ref, onBeforeUnmount, watch, type Ref } from 'vue';
import { fetchRun } from "../../api/restService";
import type { FetchRunResponse } from "../../api/restService";
import { runFinishedStates } from "./constants";

export const useRunPolling = (
  threadId: Ref<string | undefined>,
  run: Ref<FetchRunResponse | undefined>,
  setRun: (data: FetchRunResponse) => void
) => {
  const pollingTimerRef = ref<number | null>(null);

  const startPolling = async () => {
    if (!run.value) return;
    console.log(`Polling thread ${threadId.value} run ${run.value.run_id}`);
    const data = await fetchRun(threadId.value!, run.value.run_id);
    if (data && (data.run_id !== run.value.run_id || data.status !== run.value.status)) {
      setRun(data);
    }
    pollingTimerRef.value = window.setTimeout(startPolling, 1000);
  };

  const stopPolling = () => {
    if (pollingTimerRef.value !== null) {
      clearTimeout(pollingTimerRef.value);
      pollingTimerRef.value = null;
    }
  };

  watch(run, () => {
    const needsToPoll = run.value && !runFinishedStates.includes(run.value.status ?? "completed");

    if (needsToPoll) {
      startPolling();
    } else {
      stopPolling();
    }
  });

  onBeforeUnmount(() => {
    stopPolling();
  });
};