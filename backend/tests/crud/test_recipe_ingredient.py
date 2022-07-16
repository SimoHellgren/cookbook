from sqlalchemy.orm import Session
from backend.app.crud import recipe, ingredient, recipe_ingredient
from backend.app.schemas.ingredient import IngredientCreate
from backend.app.schemas.recipe import RecipeCreate


def test_get_many(db: Session) -> None:
    recipe_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_recipe = recipe.create(db=db, obj_in=recipe_in)

    ingredient_in_1 = IngredientCreate(name="Warm milk")
    ingredient_in_2 = IngredientCreate(name="Cold milk")
    db_ingredient_1 = ingredient.create(db=db, obj_in=ingredient_in_1)
    db_ingredient_2 = ingredient.create(db=db, obj_in=ingredient_in_2)

    recipe_ingredient_1 = recipe.add_ingredient(
        db, db_recipe.id, db_ingredient_1.id, 1.0, "dl", False
    )
    recipe_ingredient_2 = recipe.add_ingredient(
        db, db_recipe.id, db_ingredient_2.id, 2.0, "dl", True
    )

    db_rows = recipe_ingredient.get_many(db)

    assert db_rows
    assert len(db_rows) == 2

    assert recipe_ingredient_1 in db_rows
    assert recipe_ingredient_2 in db_rows
