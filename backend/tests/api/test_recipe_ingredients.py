from decimal import Decimal
from backend.app import crud
from backend.app.schemas.ingredient import IngredientCreate
from backend.tests.utils import create_random_recipe, random_decimal


def test_get_all(test_db, client):
    db_recipe = create_random_recipe(test_db)
    db_ingredient = crud.ingredient.create(test_db, IngredientCreate(name="Warm Milk"))

    db_obj = crud.recipe.add_ingredient(
        db=test_db,
        recipe_id=db_recipe.id,
        ingredient_id=db_ingredient.id,
        quantity=random_decimal(),
        measure="dl",
        optional=True,
    )

    res = client.get("/recipe_ingredients")

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1

    (api_obj,) = data

    assert api_obj["recipe_id"] == db_obj.recipe_id
    assert api_obj["ingredient_id"] == db_obj.ingredient_id
    assert Decimal(str(api_obj["quantity"])) == db_obj.quantity
    assert api_obj["measure"] == db_obj.measure
    assert api_obj["optional"] == db_obj.optional
