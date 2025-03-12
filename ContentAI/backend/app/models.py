from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .schemas import TemplateType

class StoredPost(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Let MongoDB handle ID
    template: TemplateType
    objective: str
    context: str
    generated_content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StoredPrompt(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Let MongoDB handle ID
    template: TemplateType
    objective: str
    context: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    use_count: int = 1  # Start at 1 since it's being used

class User(BaseModel):
    id: str = Field(default=None, alias="_id")
    email: str
    name: str
    picture: Optional[str] = None
    google_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
