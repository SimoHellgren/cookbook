from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app import crud
from backend.app.schemas.recipe import Recipe, RecipeCreate, RecipeUpdate
from backend.app.dependencies import get_db

router = APIRouter(
    prefix="/recipes"
)


@router.get("/", response_model=List[Recipe])
def get_many(db: Session = Depends(get_db)):
    return crud.recipe.get_many(db=db)


@router.get("/{recipe_id}", response_model=Recipe)
def get(recipe_id: int, db: Session = Depends(get_db)):
    db_obj = crud.recipe.get(db, id=recipe_id)

    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_obj


@router.post("/", response_model=Recipe, status_code=status.HTTP_201_CREATED)
def create(recipe: RecipeCreate, db: Session = Depends(get_db)):
    return crud.recipe.create(db, recipe)


@router.put("/{recipe_id}", response_model=Recipe, status_code=status.HTTP_200_OK)
def update(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)):
    db_recipe = crud.recipe.get(db, recipe_id)

    if not db_recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return crud.recipe.update(db, db_obj=db_recipe, obj_in=recipe)


@router.delete("/{recipe_id}", response_model=Recipe, status_code=status.HTTP_200_OK)
def delete(recipe_id: int, db: Session = Depends(get_db)):
    return crud.recipe.remove(db, recipe_id)
