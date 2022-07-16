import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from backend.app.crud import recipe, ingredient


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


def test_create_recipe_twice_fails(db: Session) -> None:
    recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        recipe.create(
            db=db,
            name="Test recipe",
            servings=2.0,
            method="Do the thing with the ingredients",
            tags="japan,食べ物",
        )


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

    assert obj_1 in db_rows
    assert obj_2 in db_rows


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


def test_add_ingredient(db: Session) -> None:
    recipe_in = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    ingredient_in = ingredient.create(
        db=db,
        name="Ingredient name"
    )

    recipe_ingredient = recipe.add_ingredient(
        db=db,
        recipe_id=recipe_in.id,
        ingredient_id=ingredient_in.id,
        quantity=10.0,
        measure="dl",
        optional=True,
    )

    assert recipe_ingredient.recipe_id == recipe_in.id
    assert recipe_ingredient.ingredient_id == ingredient_in.id
    assert recipe_ingredient.quantity == 10.0
    assert recipe_ingredient.measure == "dl"
    assert recipe_ingredient.optional


def test_get_recipe_ingredients(db: Session) -> None:
    recipe_in = recipe.create(
        db=db,
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    ingredient_in = ingredient.create(
        db=db,
        name="Ingredient name"
    )

    recipe_ingredient_in = recipe.add_ingredient(
        db=db,
        recipe_id=recipe_in.id,
        ingredient_id=ingredient_in.id,
        quantity=10.0,
        measure="dl",
        optional=True,
    )

    db_recipe_ingredients = recipe.get_ingredients(db, recipe_in.id)
    assert recipe_ingredient_in in db_recipe_ingredients
    assert [recipe_ingredient_in] == db_recipe_ingredients
