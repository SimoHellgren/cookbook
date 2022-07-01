from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from backend.db.base_class import Base


class Mealplan(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    servings = Column(Numeric)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    recipe = relationship('Recipe', back_populates="mealplans")
