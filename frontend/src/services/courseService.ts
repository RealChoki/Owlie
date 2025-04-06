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
    "Rechnernetze", 
    "Einführung in die BWL und VWL", 
    "Einführung in die Wirtschaftsinformatik", 
    "Grundlagen des Software-Engineering", 
    "Mathematik", 
    "Angewandte Programmierung", 
    "Datenmodellierung und Datenbanksysteme", 
    "Unternehmens- und Personalmanagement", 
    "Buchführung und Bilanzen", 
    "Grundlagen Projektmanagement", 
    "Geschäftsprozesse und betriebliche Anwendungen", 
    "Webtechnologien", 
    "Datenbanktechnologien", 
    "Controlling", 
    "Modellierung von Anwendungssystemen", 
    "Statistik", 
    "Fremdsprache", 
    "Investition und Finanzierung", 
    "Wahlpflichtmodul Soft Skills", 
    "Fachpraktikum", 
    "Seminar zum Fachpraktikum", 
    "Verteilte Anwendungen", 
    "Produktionswirtschaft/Logistik", 
    "Unternehmenssoftware", 
    "Wahlpflichtmodul Informatik", 
    "Wahlpflichtmodul Ausgewählte Themen der BWL", 
    "AWE-Modul 1", 
    "Fremdsprache", 
    "Bachelorarbeit", 
    "Bachelorseminar/ Abschlusskolloquium", 
    "Wahlpflichtmodul Wirtschaftsinformatik", 
    "Wahlpflichtmodul Ausgewählte Themen der Wirtschaftsinformatik", 
    "AWE-Modul 2"
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
