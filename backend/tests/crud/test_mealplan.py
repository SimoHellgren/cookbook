from datetime import date
from sqlalchemy.orm import Session
from backend.app.crud import mealplan, recipe
from backend.app.schemas.mealplan import MealplanCreate, MealplanUpdate
from backend.app.schemas.recipe import RecipeCreate


def test_create(test_db: Session) -> None:
    obj_in = MealplanCreate(
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    db_obj = mealplan.create(db=test_db, obj_in=obj_in)

    assert db_obj
    assert db_obj.id
    assert db_obj.date == date(2022, 1, 1)
    assert db_obj.name == "lunch"
    assert db_obj.recipe_id is None


def test_get(test_db: Session) -> None:
    obj_in = MealplanCreate(
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    db_obj = mealplan.create(db=test_db, obj_in=obj_in)

    assert db_obj is not None

    get_obj = mealplan.get(test_db, db_obj.id)

    assert get_obj
    assert get_obj.id == db_obj.id
    assert get_obj.name == db_obj.name
    assert get_obj.date == db_obj.date
    assert get_obj.servings == db_obj.servings


def test_get_nonexistent(test_db: Session) -> None:
    db_obj = mealplan.get(test_db, 1)

    assert db_obj is None


def test_get_many(test_db: Session) -> None:
    obj_in_1 = MealplanCreate(
        db=test_db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    obj_in_2 = MealplanCreate(
        db=test_db,
        date="2022-01-01",
        name="dinner",
        servings=2.0,
    )

    db_obj_1 = mealplan.create(db=test_db, obj_in=obj_in_1)
    db_obj_2 = mealplan.create(db=test_db, obj_in=obj_in_2)

    db_rows = mealplan.get_many(test_db)

    assert db_rows
    assert len(db_rows) == 2

    assert db_obj_1 in db_rows
    assert db_obj_2 in db_rows


def test_delete(test_db: Session) -> None:
    obj_in = MealplanCreate(
        db=test_db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    db_obj = mealplan.create(db=test_db, obj_in=obj_in)

    assert db_obj is not None

    deleted_mealplan = mealplan.remove(test_db, db_obj.id)

    assert mealplan.get(test_db, db_obj.id) is None
    assert db_obj is deleted_mealplan


def test_update(test_db: Session) -> None:
    recipe_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_recipe = recipe.create(db=test_db, obj_in=recipe_in)

    mealplan_in = MealplanCreate(
        db=test_db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    db_mealplan = mealplan.create(db=test_db, obj_in=mealplan_in)

    assert db_mealplan is not None
    update_data = MealplanUpdate(
        id=db_mealplan.id,
        recipe_id=db_recipe.id,
        date="2022-02-02",
        name="second lunch",
        servings=3.0,
    )

    mealplan_updated = mealplan.update(
        db=test_db, db_obj=db_mealplan, obj_in=update_data
    )

    assert mealplan_updated is db_mealplan
    assert mealplan_updated.recipe is db_recipe
    assert mealplan_updated.date == date(2022, 2, 2)
    assert mealplan_updated.name == "second lunch"
    assert mealplan_updated.servings == 3.0
