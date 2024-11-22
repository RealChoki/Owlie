// Core Interfaces

interface RequiredAction {
    action: string;
    details?: string;
}

interface LastError {
    code: string;
    message: string;
}

// Run Status Interfaces

interface RunStatus {
    run_id: string;
    thread_id: string;
    status?: string;
    required_action?: RequiredAction;
    last_error?: LastError;
}

// Message and Thread Interfaces

interface ThreadMessage {
    id: string;
    content: string;
    role: string;
    hidden: boolean;
    created_at: number;
}

interface Thread {
    messages: ThreadMessage[];
}

// Tool Output Interface

interface ToolOutput {
    tool_id: string;
    output: string;
}

// Response Interfaces

interface PostToolResponse extends RunStatus {}

interface CreateThreadResponse extends RunStatus {}

interface FetchThreadResponse extends Thread {}

interface FetchRunResponse extends RunStatus {}

interface PostMessageResponse extends RunStatus {}

// REST Service functions

export const createNewThread = async (): Promise<CreateThreadResponse | undefined> => {
    try {
        const response = await fetch("http://localhost:8000/api/new", {
            method: "POST",
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data: CreateThreadResponse = await response.json();
        return data;
    } catch (err: any) {
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