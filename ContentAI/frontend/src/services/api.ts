import { GenerationRequest, GenerationResponse, StoredPost, StoredPrompt } from '../types';

// Make sure base URL includes /api/v1
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api/v1';

export const generatePost = async (request: GenerationRequest): Promise<GenerationResponse> => {
    const response = await fetch(`${API_BASE_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        throw new Error('Failed to generate post');
    }

    return response.json();
};

export const getPostHistory = async (limit = 10, skip = 0): Promise<StoredPost[]> => {
    const response = await fetch(
        `${API_BASE_URL}/history?limit=${limit}&skip=${skip}`
    );
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
};

export const getPopularPrompts = async (limit = 5): Promise<StoredPrompt[]> => {
    const response = await fetch(
        `${API_BASE_URL}/popular-prompts?limit=${limit}`
    );
    if (!response.ok) throw new Error('Failed to fetch popular prompts');
    return response.json();
};
