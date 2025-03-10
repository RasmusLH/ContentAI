from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .schemas import TemplateType

class StoredPost(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    template: TemplateType
    objective: str
    context: str
    generated_content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StoredPrompt(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    template: TemplateType
    objective: str
    context: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    use_count: int = 0
