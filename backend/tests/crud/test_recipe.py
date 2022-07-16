import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from backend.app.schemas.recipe import RecipeCreate
from backend.app.crud import recipe, ingredient


def test_create(db: Session) -> None:
    obj_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    obj = recipe.create(db=db, obj_in=obj_in)

    assert obj.id
    assert obj.name == "Test recipe"
    assert obj.servings == 2.0
    assert obj.method == "Do the thing with the ingredients"
    assert obj.tags == "japan,食べ物"


def test_create_twice_fails(db: Session) -> None:
    obj_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    recipe.create(db=db, obj_in=obj_in)

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        recipe.create(db=db, obj_in=obj_in)


def test_get(db: Session) -> None:
    obj_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_obj = recipe.create(db=db, obj_in=obj_in)
    get_obj = recipe.get(db, db_obj.id)

    assert get_obj
    assert get_obj.id == db_obj.id
    assert get_obj.name == db_obj.name
    assert get_obj.servings == db_obj.servings
    assert get_obj.method == db_obj.method
    assert get_obj.tags == db_obj.tags


def test_get_nonexistent(db: Session) -> None:
    obj = recipe.get(db, 1)
    assert obj is None


def test_get_many(db: Session) -> None:
    obj_in_1 = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    obj_in_2 = RecipeCreate(
        name="Test recipe 2 - electric boogaloo",
        servings=1.0,
        method="Cook the things",
        tags="Spain,fish",
    )

    db_obj_1 = recipe.create(db=db, obj_in=obj_in_1)
    db_obj_2 = recipe.create(db=db, obj_in=obj_in_2)

    db_rows = recipe.get_many(db)

    assert db_rows
    assert len(db_rows) == 2

    assert db_obj_1 in db_rows
    assert db_obj_2 in db_rows


def test_delete(db: Session) -> None:
    obj_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_obj = recipe.create(db=db, obj_in=obj_in)

    deleted_obj = recipe.remove(db, db_obj.id)
    assert deleted_obj is not None

    assert recipe.get(db, db_obj.id) is None
    assert db_obj.id == deleted_obj.id


def test_add_ingredient(db: Session) -> None:
    recipe_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_recipe = recipe.create(db=db, obj_in=recipe_in)

    ingredient_in = ingredient.create(db=db, name="Ingredient name")

    recipe_ingredient = recipe.add_ingredient(
        db=db,
        recipe_id=db_recipe.id,
        ingredient_id=ingredient_in.id,
        quantity=10.0,
        measure="dl",
        optional=True,
    )

    assert recipe_ingredient.recipe_id == db_recipe.id
    assert recipe_ingredient.ingredient_id == ingredient_in.id
    assert recipe_ingredient.quantity == 10.0
    assert recipe_ingredient.measure == "dl"
    assert recipe_ingredient.optional


def test_get_recipe_ingredients(db: Session) -> None:
    recipe_in = RecipeCreate(
        name="Test recipe",
        servings=2.0,
        method="Do the thing with the ingredients",
        tags="japan,食べ物",
    )

    db_recipe = recipe.create(db=db, obj_in=recipe_in)

    ingredient_in = ingredient.create(db=db, name="Ingredient name")

    recipe_ingredient_in = recipe.add_ingredient(
        db=db,
        recipe_id=db_recipe.id,
        ingredient_id=ingredient_in.id,
        quantity=10.0,
        measure="dl",
        optional=True,
    )

    db_recipe_ingredients = recipe.get_ingredients(db, db_recipe.id)
    assert recipe_ingredient_in in db_recipe_ingredients
    assert [recipe_ingredient_in] == db_recipe_ingredients
