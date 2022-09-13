from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app import crud
from backend.app.schemas.comment import Comment
from backend.app.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate
from backend.app.dependencies import get_db
from backend.app.schemas.recipe_ingredient import (
    RecipeIngredient,
    RecipeIngredientCreate,
)

router = APIRouter(prefix="/recipes")


@router.get("/", response_model=list[Recipe])
def get_many(db: Session = Depends(get_db)) -> Any:
    return crud.recipe.get_many(db=db)


@router.get("/{recipe_id}", response_model=Recipe)
def get(recipe_id: int, db: Session = Depends(get_db)) -> Any:
    db_obj = crud.recipe.get(db, id=recipe_id)

    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_obj


@router.post("/", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def create(recipe: RecipeCreate, db: Session = Depends(get_db)) -> Any:
    return crud.recipe.create(db, recipe)


@router.put("/{recipe_id}", response_model=Recipe, status_code=status.HTTP_200_OK)
def update(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)) -> Any:
    db_recipe = crud.recipe.get(db, recipe_id)

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return crud.recipe.update(db, db_obj=db_recipe, obj_in=recipe)


@router.delete("/{recipe_id}", response_model=Recipe, status_code=status.HTTP_200_OK)
def delete(recipe_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.recipe.remove(db, recipe_id)


@router.get("/{recipe_id}/ingredients", response_model=list[RecipeIngredient])
def get_ingredients(recipe_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.recipe.get_ingredients(db, recipe_id)


@router.post(
    "/{recipe_id}/ingredients",
    response_model=RecipeIngredient,
    status_code=status.HTTP_201_CREATED,
)
def add_ingredient(
    recipe_id: int,
    recipe_ingredient: RecipeIngredientCreate,
    db: Session = Depends(get_db),
) -> Any:
    return crud.recipe.add_ingredient(
        db,
        recipe_id,
        recipe_ingredient.ingredient_id,
        recipe_ingredient.quantity,
        recipe_ingredient.measure,
        recipe_ingredient.optional,
        recipe_ingredient.position,
    )


@router.get("/{recipe_id}/comments", response_model=list[Comment])
def get_comments(recipe_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.recipe.get_comments(db, recipe_id)
