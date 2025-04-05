import axios from "axios";
import { ref } from "vue";
import { updateAssistant } from "./openaiService";
import { setOwlDisplayMessage, clearOwlDisplayMessage, displayAssistantNotFountMessage } from "./homeService";

const activeCourses = ref<string[]>(["Grundlagen der Programmierung"]);
export const courses = ref<string[]>([]);

export async function fetchCourses() {
  // try {
  //   const response = await fetch(
  //     "http://localhost:8000/api/courses?university=hochschule_fuer_technik_und_wirtschaft_berlin&degree=bachelor&subject=wirtschaftsinformatik"
  //   );
  //   if (!response.ok) {
  //     throw new Error("Network response was not ok");
  //   }
  //   const data = await response.json();
  //   courses.value = data.courses.map((course: string) =>
  //     course.replace(/_/g, " ")
  //   );
  //   // temp for /quiz
  //   localStorage.setItem("courses", JSON.stringify(courses.value));
  // } catch (error) {
  //   console.error("There has been a problem with your fetch operation:", error);
  //   throw error;
  // }

  courses.value = [
    "Grundlagen der Programmierung",
    "Statistics",
    "Software Engineering"
  ];
}

export async function fetchAssistantIds(courseName: string, modeName: string) {
  try {
    setOwlDisplayMessage("Fetching assistant...");
    const response = await axios.get(
      "http://localhost:8000/api/get_assistant_ids",
      {
        params: { course_name: courseName.replace(/ /g, "_"), mode_name: modeName },
      }
    );
    const { assistant_id } = response.data;

    console.log("Assistant ID:", assistant_id);
    if (!assistant_id) {
      throw new Error("Assistant ID not found");
    }

    updateAssistant(assistant_id, courseName, modeName);
    setOwlDisplayMessage("Assistant found");
    setTimeout(() => clearOwlDisplayMessage(), 1000);
    return response.data; 
  } catch (error) {
    console.error("Error fetching assistant IDs:", error);
    displayAssistantNotFountMessage();
    throw error;
  }
}

export function isCourseActive(course: string): boolean {
  return activeCourses.value.includes(course);
}

export function formatCourseName(course: string): string {
  return course.replace(/ /g, "_").toLowerCase();
}
