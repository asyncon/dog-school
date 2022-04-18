from eventsourcing.domain import Aggregate, LogEvent, event
from uuid import UUID


class Dog(Aggregate):
    # @event('Registered')
    def __init__(self, name, tricks=None, active=True):
        self.name = name
        self.tricks = tricks or []
        self.active = active

    @event('TrickAdded')
    def add_trick(self, trick):
        self.tricks.append(trick)

    @event('Deactivated')
    def deactivate(self):
        self.active = False


class DogIndexed(LogEvent):
    dog_id: UUID
