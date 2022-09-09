from decimal import Decimal
from backend.tests.utils import create_random_mealplan, create_random_recipe


def test_get_many(test_db, client):
    db_mp = create_random_mealplan(test_db)

    res = client.get("/mealplans")

    assert res.status_code == 200

    data = res.json()
    assert len(data) == 1

    (api_mp,) = data

    assert api_mp["id"] == db_mp.id
    assert api_mp["name"] == db_mp.name
    assert api_mp["date"] == str(db_mp.date)
    assert Decimal(str(api_mp["servings"])) == db_mp.servings
    assert api_mp["recipe_id"] == db_mp.recipe_id


def test_get(test_db, client):
    db_mp = create_random_mealplan(test_db)

    res = client.get(f"/mealplans/{db_mp.id}")

    assert res.status_code == 200

    api_mp = res.json()

    assert api_mp["id"] == db_mp.id
    assert api_mp["name"] == db_mp.name
    assert api_mp["date"] == str(db_mp.date)
    assert Decimal(str(api_mp["servings"])) == db_mp.servings
    assert api_mp["recipe_id"] == db_mp.recipe_id


def test_get_nonexistent(client):
    res = client.get("/mealplans/1")

    assert res.status_code == 404


def test_create(client):
    data_in = {
        "date": "2022-01-02",
        "name": "lunch",
        "servings": 2.0,
        "position": 1,
    }

    res = client.post("/mealplans/", json=data_in)

    assert res.status_code == 201

    api_data = res.json()

    assert api_data
    assert api_data["id"]
    assert api_data["date"] == data_in["date"]
    assert api_data["name"] == data_in["name"]
    assert api_data["servings"] == data_in["servings"]
    assert api_data["recipe_id"] is None


def test_update(test_db, client):
    db_mp = create_random_mealplan(test_db)
    db_recipe = create_random_recipe(test_db)

    data_in = {
        "id": db_mp.id,
        "date": "2022-01-02",
        "servings": 10,
        "name": "new name who dis?",
        "recipe_id": db_recipe.id,
        "position": 2,
    }

    res = client.put(f"/mealplans/{db_mp.id}", json=data_in)

    assert res.status_code == 200

    api_data = res.json()

    assert api_data["id"] == data_in["id"]
    assert api_data["date"] == data_in["date"]
    assert api_data["servings"] == data_in["servings"]
    assert api_data["name"] == data_in["name"]
    assert api_data["recipe_id"] == data_in["recipe_id"]
    assert api_data["position"] == data_in["position"]


def test_update_nonexistent(client):
    data_in = {
        "id": 1,
        "date": "2022-01-02",
        "servings": 10,
        "name": "new name who dis?",
        "recipe_id": 0,
        "position": 1,
    }

    res = client.put("/mealplans/1", json=data_in)

    assert res.status_code == 404


def test_delete(test_db, client):
    db_mealplan = create_random_mealplan(test_db)

    res = client.delete(f"/mealplans/{db_mealplan.id}")

    assert res.status_code == 200

    assert res.json()["id"] == db_mealplan.id

    get_res = client.get(f"/mealplans/{db_mealplan.id}")

    assert get_res.status_code == 404
