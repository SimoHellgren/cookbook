from decimal import Decimal
from backend.app.models.recipe_ingredient import RecipeIngredient
from backend.tests.utils import create_random_recipe_with_ingredients


def test_get_all(test_db, client):
    *_, [db_ri] = create_random_recipe_with_ingredients(test_db)

    res = client.get("/recipe_ingredients")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1

    (api_obj,) = data

    assert api_obj["recipe_id"] == db_ri.recipe_id
    assert api_obj["ingredient_id"] == db_ri.ingredient_id
    assert Decimal(str(api_obj["quantity"])) == db_ri.quantity
    assert api_obj["measure"] == db_ri.measure
    assert api_obj["optional"] == db_ri.optional


def test_put(test_db, client):
    *_, (ri,) = create_random_recipe_with_ingredients(test_db)

    ri_in = {
        "recipe_id": ri.recipe_id,
        "ingredient_id": ri.ingredient_id,
        "quantity": 10,
        "measure": "dl",
        "optional": not (ri.optional),
        "position": 2,
    }

    res = client.put(
        f"/recipe_ingredients/{ri.recipe_id}:{ri.ingredient_id}", json=ri_in
    )

    assert res.status_code == 200

    new_ri = res.json()

    assert new_ri["recipe_id"] == ri_in["recipe_id"]
    assert new_ri["ingredient_id"] == ri_in["ingredient_id"]
    assert new_ri["quantity"] == ri_in["quantity"]
    assert new_ri["measure"] == ri_in["measure"]
    assert new_ri["optional"] == ri_in["optional"]
    assert new_ri["position"] == ri_in["position"]


def test_put_many(test_db, client):
    *_, [ri_1, ri_2] = create_random_recipe_with_ingredients(test_db, 2)

    # swap the positions of the ingredients (and other changes)
    in_1 = {
        "recipe_id": ri_1.recipe_id,
        "ingredient_id": ri_1.ingredient_id,
        "quantity": 10,
        "measure": "dl",
        "optional": not (ri_1.optional),
        "position": ri_2.position,
    }

    in_2 = {
        "recipe_id": ri_2.recipe_id,
        "ingredient_id": ri_2.ingredient_id,
        "quantity": 10,
        "measure": "dl",
        "optional": not (ri_2.optional),
        "position": ri_1.position,
    }

    res = client.put("/recipe_ingredients/bulk", json=[in_1, in_2])

    assert res.status_code == 200

    db_1, db_2 = res.json()

    assert db_1["recipe_id"] == in_1["recipe_id"]
    assert db_1["ingredient_id"] == in_1["ingredient_id"]
    assert db_1["quantity"] == in_1["quantity"]
    assert db_1["measure"] == in_1["measure"]
    assert db_1["optional"] == in_1["optional"]
    assert db_1["position"] == in_1["position"]

    assert db_2["recipe_id"] == in_2["recipe_id"]
    assert db_2["ingredient_id"] == in_2["ingredient_id"]
    assert db_2["quantity"] == in_2["quantity"]
    assert db_2["measure"] == in_2["measure"]
    assert db_2["optional"] == in_2["optional"]
    assert db_2["position"] == in_2["position"]


def test_delete(test_db, client):
    db_recipe, [db_ingredient], [db_ri] = create_random_recipe_with_ingredients(test_db)

    assert db_ri is not None

    res = client.delete(f"/recipe_ingredients/{db_recipe.id}:{db_ingredient.id}")

    assert res.status_code == 200

    assert res.json()["recipe_id"] == db_ri.recipe_id
    assert res.json()["ingredient_id"] == db_ri.ingredient_id

    assert (
        test_db.query(RecipeIngredient)
        .filter_by(recipe_id=db_ri.recipe_id, ingredient_id=db_ri.ingredient_id)
        .first()
        is None
    )
