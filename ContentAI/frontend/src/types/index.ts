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
