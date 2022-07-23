from backend.app import crud
from backend.app.schemas.ingredient import IngredientCreate

def test_get_all(test_db, client):
    obj_1 = crud.ingredient.create(test_db, IngredientCreate(name="Warm Milk"))
    obj_2 = crud.ingredient.create(test_db, IngredientCreate(name="Cold Milk"))

    res = client.get("/ingredients")

    assert res.status_code == 200

    data = res.json()
    assert len(data) == 2

    ids = {d["id"] for d in data}

    assert obj_1.id in ids
    assert obj_2.id in ids


def test_get(test_db, client):
    db_obj = crud.ingredient.create(test_db, IngredientCreate(name="Warm Milk"))

    res = client.get(f"/ingredients/{db_obj.id}")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == db_obj.id
    assert data["name"] == db_obj.name


def test_get_nonexistent(client):
    res = client.get("/ingredients/1")

    assert res.status_code == 404
    assert res.content == b'{"detail":"Not Found"}'


def test_create(client):
    data_in = {"name": "Warm Milk"}

    res = client.post("/ingredients/", json=data_in)

    assert res.status_code == 201

    data = res.json()

    assert data["id"]
    assert data["name"] == data_in["name"]
