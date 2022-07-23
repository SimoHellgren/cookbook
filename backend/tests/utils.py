from decimal import Decimal
import random
import string
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.schemas.recipe import RecipeCreate
from backend.app import crud


def random_string(length=16):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_decimal():
    return Decimal(random.randint(0, 999)) / Decimal(100)


def create_random_recipe(db: Session) -> models.Recipe:
    recipe_in = RecipeCreate(
        name=random_string(),
        method=random_string(),
        servings=random_decimal(),
        tags=f"{random_string()},{random_string()}"
    )

    return crud.recipe.create(db, recipe_in)
