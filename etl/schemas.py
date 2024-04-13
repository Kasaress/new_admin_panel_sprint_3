from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class PersonSchema(BaseModel):
    id: str
    name: str
    role: Optional[str] = None


class FilmWorkSchema(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    rating: Optional[float] = None
    type: str
    genres: List[str]
    persons: List[PersonSchema]
    extracted_time: datetime
