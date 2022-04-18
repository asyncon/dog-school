from typing import Iterator
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.application import AggregateNotFound, Application, EventSourcedLog
from eventsourcing.utils import EnvType
from . import domain
from . import models


class DogSchool(Application):
    def __init__(self, env: EnvType = None) -> None:
        super().__init__(env)
        self.dog_log: EventSourcedLog[domain.DogIndexed] = EventSourcedLog(
            self.events, uuid5(NAMESPACE_URL, "/dog_log"), domain.DogIndexed
        )

    def register_dog(self, new_dog):
        dog = domain.Dog(**new_dog.dict())
        dog_registered = self.dog_log.trigger_event(dog_id=dog.id)
        self.save(dog, dog_registered)
        return models.Dog.from_orm(dog)

    def deactivate_dog(self, dog_id: UUID):
        dog = self.repository.get(dog_id)
        dog.deactivate()
        self.save(dog)

    def add_trick(self, dog_id: UUID, trick: str):
        dog = self.repository.get(dog_id)
        dog.add_trick(trick)
        self.save(dog)
        return models.Dog.from_orm(dog)

    def get_dog(self, dog_id: UUID, active: bool = None):
        try:
            dog = self.repository.get(dog_id)
        except AggregateNotFound as e:
            raise DogNotFound(dog_id) from e
        if active is not None and dog.active != active:
            raise DogNotFound(dog_id)
        return models.Dog.from_orm(dog)

    def get_dogs(
        self,
        gt: int = None,
        lte: int = None,
        desc: bool = False,
        limit: int = None,
        active: bool = None,
    ) -> Iterator[models.Dog]:
        for index_dog in self.dog_log.get(gt, lte, desc, limit):
            dog = self.repository.get(index_dog.dog_id)
            if active is None or dog.active == active:
                yield models.Dog.from_orm(dog)


class DogNotFound(Exception):
    """
    Raised when a dog is not active or missing.
    """
