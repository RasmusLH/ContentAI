export type TemplateType = "tech-insight" | "startup-story" | "product-launch" | "industry-update";

export interface GenerationRequest {
    template: TemplateType;
    objective: string;
    context: string;
    documents?: File[];
    type: GenerationType;  // Make type required
}

export interface TextGenerationResponse {
    post: string;
    error?: string;
}

export interface ImageGenerationResponse {
    image_url: string;
    error?: string;
}

export type GenerationResponse = TextGenerationResponse | ImageGenerationResponse;

export interface Template {
    id: TemplateType;
    label: string;
    description: string;
}

export interface StoredPost extends GenerationRequest {
    _id: string;
    generated_content: string;
    created_at: string;
}

export interface StoredPrompt extends GenerationRequest {
    _id: string;
    created_at: string;
    use_count: number;
}

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
}

export interface PaginatedResponse<T> {
  posts: T[];
  total: number;
  page: number;
  totalPages: number;
}

export type GenerationType = "text" | "image" | "full";
