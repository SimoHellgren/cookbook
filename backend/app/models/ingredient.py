from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base


class Ingredient(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    recipes = relationship("RecipeIngredient", back_populates="ingredient")
