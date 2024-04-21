from typing import List
from pydantic import BaseModel, Field


ROLES = {
    'directors': 'director',
    'actors': 'actor',
    'writers': 'writer'
}


class PersonSchema(BaseModel):
    id: str
    name: str
    role: str


class FilmWorkSchema(BaseModel):
    id: str
    imdb_rating: float | None = Field(alias='rating')
    genres: List[str]
    title: str
    persons: list[PersonSchema] | None = Field(exclude=True)
    description: str | None = None

    def _filter_persons(self, role: str):
        if self.persons is not None:
            return [person for person in self.persons if person.role == role]
        return []

    def _get_persons_info(self, role: str):
        return [
            {'id': person.id, 'name': person.name}
            for person in self._filter_persons(role)
        ]

    def _get_persons_names(self, role: str):
        return [person.name for person in self._filter_persons(role)]

    def dict(self, **kwargs):
        obj_dict = super().dict(**kwargs)
        for role_key, role_value in ROLES.items():
            obj_dict[role_key] = self._get_persons_info(role_value)
            obj_dict[f'{role_key}_names'] = self._get_persons_names(role_value)
        return obj_dict
