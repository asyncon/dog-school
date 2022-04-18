from uuid import uuid4


def test_dog_school(app):
    data = {
        "Foxy": ["Lunge", "Lick", "Flee", "Chase", "Steal"],
        "Roxy": ["Lunge", "Lick", "Flee", "Chase", "Steal"],
        "Soxy": ["Lunge", "Lick", "Flee", "Chase", "Steal"],
    }
    res = app.get(f"/dog/{uuid4()}")
    assert res.status_code == 404
    for name, tricks in data.items():
        res = app.post("/dog", json={"name": name, "tricks": tricks[:3]})
        assert res.ok
        dog = res.json()
        assert dog["name"] == name
        for trick in tricks[3:]:
            res = app.put(f"/dog/{dog['id']}/add-trick/{trick}")
            assert res.ok
        res = app.get(f"/dog/{dog['id']}")
        assert res.ok
        assert res.json()["tricks"] == tricks
    res = app.get("/dog")
    assert res.ok
    dogs = [*res.json()]
    assert {dog['name']: dog['tricks'] for dog in dogs} == data
    updated = {k: v for k, v in data.items() if k != "Soxy"}
    dog_id = {dog['name']: dog['id'] for dog in dogs}["Soxy"]
    res = app.get(f"/dog/{dog_id}")
    assert res.ok
    dog = res.json()
    res = app.delete(f"/dog/{dog_id}")
    assert res.ok
    res = app.get(f"/dog/{dog_id}", params={"active": True})
    assert res.status_code == 404
    res = app.get("/dog")
    assert res.ok
    assert {dog['name']: dog['tricks'] for dog in res.json()} == updated
