from sqlalchemy.orm import Session
from backend.app.crud import recipe


def test_create_recipe(db: Session) -> None:
    obj = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    assert obj.id
    assert obj.name == "Test recipe"
    assert obj.servings == 2.0
    assert obj.method == "Do the thing with the ingredients"
    assert obj.tags == "japan,食べ物"


def test_get_recipe(db: Session) -> None:
    obj_in = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_obj = recipe.get(db, obj_in.id)

    assert db_obj
    assert db_obj.id == obj_in.id
    assert db_obj.name == obj_in.name
    assert db_obj.servings == obj_in.servings
    assert db_obj.method == obj_in.method
    assert db_obj.tags == obj_in.tags


def test_get_nonexistent_recipe(db: Session) -> None:
    obj = recipe.get(db, 1)
    assert obj is None


def test_get_many_recipes(db: Session) -> None:
    obj_1 = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    obj_2 = recipe.create(
        db=db,
        name="Test recipe 2 - electric boogaloo",
        servings=1.0,
        method="Cook the things",
        tags="Spain,fish",
    )

    db_rows = recipe.get_all(db)

    assert db_rows
    assert len(db_rows) == 2

    db_ids = [row.id for row in db_rows]
    assert obj_1.id in db_ids
    assert obj_2.id in db_ids


def test_delete_recipe(db: Session) -> None:
    obj_in = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    deleted_obj = recipe.delete(db, obj_in.id)

    assert recipe.get(db, obj_in.id) is None
    assert obj_in.id == deleted_obj.id
