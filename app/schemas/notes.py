#app/schemas/notes.py

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str
    category: Optional[str] = Field (default=None, max_length=50)
    is_pinned: bool = Field(default=False)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]
    is_pinned: bool
    created_at: datetime
    model_config =ConfigDict(from_attributes=True) #FastAPI and Pydantic can read the SQLAlchemy ojects directly