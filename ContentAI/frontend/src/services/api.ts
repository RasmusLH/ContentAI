import { GenerationRequest, GenerationResponse, StoredPost, StoredPrompt } from '../types';

const API_BASE_URL = "http://localhost:8000";
const MAX_FILE_SIZE = 50 * 1024; // 50KB per file (approximately 4-5 pages of text)

const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('authToken');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const generatePost = async (request: GenerationRequest): Promise<GenerationResponse> => {
    try {
        console.log('Attempting to generate post with request:', request);
        console.log('Sending request to:', `${API_BASE_URL}/api/generate`);  // Add /api in the endpoint
        
        // Validate file sizes
        if (request.documents && request.documents.length > 0) {
            for (const file of request.documents) {
                if (file.size > MAX_FILE_SIZE) {
                    throw new Error(`File ${file.name} is too large. Maximum size is 50KB (about 4-5 pages of text)`);
                }
            }
        }

        const formData = new FormData();
        formData.append('template', request.template);
        formData.append('objective', request.objective);
        formData.append('context', request.context);
        
        // Add documents if they exist
        if (request.documents && request.documents.length > 0) {
            request.documents.forEach((file, index) => {
                formData.append(`document_${index}`, file);
            });
        }

        const response = await fetch(`${API_BASE_URL}/api/generate`, {
            method: 'POST',
            headers: {
                ...getAuthHeaders(),
            },
            body: formData, // Send as FormData instead of JSON
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
        `${API_BASE_URL}/api/history?limit=${limit}&skip=${skip}`,
        {
            headers: getAuthHeaders(),
        }
    );
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
};

export const getPopularPrompts = async (limit = 5): Promise<StoredPrompt[]> => {
    const response = await fetch(
        `${API_BASE_URL}/api/popular-prompts?limit=${limit}`,
        {
            headers: getAuthHeaders(),
        }
    );
    if (!response.ok) throw new Error('Failed to fetch popular prompts');
    return response.json();
};
