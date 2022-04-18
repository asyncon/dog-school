from uuid import UUID
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .app import DogNotFound, DogSchool
from .models import Dog, NewDog

school = DogSchool()

app = FastAPI()


@app.exception_handler(DogNotFound)
async def dog_not_found_handler(request: Request, exc: DogNotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"{exc.__class__.__name__}: {exc.args[0]}"},
    )


@app.post("/dog", response_model=Dog, status_code=201)
async def register_dog(dog: NewDog):
    return school.register_dog(dog)


@app.put("/dog/{dog_id}/add-trick/{trick}", status_code=status.HTTP_204_NO_CONTENT)
async def add_trick(dog_id: UUID, trick: str):
    school.add_trick(dog_id, trick)


@app.get("/dog", response_model=list[Dog])
async def get_dogs(active: bool | None = True):
    return [*school.get_dogs(active=active)]


@app.get("/dog/{dog_id}", response_model=Dog)
async def get_dog(dog_id: UUID, active: bool | None = True):
    return school.get_dog(dog_id, active=active)


@app.delete("/dog/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_dog(dog_id: UUID):
    school.deactivate_dog(dog_id)
