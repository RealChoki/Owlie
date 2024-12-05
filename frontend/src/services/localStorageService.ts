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
  messageCount: { key: "messageCount", defaultValue: 0 },
  currentModule: {
    key: "currentModule",
    defaultValue: "Grundlagen der Programmierung",
  },
  currentMode: { key: "currentMode", defaultValue: "general" },
  selectedModule: {
    key: "selectedModule",
    defaultValue: "Grundlagen der Programmierung",
  },
  assistantId: { key: "assistant_id", defaultValue: null },
  threadId: { key: "thread_id", defaultValue: null },
  vectorStoreId: { key: "vector_store_id", defaultValue: null },
};

// Heart Count
export const getHeartCountLS = () =>
  localStorageUtils.get(keys.heartCount.key, keys.heartCount.defaultValue);
export const setHeartCountLS = (value: number) =>
  localStorageUtils.set(keys.heartCount.key, value);

// Message Count
export const getMessageCountLS = () =>
  localStorageUtils.get(keys.messageCount.key, keys.messageCount.defaultValue);
export const setMessageCountLS = (value: number) =>
  localStorageUtils.set(keys.messageCount.key, value);

// Current Module
export const getCurrentModuleLS = () =>
  localStorageUtils.get(
    keys.currentModule.key,
    keys.currentModule.defaultValue
  );
export const setCurrentModuleLS = (module: string | null) =>
  localStorageUtils.set(keys.currentModule.key, module);

// Current Mode
export const getCurrentModeLS = () =>
  localStorageUtils.get(keys.currentMode.key, keys.currentMode.defaultValue);
export const setCurrentModeLS = (mode: string | null) =>
  localStorageUtils.set(keys.currentMode.key, mode);

// Selected Module
export const getSelectedModuleLS = () =>
  localStorageUtils.get(
    keys.selectedModule.key,
    keys.selectedModule.defaultValue
  );
export const setSelectedModuleLS = (module: string | null) =>
  localStorageUtils.set(keys.selectedModule.key, module);

// Assistant ID
export const getAssistantIdLS = () =>
  localStorageUtils.get(keys.assistantId.key, keys.assistantId.defaultValue);
export const setAssistantIdLS = (value: string) =>
  localStorageUtils.set(keys.assistantId.key, value);

// Thread ID
export const getThreadIdLS = () =>
    localStorageUtils.get(keys.threadId.key, keys.threadId.defaultValue);
export const setThreadIdLS = (value: string) =>
  localStorageUtils.set(keys.threadId.key, value);
export const removeThreadIdLS = () =>
    localStorageUtils.remove(keys.threadId.key);

// Vector Store ID
export const getVectorStoreIdLS = () =>
  localStorageUtils.get(
    keys.vectorStoreId.key,
    keys.vectorStoreId.defaultValue
  );
export const setVectorStoreIdLS = (value: string) =>
  localStorageUtils.set(keys.vectorStoreId.key, value);

// Utility to remove an item if needed
export const removeLocalStorageItem = localStorageUtils.remove;
