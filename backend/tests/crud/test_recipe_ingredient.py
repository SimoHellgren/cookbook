from sqlalchemy.orm import Session
from backend.app.crud import recipe, ingredient, recipe_ingredient
from backend.app.schemas.ingredient import IngredientCreate
from backend.app.schemas.recipe import RecipeCreate


def test_get(test_db: Session):
    recipe_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_recipe = recipe.create(db=test_db, obj_in=recipe_in)

    ingredient_in = IngredientCreate(name="Warm milk")
    db_ingredient = ingredient.create(db=test_db, obj_in=ingredient_in)

    recipe_ingredient_in = recipe.add_ingredient(
        test_db, db_recipe.id, db_ingredient.id, 1.0, "dl", False
    )

    get_obj = recipe_ingredient.get(
        db=test_db, recipe_id=db_recipe.id, ingredient_id=db_ingredient.id
    )

    assert get_obj
    assert get_obj.recipe_id == recipe_ingredient_in.recipe_id
    assert get_obj.ingredient_id == recipe_ingredient_in.ingredient_id
    assert get_obj.quantity == recipe_ingredient_in.quantity
    assert get_obj.measure == recipe_ingredient_in.measure
    assert get_obj.optional == recipe_ingredient_in.optional


def test_get_many(test_db: Session) -> None:
    recipe_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_recipe = recipe.create(db=test_db, obj_in=recipe_in)

    ingredient_in_1 = IngredientCreate(name="Warm milk")
    ingredient_in_2 = IngredientCreate(name="Cold milk")
    db_ingredient_1 = ingredient.create(db=test_db, obj_in=ingredient_in_1)
    db_ingredient_2 = ingredient.create(db=test_db, obj_in=ingredient_in_2)

    recipe_ingredient_1 = recipe.add_ingredient(
        test_db, db_recipe.id, db_ingredient_1.id, 1.0, "dl", False
    )

    recipe_ingredient_2 = recipe.add_ingredient(
        test_db, db_recipe.id, db_ingredient_2.id, 2.0, "dl", True
    )

    db_rows = recipe_ingredient.get_many(test_db)

    assert db_rows
    assert len(db_rows) == 2

    assert recipe_ingredient_1 in db_rows
    assert recipe_ingredient_2 in db_rows
