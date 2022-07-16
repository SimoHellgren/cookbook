from sqlalchemy.orm import Session
from backend.app.crud import ingredient


def test_create_ingredient(db: Session) -> None:
    ingredient_in = ingredient.create(db=db, name="Warm milk")

    assert ingredient_in.id
    assert ingredient_in.name == "Warm milk"


def test_create_returns_existing(db: Session) -> None:
    ingredient_1 = ingredient.create(db=db, name="Warm milk")
    ingredient_2 = ingredient.create(db=db, name="Warm milk")

    assert ingredient_1 is ingredient_2


def test_get_all_ingredients(db: Session) -> None:
    ingredient_1 = ingredient.create(db=db, name="Warm milk")
    ingredient_2 = ingredient.create(db=db, name="Cold milk")

    db_rows = ingredient.get_all(db)

    assert db_rows
    assert len(db_rows) == 2

    assert ingredient_1 in db_rows
    assert ingredient_2 in db_rows
