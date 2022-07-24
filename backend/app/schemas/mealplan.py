from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class MealplanBase(BaseModel):
    date: date
    name: str
    servings: Decimal


class MealplanCreate(MealplanBase):
    pass


class MealplanUpdate(MealplanBase):
    id: int
    recipe_id: Optional[int]


class Mealplan(MealplanBase):
    """For use as API response model"""

    id: int
    recipe_id: Optional[int]

    class Config:
        orm_mode = True
