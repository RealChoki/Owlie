import { reactive, ref, watch } from 'vue';

const assistant = reactive({
    id: '',
    courseName: '',
    modeName: '',
    threadId: ''
});

const oldAssistantId = ref('');
const threadId = ref('');

function updateAssistant(newId: string, newCourseName: string, newModeName: string) {
    assistant.id = newId;
    assistant.courseName = newCourseName;
    assistant.modeName = newModeName;
}

function getAssistant() {
    return assistant;
}

function setAssistantId(newId: string) {
    assistant.id = newId;
}

function setAssistantThreadId(newThreadId: string) {
    assistant.threadId = newThreadId;
}

// Function to reset assistantId
function resetAssistant() {
    assistant.id = '';
    assistant.courseName = '';
    assistant.modeName = '';
    assistant.threadId = '';
}

function setNewAssistantIdAndSetOldAssistantId(newId: string) {
    oldAssistantId.value = assistant.id;
    assistant.id = newId;
}

function deleteOldAssistantIdAndUpdateAssistantId() {
    assistant.id = oldAssistantId.value;
    oldAssistantId.value = '';
}

// Function to update threadId
function updateThreadId(newId: string) {
    threadId.value = newId;
}

// Watcher to log changes to assistantId
watch(assistant, (newVal, oldVal) => {
    console.log('assistant changed from', oldVal, 'to', newVal);
});

// Watcher to log changes to threadId
watch(threadId, (newVal, oldVal) => {
    console.log('threadId changed from', oldVal, 'to', newVal);
});


export {
    assistant,
    oldAssistantId,
    threadId,
    updateAssistant,
    resetAssistant,
    updateThreadId,
    setAssistantThreadId,
    getAssistant,
    setAssistantId
};
