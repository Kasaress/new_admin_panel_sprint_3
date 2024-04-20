from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PersonSchema(BaseModel):
    id: str
    name: str


class FilmWorkSchema(BaseModel):
    id: str
    imdb_rating: float | None = Field(alias='rating')
    genres: List[str]
    title: str
    description: str | None = None
    directors_names: str | None = None
    actors_names: str | None = None
    writers_names: str | None = None
    directors: PersonSchema | None = None
    actors: PersonSchema | None = None
    writers: PersonSchema | None = None


