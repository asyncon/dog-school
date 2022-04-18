from uuid import uuid4
from pytest import raises
from dog_school.app import DogNotFound, DogSchool, models


def test_dog_school():
    data = {
        "Foxy": ["Lunge", "Lick", "Flee", "Chase", "Steal"],
        "Roxy": ["Lunge", "Lick", "Flee", "Chase", "Steal"],
        "Soxy": ["Lunge", "Lick", "Flee", "Chase", "Steal"],
    }
    app = DogSchool()
    with raises(DogNotFound):
        app.get_dog(uuid4())
    for name, tricks in data.items():
        dog = app.register_dog(models.NewDog(name=name, tricks=tricks[:3]))
        assert dog.name == name
        for trick in tricks[3:]:
            app.add_trick(dog.id, trick)
        assert app.get_dog(dog.id).tricks == tricks
    dogs = [*app.get_dogs()]
    assert {dog.name: dog.tricks for dog in dogs} == data
    updated = {k: v for k, v in data.items() if k != "Soxy"}
    dog = app.get_dog({dog.name: dog.id for dog in dogs}["Soxy"])
    app.deactivate_dog(dog.id)
    with raises(DogNotFound):
        app.get_dog(dog.id, active=True)
    assert {dog.name: dog.tricks for dog in app.get_dogs(active=True)} == updated
