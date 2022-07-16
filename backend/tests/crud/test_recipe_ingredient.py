from sqlalchemy.orm import Session
from backend.app.crud import recipe, ingredient, recipe_ingredient


def test_get_all(db: Session) -> None:
    recipe_in = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    ingredient_1 = ingredient.create(db=db, name="Warm milk")
    ingredient_2 = ingredient.create(db=db, name="Cold milk")

    recipe_ingredient_1 = recipe.add_ingredient(
        db, recipe_in.id, ingredient_1.id, 1.0, "dl", False
    )
    recipe_ingredient_2 = recipe.add_ingredient(
        db, recipe_in.id, ingredient_2.id, 2.0, "dl", True
    )

    db_rows = recipe_ingredient.get_all(db)

    assert db_rows
    assert len(db_rows) == 2

    assert recipe_ingredient_1 in db_rows
    assert recipe_ingredient_2 in db_rows
