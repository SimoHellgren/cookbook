from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from backend.app.models import RecipeIngredient


class Ingredient(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    recipes: List["RecipeIngredient"] = relationship(
        "RecipeIngredient", back_populates="ingredient", uselist=True
    )
