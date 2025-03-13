import { GenerationRequest, GenerationResponse, StoredPost, StoredPrompt } from '../types';

const API_BASE_URL = "http://localhost:8000";
const MAX_FILE_SIZE = 50 * 1024; // 50KB per file (approximately 4-5 pages of text)

export const generatePost = async (request: GenerationRequest): Promise<GenerationResponse> => {
    try {
        if (!request.template || !request.objective || !request.context) {
            throw new Error('Missing required fields');
        }
        console.log('Attempting to generate post with request:', request);
        console.log('Sending request to:', `${API_BASE_URL}/api/generate`);
        
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
        
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/api/generate`, {
            method: 'POST',
            // Do not set 'Content-Type' when sending FormData; include auth header if token exists.
            headers: token ? { 'Authorization': `Bearer ${token}` } : {},
            body: formData,
        });

        if (response.status === 401) {
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
            throw new Error('Authentication failed. Please login again.');
        }

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('API Error Response:', errorData);
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
    const token = localStorage.getItem('authToken');
    const response = await fetch(
        `${API_BASE_URL}/api/history?limit=${limit}&skip=${skip}`,
        { headers: token ? { 'Authorization': `Bearer ${token}` } : {} }
    );
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
};

export const getPopularPrompts = async (limit = 5): Promise<StoredPrompt[]> => {
    const response = await fetch(
        `${API_BASE_URL}/api/popular-prompts?limit=${limit}`
    );
    if (!response.ok) throw new Error('Failed to fetch popular prompts');
    return response.json();
};

export const savePost = async (post: {
  template: string;
  objective: string;
  context: string;
  generated_content: string;
}): Promise<void> => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    throw new Error('Authentication required');
  }

  const response = await fetch(`${API_BASE_URL}/api/posts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(post)
  });

  if (!response.ok) {
    throw new Error('Failed to save post');
  }
};

export const deletePost = async (postId: string): Promise<void> => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    throw new Error('Authentication required');
  }

  const response = await fetch(`${API_BASE_URL}/api/posts/${postId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to delete post');
  }
};
