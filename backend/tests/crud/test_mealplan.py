from sqlalchemy.orm import Session
from backend.app.crud import mealplan, recipe


def test_create(db: Session) -> None:
    mealplan_in = mealplan.create(
        db=db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    assert mealplan_in
    assert mealplan_in.id
    assert mealplan_in.date.strftime("%Y-%m-%d") == "2022-01-01"
    assert mealplan_in.name == "lunch"
    assert mealplan_in.recipe_id is None


def test_get(db: Session) -> None:
    mealplan_in = mealplan.create(
        db=db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    assert mealplan_in is not None

    db_obj = mealplan.get(db, mealplan_in.id)

    assert db_obj
    assert db_obj.id == mealplan_in.id
    assert db_obj.name == mealplan_in.name
    assert db_obj.date == mealplan_in.date
    assert db_obj.servings == mealplan_in.servings


def test_get_nonexistent(db: Session) -> None:
    db_obj = mealplan.get(db, 1)

    assert db_obj is None


def test_get_all(db: Session) -> None:
    mealplan_1 = mealplan.create(
        db=db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    mealplan_2 = mealplan.create(
        db=db,
        date="2022-01-01",
        name="dinner",
        servings=2.0,
    )

    db_rows = mealplan.get_all(db)

    assert db_rows
    assert len(db_rows) == 2

    assert mealplan_1 in db_rows
    assert mealplan_2 in db_rows


def test_delete(db: Session) -> None:
    mealplan_in = mealplan.create(
        db=db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    assert mealplan_in is not None

    deleted_mealplan = mealplan.delete(db, mealplan_in.id)

    assert mealplan.get(db, mealplan_in.id) is None
    assert mealplan_in is deleted_mealplan


def test_update(db: Session) -> None:
    recipe_in = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    mealplan_in = mealplan.create(
        db=db,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
    )

    assert mealplan_in is not None

    mealplan_updated = mealplan.update(
        db=db,
        id=mealplan_in.id,
        date="2022-02-02",
        name="second lunch",
        servings=3.0,
        recipe_id=recipe_in.id,
    )

    assert mealplan_updated is mealplan_in
    assert mealplan_updated.recipe is recipe_in
    assert mealplan_updated.date.strftime("%Y-%m-%d") == "2022-02-02"
    assert mealplan_updated.name == "second lunch"
    assert mealplan_updated.servings == 3.0


def test_update_nonexistent(db: Session) -> None:
    db_obj = mealplan.update(
        db=db,
        id=1,
        date="2022-01-01",
        name="lunch",
        servings=2.0,
        recipe_id=1,
    )

    assert db_obj is None
