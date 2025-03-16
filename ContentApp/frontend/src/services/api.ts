import { GenerationRequest, StoredPost, StoredPrompt, PaginatedResponse, TextGenerationResponse, ImageGenerationResponse } from '../types';

const API_BASE_URL = "http://localhost:8000";

// Helper for building URLs with query params
function buildUrl(endpoint: string, params?: Record<string, string>): string {
  const url = `${API_BASE_URL}/api${endpoint}`;
  if (!params) return url;
  
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) searchParams.append(key, value);
  });
  
  const queryString = searchParams.toString();
  return queryString ? `${url}?${queryString}` : url;
}

// Shared API helper
async function apiRequest<T>(
  endpoint: string,
  options: {
    method?: string;
    body?: FormData | string;
    headers?: Record<string, string>;
    requiresAuth?: boolean;
    params?: Record<string, string>;
  } = {}
): Promise<T> {
  const { 
    method = 'GET',
    body,
    headers = {},
    requiresAuth = true,
    params
  } = options;

  const token = localStorage.getItem('authToken');
  
  if (requiresAuth && !token) {
    throw new Error('Authentication required');
  }

  const requestHeaders: Record<string, string> = {
    ...headers,
    ...(token && requiresAuth ? { 'Authorization': `Bearer ${token}` } : {})
  };

  if (body && !(body instanceof FormData)) {
    requestHeaders['Content-Type'] = 'application/json';
  }

  const url = buildUrl(endpoint, params);
  const response = await fetch(url, {
    method,
    headers: requestHeaders,
    body,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}

// API Functions using shared helper
export const generatePost = async (request: GenerationRequest): Promise<TextGenerationResponse> => {
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

  return apiRequest<TextGenerationResponse>('/generate', {
    method: 'POST',
    body: formData
  });
};

export const generateImage = async (request: GenerationRequest): Promise<ImageGenerationResponse> => {
  const formData = new FormData();
  formData.append('template', request.template);
  formData.append('objective', request.objective);
  formData.append('context', request.context);
  formData.append('type', 'image');

  return apiRequest<ImageGenerationResponse>('/generate/image', {
    method: 'POST',
    body: formData
  });
};

export const getPostHistory = async (
  limit = 10, 
  skip = 0, 
  search?: string
): Promise<PaginatedResponse<StoredPost>> => {
  return apiRequest<PaginatedResponse<StoredPost>>('/history', {
    params: {
      limit: String(limit),
      skip: String(skip),
      ...(search && { search })
    }
  });
};

export const savePost = async (post: {
  template: string;
  objective: string;
  context: string;
  generated_content: string;
  type?: "text" | "image" | "full";
}): Promise<void> => {
  return apiRequest('/posts', {
    method: 'POST',
    body: JSON.stringify(post),
  });
};

export const deletePost = async (postId: string): Promise<void> => {
  return apiRequest(`/posts/${postId}`, {
    method: 'DELETE'
  });
};

export const getPopularPrompts = async (limit = 5): Promise<StoredPrompt[]> => {
  return apiRequest<StoredPrompt[]>('/popular-prompts', {
    requiresAuth: false,
    params: { limit: String(limit) }
  });
};
