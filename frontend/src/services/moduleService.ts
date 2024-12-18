import axios from "axios";
import { ref } from "vue";
import { setAssistantIdLS } from "../services/localStorageService";
import { updateAssistant } from "../services/openaiService";

const activeModules = ref<string[]>(["Grundlagen der Programmierung"]);
export const modules = ref<string[]>([]);

export async function fetchModules() {
  try {
    const response = await fetch(
      "http://localhost:8000/api/courses?university=hochschule_fuer_technik_und_wirtschaft_berlin&degree=bachelor&subject=wirtschaftsinformatik"
    );
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    modules.value = data.courses.map((course: string) =>
      course.replace(/_/g, " ")
    );
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
    throw error;
  }
}

export async function fetchAssistantIds(courseName: string, modeName: string) {
  try {
    const response = await axios.get(
      "http://localhost:8000/api/get_assistant_ids",
      {
        params: { course_name: courseName, mode_name: modeName },
      }
    );
    const { assistant_id } = response.data;

    console.log("Assistant ID:", assistant_id);
    if (!assistant_id) {
      throw new Error("Assistant ID or vector store ID not found");
    }

    // setAssistantIdLS(assistant_id);
    updateAssistant(assistant_id, courseName, modeName);

    return response.data; 
  } catch (error) {
    console.error("Error fetching assistant IDs:", error);
    throw error;
  }
}

export function isModuleActive(module: string): boolean {
  return activeModules.value.includes(module);
}

export function formatCourseName(module: string): string {
  return module.replace(/ /g, "_").toLowerCase();
}
