from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app import crud
from backend.app.dependencies import get_db
from backend.app.schemas.ingredient import Ingredient, IngredientCreate


router = APIRouter(prefix="/ingredients")


@router.get("/", response_model=List[Ingredient])
def get_many(db: Session = Depends(get_db)) -> Any:
    return crud.ingredient.get_many(db=db)


@router.get("/{ingredient_id}", response_model=Ingredient)
def get(ingredient_id: int, db: Session = Depends(get_db)) -> Any:
    db_obj = crud.ingredient.get(db, id=ingredient_id)

    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_obj


@router.post("/", response_model=Ingredient, status_code=status.HTTP_201_CREATED)
def create(ingredient: IngredientCreate, db: Session = Depends(get_db)) -> Any:
    return crud.ingredient.create(db, ingredient)
