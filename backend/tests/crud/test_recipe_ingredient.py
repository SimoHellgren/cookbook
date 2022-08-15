from sqlalchemy.orm import Session
from backend.app.crud import recipe_ingredient
from backend.tests.utils import create_random_recipe_with_ingredients


def test_get(test_db: Session):
    db_recipe, [db_ingredient], [db_ri] = create_random_recipe_with_ingredients(test_db)

    get_obj = recipe_ingredient.get(
        db=test_db, recipe_id=db_recipe.id, ingredient_id=db_ingredient.id
    )

    assert get_obj
    assert get_obj.recipe_id == db_ri.recipe_id
    assert get_obj.ingredient_id == db_ri.ingredient_id
    assert get_obj.quantity == db_ri.quantity
    assert get_obj.measure == db_ri.measure
    assert get_obj.optional == db_ri.optional
    assert get_obj.position == db_ri.position


def test_get_many(test_db: Session) -> None:
    *_, [db_ri_1, db_ri_2] = create_random_recipe_with_ingredients(
        test_db, ingredient_count=2
    )

    db_rows = recipe_ingredient.get_many(test_db)

    assert db_rows
    assert len(db_rows) == 2

    assert db_ri_1 in db_rows
    assert db_ri_2 in db_rows


def test_delete(test_db: Session) -> None:
    db_recipe, [db_ingredient], [db_ri] = create_random_recipe_with_ingredients(test_db)

    assert db_ri

    deleted_obj = recipe_ingredient.remove(
        db=test_db, recipe_id=db_recipe.id, ingredient_id=db_ingredient.id
    )

    assert deleted_obj is not None
    assert deleted_obj.recipe_id == db_ri.recipe_id
    assert deleted_obj.ingredient_id == db_ri.ingredient_id

    assert (
        recipe_ingredient.get(
            db=test_db, recipe_id=db_recipe.id, ingredient_id=db_ingredient.id
        )
        is None
    )
