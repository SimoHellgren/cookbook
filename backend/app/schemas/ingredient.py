from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    id: int
