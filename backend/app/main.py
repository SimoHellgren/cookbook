from fastapi import FastAPI
from backend.app.routers import recipes

app = FastAPI()

app.include_router(recipes.router)


@app.get("/")
def root() -> str:
    return "Hello there"
