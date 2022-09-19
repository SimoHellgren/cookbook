from datetime import datetime
from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    id: int


class Ingredient(IngredientBase):
    """For use as API response model"""

    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
