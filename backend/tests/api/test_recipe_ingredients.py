from decimal import Decimal
from backend.app import crud
from backend.app.models.recipe_ingredient import RecipeIngredient
from backend.app.schemas.ingredient import IngredientCreate
from backend.app.schemas.recipe_ingredient import RecipeIngredientCreate
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


def test_delete(test_db, client):
    db_recipe = create_random_recipe(test_db)
    db_ingredient = crud.ingredient.create(test_db, IngredientCreate(name="Warm Milk"))

    db_ri = crud.recipe_ingredient.create(
        test_db,
        RecipeIngredientCreate(
            recipe_id=db_recipe.id,
            ingredient_id=db_ingredient.id,
            quantity=random_decimal(),
            measure="dl",
            optional=False,
        ),
    )

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
