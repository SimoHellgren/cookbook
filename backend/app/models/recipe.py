from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base


class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    servings = Column(Numeric)
    method = Column(String)
    tags = Column(String)

    ingredients = relationship(
        "Ingredient", secondary="recipe_ingredient", back_populates="recipes"
    )
    mealplans = relationship("Mealplan", back_populates="recipe")