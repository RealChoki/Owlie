import { reactive, ref, watch } from 'vue';
import {
    getCurrentCourseLS,
    setCurrentCourseLS,
    getCurrentModeLS,
    setCurrentModeLS,
    getAssistantIdLS,
    setAssistantIdLS,
    removeAssistantIdLS,
    getThreadIdLS,
    setThreadIdLS,
    removeThreadIdLS,
    setOldAssistantIdLS,
    removeOldAssistantIdLS,
} from './localStorageService';

// Reactive state for assistant
const assistant = reactive({
    id: getAssistantIdLS() || '',
    threadId: getThreadIdLS() || '',
    courseName: getCurrentCourseLS(),
    modeName: getCurrentModeLS(),
});

const oldAssistantId = ref('');

// Assistant management functions
function updateAssistant(newId: string, newCourseName: string, newModeName: string) {
    assistant.id = newId;
    assistant.courseName = newCourseName;
    assistant.modeName = newModeName;
    setAssistantIdLS(newId);
    setCurrentCourseLS(newCourseName);
    setCurrentModeLS(newModeName);
}

function resetAssistant() {
    assistant.id = '';
    assistant.courseName = '';
    assistant.modeName = '';
    assistant.threadId = '';
    removeAssistantIdLS();
    removeThreadIdLS();
    removeOldAssistantIdLS();
}

function getAssistant() {
    return assistant;
}

// Assistant ID management functions
function setAssistantId(newId: string) {
    assistant.id = newId;
    setAssistantIdLS(newId);
}

function getAssistantId() {
    return assistant.id;
}

function getOldAssistantId() {
    return oldAssistantId.value;
}

function updateAssistantIdAndStoreOldId(newId: string) {
    oldAssistantId.value = assistant.id;
    assistant.id = newId;
    setOldAssistantIdLS(assistant.id);
    setAssistantIdLS(newId);
}

function restoreOldAssistantId() {
    assistant.id = oldAssistantId.value;
    oldAssistantId.value = '';
    setAssistantIdLS(oldAssistantId.value);
    removeOldAssistantIdLS();
}

// Assistant thread management functions
function setAssistantThreadId(newThreadId: string) {
    assistant.threadId = newThreadId;
    setThreadIdLS(newThreadId);
}

function getAssistantThreadId() {
    return assistant.threadId;
}

function removeAssistantThreadId() {
    assistant.threadId = '';
    removeThreadIdLS();
}

// Assistant course and mode management functions
function getAssistantCourse() {
    return assistant.courseName;
}

function setAssistantCourse(newCourseName: string) {
    assistant.courseName = newCourseName;
    setCurrentCourseLS(newCourseName);
}

function getAssistantMode() {
    return assistant.modeName;
}

function setAssistantMode(newModeName: string) {
    assistant.modeName = newModeName;
    setCurrentModeLS(newModeName);
}

// Watcher to log changes to assistant
watch(assistant, (newVal, oldVal) => {
    console.log('assistant changed from', oldVal, 'to', newVal);
});

export {
    // Assistant management
    assistant,
    updateAssistant,
    resetAssistant,
    getAssistant,

    // Assistant ID management
    setAssistantId,
    getAssistantId,
    getOldAssistantId,
    updateAssistantIdAndStoreOldId,
    restoreOldAssistantId,

    // Assistant thread management
    setAssistantThreadId,
    getAssistantThreadId,
    removeAssistantThreadId,

    // Assistant mode and course management
    getAssistantMode,
    setAssistantMode,
    getAssistantCourse,
    setAssistantCourse,
};