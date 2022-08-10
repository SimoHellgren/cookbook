from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app import crud
from backend.app.dependencies import get_db
from backend.app.schemas.recipe_ingredient import (
    RecipeIngredient,
    RecipeIngredientUpdate,
)

router = APIRouter(prefix="/recipe_ingredients")


@router.get("/", response_model=List[RecipeIngredient])
def get_many(db: Session = Depends(get_db)) -> Any:
    return crud.recipe_ingredient.get_many(db)


@router.put(
    "/{recipe_id}:{ingredient_id}",
    response_model=RecipeIngredient,
    status_code=status.HTTP_200_OK,
)
def put(
    recipe_id: int,
    ingredient_id: int,
    obj_in: RecipeIngredientUpdate,
    db: Session = Depends(get_db),
) -> Any:
    db_obj = crud.recipe_ingredient.get(db, recipe_id, ingredient_id)

    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return crud.recipe_ingredient.update(db, db_obj, obj_in)


@router.delete("/{recipe_id}:{ingredient_id}", response_model=RecipeIngredient)
def delete(recipe_id: int, ingredient_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.recipe_ingredient.remove(
        db=db, recipe_id=recipe_id, ingredient_id=ingredient_id
    )
