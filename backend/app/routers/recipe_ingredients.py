from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from backend.app import crud
from backend.app.dependencies import get_db
from backend.app.schemas.recipe_ingredient import RecipeIngredient

router = APIRouter(prefix="/recipe_ingredients")


@router.get("/", response_model=List[RecipeIngredient])
def get_many(db: Session = Depends(get_db)):
    return crud.recipe_ingredient.get_many(db)
