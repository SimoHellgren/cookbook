from decimal import Decimal
from backend.app import crud
from backend.app.models.recipe_ingredient import RecipeIngredient
from backend.app.schemas.ingredient import IngredientCreate
from backend.app.schemas.recipe_ingredient import RecipeIngredientCreate
from backend.tests.utils import (
    create_random_recipe,
    create_random_recipe_with_ingredients,
    random_decimal,
)


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
