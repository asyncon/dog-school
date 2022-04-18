from pydantic import BaseModel
from uuid import UUID


class NewDog(BaseModel):
    name: str
    tricks: list[str] = []


class Dog(NewDog):
    id: UUID

    class Config:
        orm_mode = True
