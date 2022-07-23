from fastapi import FastAPI
from backend.app.routers import recipes
from backend.app.routers import recipe_ingredients
from backend.app.routers import ingredients

app = FastAPI()

app.include_router(recipes.router)
app.include_router(recipe_ingredients.router)
app.include_router(ingredients.router)


@app.get("/")
def root() -> str:
    return "Hello there"
