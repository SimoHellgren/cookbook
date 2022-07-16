from sqlalchemy.orm import Session
from backend.app.crud.crud_ingredient import ingredient
from backend.app.schemas.ingredient import IngredientCreate


def test_create(db: Session) -> None:
    obj_in = IngredientCreate(name="Warm milk")
    db_ingredient = ingredient.create(db=db, obj_in=obj_in)

    assert db_ingredient.id
    assert db_ingredient.name == "Warm milk"


def test_get_many(db: Session) -> None:
    obj_in_1 = IngredientCreate(name="Warm milk")
    obj_in_2 = IngredientCreate(name="Cold milk")

    db_obj_1 = ingredient.create(db=db, obj_in=obj_in_1)
    db_obj_2 = ingredient.create(db=db, obj_in=obj_in_2)

    db_rows = ingredient.get_many(db)

    assert db_rows
    assert len(db_rows) == 2

    assert db_obj_1 in db_rows
    assert db_obj_2 in db_rows
