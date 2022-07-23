from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    id: int


class Ingredient(IngredientBase):
    """For use as API response model"""

    class Config:
        orm_mode = True