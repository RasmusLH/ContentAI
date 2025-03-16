from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TemplateType(str, Enum):
    TECH_INSIGHT = "tech-insight"
    STARTUP_STORY = "startup-story"
    PRODUCT_LAUNCH = "product-launch"
    INDUSTRY_UPDATE = "industry-update"

class GenerationRequest(BaseModel):
    template: TemplateType
    objective: str = Field(..., min_length=10, max_length=500)
    context: str = Field(..., min_length=10, max_length=1000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "template": "tech-insight",
                "objective": "Discuss the impact of AI on software development",
                "context": "Recent advancements in AI tools and their adoption in dev teams"
            }
        }
    }

TEMPLATE_PROMPTS = {
    TemplateType.TECH_INSIGHT: "Create a LinkedIn post discussing technology trends, focusing on innovation impact and future implications.",
    TemplateType.STARTUP_STORY: "Write an inspiring LinkedIn post about a startup journey, highlighting key milestones, challenges overcome, and lessons learned.",
    TemplateType.PRODUCT_LAUNCH: "Craft an engaging LinkedIn announcement about a new product launch, emphasizing unique features and customer benefits.",
    TemplateType.INDUSTRY_UPDATE: "Compose a LinkedIn post analyzing industry trends, market developments, and their business implications."
}
