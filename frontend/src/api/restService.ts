// Core Interfaces

export interface RequiredAction {
    action: string;
    details?: string;
    submit_tool_outputs?: {
        tool_calls: {
            id: string;
            function: {
                name: string;
                arguments: string;
            };
        }[];
    };
}

export interface LastError {
    code: string;
    message: string;
}

// Run Status Interfaces

export interface RunStatus {
    run_id: string;
    thread_id: string;
    status?: string;
    required_action?: RequiredAction;
    last_error?: LastError;
}

// Message and Thread Interfaces

export interface ThreadMessage {
    id: string;
    content: string;
    role: string;
    hidden: boolean;
    created_at: number;
}

export interface Thread {
    messages: ThreadMessage[];
}

// Tool Output Interface

export interface ToolOutput {
    tool_id: string;
    output: string;
}

// Response Interfaces

export interface PostToolResponse extends RunStatus {}

export interface CreateThreadResponse extends RunStatus {}

export interface FetchThreadResponse extends Thread {}

export interface FetchRunResponse extends RunStatus {}

export interface PostMessageResponse extends RunStatus {}

import { getAssistantId } from '../services/openaiService';
import { setOwlDisplayMessage } from '../services/homeService';
import { getOldThreadIdLS } from '@/services/localStorageService';
import i18n from '@/i18n'

const t = i18n.global.t as (...args: any[]) => string;

// REST Service functions
export const createNewThread = async (): Promise<CreateThreadResponse | undefined> => {
    try {
        setOwlDisplayMessage("Creating a new chat...");
        const assistant_id = getAssistantId(); 
        if (!assistant_id) {
            throw new Error('Assistant ID is not available.');
        }

        const old_thread_id = getOldThreadIdLS();

        const response = await fetch("http://localhost:8000/api/new", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ assistant_id, old_thread_id }),
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data: CreateThreadResponse = await response.json();
        setOwlDisplayMessage(t("services.owlDisplayMsg.chatCreated"));
        setTimeout(() => { setOwlDisplayMessage(" (˶˃ ᵕ ˂˶) .ᐟ.ᐟ"); }, 1000);
        setTimeout(() => { setOwlDisplayMessage(""); }, 2000);
        return data;
    } catch (err: any) {
        setOwlDisplayMessage("Failed to create a chat!");
        console.error(err.message);
    }
};

export const fetchThread = async (threadId: string): Promise<FetchThreadResponse | undefined> => {
    try {
        const response = await fetch(`http://localhost:8000/api/threads/${threadId}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data: FetchThreadResponse = await response.json();
        return data;
    } catch (err: any) {
        console.error(err.message);
    }
};

export const fetchRun = async (threadId: string, runId: string): Promise<FetchRunResponse | undefined> => {
    try {
        const response = await fetch(`http://localhost:8000/api/threads/${threadId}/runs/${runId}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data: FetchRunResponse = await response.json();
        return data;
    } catch (err: any) {
        console.error(err.message);
    }
};

export const postMessage = async (threadId: string, message: string): Promise<PostMessageResponse | undefined> => {
    try {
        const response = await fetch(`http://localhost:8000/api/threads/${threadId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ content: message }),
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data: PostMessageResponse = await response.json();
        return data;
    } catch (err: any) {
        console.error(err.message);
    }
};

export const postToolResponse = async (
    threadId: string, 
    runId: string, 
    toolResponses: ToolOutput[]
): Promise<PostToolResponse | undefined> => {
    try {
        const response = await fetch(`http://localhost:8000/api/threads/${threadId}/runs/${runId}/tool`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(toolResponses)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data: PostToolResponse = await response.json();
        return data;
    } catch (err: any) {
        console.error(err.message);
    }
};

export const startWebSocket = (threadId: string, runId: string) => {
    const socket = new WebSocket(`ws://localhost:8000/ws/${threadId}/${runId}`);

    socket.onopen = () => {
        console.log("WebSocket connection established.");
    };

    socket.onmessage = (event) => {
        // Handle incoming messages (assistant's response)
        console.log("WebSocket Message: ", event);
        console.log("Assistant Response: ", event.data);
        // Update your UI here, for example, appending the assistant's response to the chat.
    };

    socket.onerror = (error) => {
        console.error("WebSocket Error: ", error);
    };

    socket.onclose = () => {
        console.log("WebSocket connection closed.");
    };

    return socket;
};