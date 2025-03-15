import { GenerationRequest, StoredPost, StoredPrompt, PaginatedResponse, TextGenerationResponse, ImageGenerationResponse } from '../types';

const API_BASE_URL = "http://localhost:8000";

export const generatePost = async (request: GenerationRequest): Promise<TextGenerationResponse> => {
	// Very simple API call without extra error checks
	const formData = new FormData();
	formData.append('template', request.template);
	formData.append('objective', request.objective);
	formData.append('context', request.context);
	formData.append('type', request.type);
	if (request.documents) {
		request.documents.forEach((file, index) => {
			formData.append(`document_${index}`, file);
		});
	}
	const token = localStorage.getItem('authToken');
	const response = await fetch(`${API_BASE_URL}/api/generate`, {
		method: 'POST',
		headers: token ? { 'Authorization': `Bearer ${token}` } : {},
		body: formData,
	});
	return await response.json();
};

export const generateImage = async (request: GenerationRequest): Promise<ImageGenerationResponse> => {
	// A simple API call for image generation; no extra error handling
	const formData = new FormData();
	formData.append('template', request.template);
	formData.append('objective', request.objective);
	formData.append('context', request.context);
	formData.append('type', 'image');
	const token = localStorage.getItem('authToken');
	const response = await fetch(`${API_BASE_URL}/api/generate/image/`, { // added trailing slash
		method: 'POST',
		headers: token ? { 'Authorization': `Bearer ${token}` } : {},
		body: formData,
	});
	return await response.json();
};

export const getPostHistory = async (limit = 10, skip = 0, search?: string): Promise<PaginatedResponse<StoredPost>> => {
	// Simply call the API and return parsed JSON
	const token = localStorage.getItem('authToken');
	const response = await fetch(
		`${API_BASE_URL}/api/history?limit=${limit}&skip=${skip}${search ? `&search=${encodeURIComponent(search)}` : ''}`,
		{ headers: token ? { 'Authorization': `Bearer ${token}` } : {} }
	);
	const data = await response.json();
	return {
		posts: data.posts,
		total: data.total || 0,
		page: data.page || 1,
		totalPages: data.totalPages || 1
	};
}

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
  type?: "text" | "image" | "full";  // Add type property
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
