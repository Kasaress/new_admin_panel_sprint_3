from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

from etl.config.logging_settings import logger


class PersonSchema(BaseModel):
    id: str
    name: str


class PersonFullSchema(BaseModel):
    id: str
    name: str
    role: str


class FilmWorkSchema(BaseModel):
    id: str
    imdb_rating: float | None = Field(alias='rating')
    genres: List[str]
    title: str
    persons: list[PersonFullSchema] | None = Field(exclude=True)
    description: str | None = None

    @property
    def directors(self):
        return [PersonSchema(id=person.id, name=person.name).dict() for person in self.persons if person.role.lower() == 'режиссер']

    @property
    def directors_names(self):
        return [person.name for person in self.persons if person.role.lower() == 'режиссер']

    @property
    def actors(self):
        return [PersonSchema(id=person.id, name=person.name).dict() for person in self.persons if
                person.role.lower() == 'актер']

    @property
    def actors_names(self):
        return [person.name for person in self.persons if person.role.lower() == 'актер']

    @property
    def writers(self):
        return [PersonSchema(id=person.id, name=person.name).dict() for person in self.persons if
                person.role.lower() == 'сценарист']

    @property
    def writers_names(self):
        return [person.name for person in self.persons if person.role.lower() == 'сценарист']

    def dict(self, **kwargs):
        obj_dict = super().dict(**kwargs)
        obj_dict['directors'] = self.directors
        obj_dict['directors_names'] = self.directors_names
        obj_dict['actors'] = self.actors
        obj_dict['actors_names'] = self.actors_names
        obj_dict['writers'] = self.writers
        obj_dict['writers_names'] = self.writers_names
        return obj_dict
