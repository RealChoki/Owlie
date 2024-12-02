import { ref, watch, type Ref } from 'vue';
import { runFinishedStates } from "./constants";
import type { RunStatus } from "../api/restService";

export const useRunStatus = (run: Ref<RunStatus | undefined>) => {
    const status = ref<string | undefined>(undefined);
    const processing = ref(false);

    watch(run, () => {
        if (run.value?.status === "in_progress") {
            status.value = "Thinking ...";
        } else if (run.value?.status === "queued") {
            status.value = "Queued ...";
        } else {
            status.value = undefined;
        }

        processing.value = !runFinishedStates.includes(run.value?.status ?? "completed");
    });

    return { status, processing };
};