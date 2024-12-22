import { ref } from "vue";

const owlDisplayMessage = ref("");
const navbarCourseTitle = ref("");

const setOwlDisplayMessage = (message: string) => {
  owlDisplayMessage.value = message;
};

const setNavbarCourseTitle = (course: string, mode: string) => {
    console.log("Course selected from home view:", course, mode);
    navbarCourseTitle.value = mode !== "general" ? `${course} (${mode})` : course;
};

const clearOwlDisplayMessage = () => {
  owlDisplayMessage.value = "";
};

const clearNavbarCourseTitle = () => {
  navbarCourseTitle.value = "";
};

const displayAssistantNotFountMessage = () => {
    setOwlDisplayMessage("Assistant not found!");
    setTimeout(() => setOwlDisplayMessage("(｡>﹏<)"), 2000);
    setTimeout(() => setOwlDisplayMessage("Assistant not found!"), 4000);
}

export {
  owlDisplayMessage,
  navbarCourseTitle,
  setOwlDisplayMessage,
  setNavbarCourseTitle,
  clearOwlDisplayMessage,
  clearNavbarCourseTitle,
  displayAssistantNotFountMessage,
};
