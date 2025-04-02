const localStorageUtils = {
  get: (key: string, defaultValue: any = null) => {
    const item = localStorage.getItem(key);
    if (item === null) {
      return defaultValue;
    }

    try {
      return JSON.parse(item);
    } catch (error) {
      console.warn(
        `Failed to parse JSON for key "${key}". Returning the raw value.`
      );
      return item;
    }
  },
  set: (key: string, value: any) => {
    localStorage.setItem(key, JSON.stringify(value));
  },
  remove: (key: string) => {
    localStorage.removeItem(key);
  },
};

// Keys and default values
const keys = {
  heartCount: { key: "heartCount", defaultValue: 5 },
  userMessageTokens: { key: "userMessageTokens", defaultValue: 10000 },
  currentCourse: {
    key: "currentCourse",
    defaultValue: "Grundlagen der Programmierung",
  },
  currentMode: { key: "currentMode", defaultValue: "general" },
  selectedCourse: {
    key: "selectedCourse",
    defaultValue: "Grundlagen der Programmierung",
  },
  assistantId: { key: "assistant_id", defaultValue: null },
  oldAssistantId: { key: "old_assistant_id", defaultValue: null },
  threadId: { key: "thread_id", defaultValue: null },
  oldThreadId: { key: "old_thread_id", defaultValue: null },
  theme: { key: "theme", defaultValue: "dark" },
  language: { key: "language", defaultValue: "de" },
};

// Selected Theme
export const setThemeLS = (theme: string) =>
  localStorageUtils.set(keys.theme.key, theme);

export const getThemeLS = () =>
  localStorageUtils.get(keys.theme.key, keys.theme.defaultValue);

// Selected Language
export const setLanguageLS = (language: string) =>
  localStorageUtils.set(keys.language.key, language);

export const getLanguageLS = () =>
  localStorageUtils.get(keys.language.key, keys.language.defaultValue);


// Heart Count
export const getHeartCountLS = () =>
  localStorageUtils.get(keys.heartCount.key, keys.heartCount.defaultValue);
export const setHeartCountLS = (value: number) =>
  localStorageUtils.set(keys.heartCount.key, value);

// Message Count
export const getUserMessageTokensLS = () =>
  localStorageUtils.get(keys.userMessageTokens.key, keys.userMessageTokens.defaultValue);
export const setUserMessageTokensLS = (value: number) =>
  localStorageUtils.set(keys.userMessageTokens.key, value);

// Current Course
export const getCurrentCourseLS = () =>
  localStorageUtils.get(
    keys.currentCourse.key,
    keys.currentCourse.defaultValue
  );
export const setCurrentCourseLS = (course: string | null) =>
  localStorageUtils.set(keys.currentCourse.key, course);

// Current Mode
export const getCurrentModeLS = () =>
  localStorageUtils.get(keys.currentMode.key, keys.currentMode.defaultValue);
export const setCurrentModeLS = (mode: string | null) =>
  localStorageUtils.set(keys.currentMode.key, mode);

// Selected Course
export const getSelectedCourseLS = () =>
  localStorageUtils.get(
    keys.selectedCourse.key,
    keys.selectedCourse.defaultValue
  );
export const setSelectedCourseLS = (course: string | null) =>
  localStorageUtils.set(keys.selectedCourse.key, course);

// Assistant ID
export const getAssistantIdLS = () =>
  localStorageUtils.get(keys.assistantId.key, keys.assistantId.defaultValue);
export const setAssistantIdLS = (value: string) =>
  localStorageUtils.set(keys.assistantId.key, value);
export const removeAssistantIdLS = () =>
  localStorageUtils.remove(keys.assistantId.key);

// Old / Main Assistant ID (to hold the original assistant ID)
export const getOldAssistantIdLS = () => localStorageUtils.get(keys.oldAssistantId.key, keys.oldAssistantId.defaultValue);
export const setOldAssistantIdLS = (value: string) =>
  localStorageUtils.set(keys.oldAssistantId.key, value);
export const removeOldAssistantIdLS = () =>
  localStorageUtils.remove(keys.oldAssistantId.key);

// Thread ID
export const getThreadIdLS = () =>
    localStorageUtils.get(keys.threadId.key, keys.threadId.defaultValue);
export const setThreadIdLS = (value: string) =>
  localStorageUtils.set(keys.threadId.key, value);
export const removeThreadIdLS = () =>
    localStorageUtils.remove(keys.threadId.key);

export const getOldThreadIdLS = () =>
    localStorageUtils.get(keys.oldThreadId.key, keys.oldThreadId.defaultValue);
export const setOldThreadIdLS = (value: string) =>
    localStorageUtils.set(keys.oldThreadId.key, value);
export const removeOldThreadIdLS = () =>
    localStorageUtils.remove(keys.oldThreadId.key);

// Utility to remove an item if needed
export const removeLocalStorageItem = localStorageUtils.remove;
