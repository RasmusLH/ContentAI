from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .schemas import TemplateType
from bson import ObjectId

class StoredPost(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # Let MongoDB handle ID
    user_id: str
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
    id: Optional[str] = Field(default=None, alias="_id")  # Changed from str to Optional[str]
    email: str
    name: str
    picture: Optional[str] = None
    google_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
        json_encoders = {
            ObjectId: str  # Add this to handle ObjectId serialization
        }
