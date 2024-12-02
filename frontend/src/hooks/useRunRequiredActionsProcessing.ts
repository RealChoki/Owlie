import { watch, type Ref } from 'vue';
import { postToolResponse } from "../api/restService";
import type { RunStatus, ToolOutput, ThreadMessage, PostToolResponse } from "../api/restService";

export const useRunRequiredActionsProcessing = (
  run: Ref<RunStatus | undefined>,
  setRun: (data: RunStatus) => void,
  setActionMessages: (messages: ThreadMessage[]) => void
) => {
  watch(run, () => {
    if (run.value?.status === "requires_action") {
      let response: ToolOutput[] = [];
      let actionMessages: ThreadMessage[] = [];
      for (const tool_call of run.value.required_action?.submit_tool_outputs?.tool_calls || []) {
        if (tool_call.function.name === "get_moodle_course_content") {
          response.push({
            tool_id: tool_call.id,
            output: "{'success': true}"
          });

          const courseId = JSON.parse(tool_call.function.arguments).courseid;
          actionMessages.push({
            id: `moodle_content_${courseId}_${Date.now()}`,
            content: `Retrieved Moodle content for course ID: ${courseId}`,
            role: "moodle_content",
            hidden: false,
            created_at: Math.floor(Date.now() / 1000)
          });
        }
      }
      setActionMessages(actionMessages);
      postToolResponse(run.value.thread_id, run.value.run_id, response).then((data: PostToolResponse | undefined) => {
        if (data) {
          setRun(data);
        }
      });
    }
  }, { immediate: true });
};