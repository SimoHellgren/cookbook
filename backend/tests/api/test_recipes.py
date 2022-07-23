from decimal import Decimal
from backend.tests.utils import create_random_recipe


def test_get_all_when_empty(client):
    res = client.get("/recipes").json()
    assert len(res) == 0


def test_create(client):
    recipe = {
        "name": "Test recipe",
        "servings": 10,
        "method": "do the thing",
        "tags": "food",
    }

    res = client.post("/recipes/", json=recipe)

    assert res.status_code == 201

    data = res.json()

    assert data
    assert data["id"]
    assert recipe["name"] == data["name"]
    assert recipe["servings"] == data["servings"]
    assert recipe["method"] == data["method"]
    assert recipe["tags"] == data["tags"]


def test_get(test_db, client):
    db_obj = create_random_recipe(test_db)

    res = client.get(f"/recipes/{db_obj.id}/")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == db_obj.id
    assert data["name"] == db_obj.name
    assert data["method"] == db_obj.method
    assert data["tags"] == db_obj.tags
    assert Decimal(str(data["servings"])) == db_obj.servings
