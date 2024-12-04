import axios from "axios";
import { ref } from "vue";

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
    const { assistant_id, vector_store_id } = response.data;

    console.log("Assistant ID:", assistant_id);
    console.log("Vector Store ID:", vector_store_id);
    if (!assistant_id || !vector_store_id) {
      throw new Error("Assistant ID or vector store ID not found");
    }
    localStorage.setItem("assistant_id", assistant_id);
    localStorage.setItem("vector_store_id", vector_store_id);

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
