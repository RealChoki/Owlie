import { reactive, ref, watch } from 'vue';

const assistant = reactive({
    id: '',
    threadId: '',
    courseName: '',
    modeName: '',
});

const defaultValues = {
    id: '',
    threadId: '',
    courseName: 'Grundlagen der Programmierung',
    modeName: 'general',
};

const oldAssistantId = ref('');

function updateAssistant(newId: string, newCourseName: string, newModeName: string) {
    assistant.id = newId;
    assistant.courseName = newCourseName;
    assistant.modeName = newModeName;
}

function getAssistant() {
    return assistant;
}

function getAssistantId() {
    return assistant.id;
}

function setAssistantId(newId: string) {
    assistant.id = newId;
}

function setAssistantThreadId(newThreadId: string) {
    assistant.threadId = newThreadId;
}

function getAssistantThreadId() {
    return assistant.threadId;
}

// Function to reset assistantId
function resetAssistant() {
    assistant.id = '';
    assistant.courseName = '';
    assistant.modeName = '';
    assistant.threadId = '';
}

function getOldAssistantId() {
    return oldAssistantId.value;
}

function setNewAssistantIdAndSetOldAssistantId(newId: string) {
    oldAssistantId.value = assistant.id;
    assistant.id = newId;
}

function deleteOldAssistantIdAndUpdateAssistantId() {
    assistant.id = oldAssistantId.value;
    oldAssistantId.value = '';
}

function removeAssistantThreadId(){
    assistant.threadId = '';
}

function getAssistantCourseName() {
    if (!assistant.courseName) {
        return defaultValues.courseName;
    }
    return assistant.courseName;
}

function setAssistantCourseName(newCourseName: string) {
    assistant.courseName = newCourseName;
}

function getAssistantModeName() {
    if (!assistant.modeName) {
        return defaultValues.modeName;
    }
    return assistant.modeName;
}

function setAssistantModeName(newModeName: string) {
    assistant.modeName = newModeName;
}

// Watcher to log changes to assistantId
watch(assistant, (newVal, oldVal) => {
    console.log('assistant changed from', oldVal, 'to', newVal);
});

export {
    assistant,
    oldAssistantId,
    updateAssistant,
    resetAssistant,
    setAssistantThreadId,
    getAssistant,
    setAssistantId,
    getOldAssistantId,
    setNewAssistantIdAndSetOldAssistantId,
    deleteOldAssistantIdAndUpdateAssistantId,
    removeAssistantThreadId,
    getAssistantId,
    getAssistantThreadId,
    getAssistantModeName,
    getAssistantCourseName,
    setAssistantCourseName,
    setAssistantModeName,
};
