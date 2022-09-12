from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class RecipeBase(BaseModel):
    name: str
    servings: Decimal
    method: str
    tags: str
    source: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    id: int


class Recipe(RecipeBase):
    """For use as API response model"""

    id: int

    class Config:
        orm_mode = True
