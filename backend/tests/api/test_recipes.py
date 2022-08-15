from decimal import Decimal
from sqlalchemy.exc import IntegrityError
import pytest
from backend.app.models.recipe import Recipe
from backend.app import crud
from backend.app.schemas.ingredient import IngredientCreate
from backend.tests.utils import create_random_recipe, create_random_recipe_with_ingredients, random_decimal, random_string


def test_get_all(test_db, client):
    obj_1 = create_random_recipe(test_db)
    obj_2 = create_random_recipe(test_db)

    res = client.get("/recipes")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 2

    ids = {d["id"] for d in data}

    assert obj_1.id in ids
    assert obj_2.id in ids


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


def test_create_existing_name_fails(test_db, client):
    db_obj = create_random_recipe(test_db)

    with pytest.raises(IntegrityError):
        client.post(
            "/recipes/",
            json={
                "name": db_obj.name,
                "servings": str(random_decimal()),
                "method": random_string(),
                "tags": f"{random_string()},{random_string()}",
            },
        )


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


def test_nonexistent(client):
    res = client.get("/recipes/1/")

    assert res.status_code == 404
    assert res.content == b'{"detail":"Not Found"}'


def test_put(test_db, client):
    db_obj = create_random_recipe(test_db)

    # this test data is for now quaranteed to be different from the randomly generated,
    # since the string lengths are different, random servings are capped at 9.99, and
    # there are always two tags. But, this may change later which might introduce a
    # chance of this test passing when it shouldn't.
    new_obj = {
        "id": db_obj.id,
        "name": "New name",
        "method": "New method",
        "servings": 10.0,
        "tags": "tags,and,more,tags",
    }

    res = client.put(f"/recipes/{db_obj.id}", json=new_obj)

    assert res.status_code == 200

    data = res.json()

    assert new_obj["id"] == data["id"]
    assert new_obj["name"] == data["name"]
    assert new_obj["method"] == data["method"]
    assert new_obj["servings"] == data["servings"]
    assert new_obj["tags"] == data["tags"]


def test_put_nonexistent(client):
    data_in = {
        "id": 1,
        "name": "New name",
        "method": "New method",
        "servings": 10.0,
        "tags": "tags,and,more,tags",
    }

    res = client.put("/recipes/1", json=data_in)

    assert res.status_code == 404


def test_delete(test_db, client):
    db_obj = create_random_recipe(test_db)

    res = client.delete(f"/recipes/{db_obj.id}")

    assert res.status_code == 200

    assert res.json()["id"] == db_obj.id

    assert test_db.query(Recipe).get(db_obj.id) is None


def test_get_ingredients(test_db, client):
    db_recipe, _, [db_ri] = create_random_recipe_with_ingredients(test_db)

    res = client.get(f"/recipes/{db_recipe.id}/ingredients")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1

    (api_obj,) = data

    assert api_obj["recipe_id"] == db_ri.recipe_id
    assert api_obj["ingredient_id"] == db_ri.ingredient_id
    assert Decimal(str(api_obj["quantity"])) == db_ri.quantity
    assert api_obj["measure"] == db_ri.measure
    assert api_obj["optional"] == db_ri.optional


def test_add_ingredient(test_db, client):
    db_recipe = create_random_recipe(test_db)
    db_ingredient = crud.ingredient.create(test_db, IngredientCreate(name="Warm Milk"))

    res = client.post(
        f"/recipes/{db_recipe.id}/ingredients",
        json={
            "recipe_id": db_recipe.id,
            "ingredient_id": db_ingredient.id,
            "quantity": 2,
            "measure": "dl",
            "optional": True,
            "position": 1,
        },
    )

    assert res.status_code == 201

    data = res.json()

    assert data["recipe_id"] == db_recipe.id
    assert data["ingredient_id"] == db_ingredient.id
    assert data["quantity"] == 2
    assert data["measure"] == "dl"
    assert data["optional"] is True
    assert data["position"] == 1
