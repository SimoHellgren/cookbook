from decimal import Decimal
from datetime import date
import random
import string
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.schemas.ingredient import IngredientCreate
from backend.app.schemas.recipe import RecipeCreate
from backend.app.models import Mealplan
from backend.app import crud
from backend.app.schemas.recipe_ingredient import RecipeIngredientCreate


def random_string(length=16):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_decimal():
    return Decimal(random.randint(0, 999)) / Decimal(100)


def create_random_recipe(db: Session) -> models.Recipe:
    recipe_in = RecipeCreate(
        name=random_string(),
        method=random_string(),
        servings=random_decimal(),
        tags=f"{random_string()},{random_string()}",
    )

    return crud.recipe.create(db, recipe_in)


def create_random_recipe_with_ingredients(
    db: Session, ingredient_count: int = 1
) -> Tuple[models.Recipe, List[models.Ingredient], List[models.RecipeIngredient]]:
    recipe = create_random_recipe(db)

    # generate random ingredient names
    names = set()
    while len(names) < ingredient_count:
        names.add(random_string())

    ingredients = [
        crud.ingredient.create(db, IngredientCreate(name=name)) for name in names
    ]

    recipe_ingredients = [
        crud.recipe_ingredient.create(
            db,
            RecipeIngredientCreate(
                recipe_id=recipe.id,
                ingredient_id=ing.id,
                quantity=random_decimal(),
                measure=random_string(3),
                optional=random.random() > 0.5,
                position=i,
            ),
        )
        for i, ing in enumerate(ingredients, 1)
    ]

    return recipe, ingredients, recipe_ingredients


def create_random_mealplan(db: Session, recipe_id: Optional[int] = None):
    mealplan = Mealplan(
        date=date(2022, 6, 15),
        name=random_string(),
        servings=random_decimal(),
        recipe_id=recipe_id,
        position=1,
    )

    db.add(mealplan)
    db.commit()
    db.refresh(mealplan)
    return mealplan
