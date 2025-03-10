export type TemplateType = "tech-insight" | "startup-story" | "product-launch" | "industry-update";

export interface GenerationRequest {
    template: TemplateType;
    objective: string;
    context: string;
    documents?: File[];
}

export interface GenerationResponse {
    post: string;
}

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
