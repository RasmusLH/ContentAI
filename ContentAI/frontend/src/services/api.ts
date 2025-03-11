import { GenerationRequest, GenerationResponse, StoredPost, StoredPrompt } from '../types';

const API_BASE_URL = "http://localhost:8000";

export const generatePost = async (request: GenerationRequest): Promise<GenerationResponse> => {
    try {
        console.log('Attempting to generate post with request:', request);
        console.log('Sending request to:', `${API_BASE_URL}/api/generate`);  // Add /api in the endpoint
        
        const response = await fetch(`${API_BASE_URL}/api/generate`, {  // Add /api in the endpoint
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(request),
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('API Error Response:', errorData);
            // Additional logging of response headers for diagnostic details
            console.error('Response Headers:', response.headers);
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Successful response:', data);
        return data;
    } catch (error) {
        console.error('API Error:', error);
        if (error instanceof Error) {
            console.error('Full error object:', {
                message: error.message,
                stack: error.stack,
                name: error.name
            });
        } else {
            console.error('Unknown error:', error);
        }
        throw error;
    }
};

export const getPostHistory = async (limit = 10, skip = 0): Promise<StoredPost[]> => {
    const response = await fetch(
        `${API_BASE_URL}/api/history?limit=${limit}&skip=${skip}`  // Add /api in the endpoint
    );
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
};

export const getPopularPrompts = async (limit = 5): Promise<StoredPrompt[]> => {
    const response = await fetch(
        `${API_BASE_URL}/api/popular-prompts?limit=${limit}`  // Add /api in the endpoint
    );
    if (!response.ok) throw new Error('Failed to fetch popular prompts');
    return response.json();
};
