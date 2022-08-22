from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app import crud
from backend.app.dependencies import get_db
from backend.app.schemas.mealplan import Mealplan, MealplanCreate, MealplanUpdate


router = APIRouter(prefix="/mealplans")


@router.get("/", response_model=List[Mealplan])
def get_many(db: Session = Depends(get_db)) -> Any:
    return crud.mealplan.get_many(db=db)


@router.get("/{mealplan_id}", response_model=Mealplan)
def get(mealplan_id: int, db: Session = Depends(get_db)) -> Any:
    db_obj = crud.mealplan.get(db, id=mealplan_id)

    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_obj


@router.post("/", response_model=Mealplan, status_code=status.HTTP_201_CREATED)
def create(mealplan: MealplanCreate, db: Session = Depends(get_db)) -> Any:
    return crud.mealplan.create(db, mealplan)


@router.put("/{mealplan_id}", response_model=Mealplan, status_code=status.HTTP_200_OK)
def update(
    mealplan_id: int, mealplan: MealplanUpdate, db: Session = Depends(get_db)
) -> Any:
    db_mealplan = crud.mealplan.get(db, mealplan_id)

    if not db_mealplan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return crud.mealplan.update(db, db_obj=db_mealplan, obj_in=mealplan)


@router.delete("/{mealplan_id}", response_model=Mealplan, status_code=200)
def delete(mealplan_id: int, db: Session = Depends(get_db)):
    return crud.mealplan.remove(db=db, id=mealplan_id)
