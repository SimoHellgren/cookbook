export async function load() {
  return {
    mealplans: (await fetch("http://127.0.0.1:8000/mealplans")).json(),
    recipes: (await fetch("http://127.0.0.1:8000/recipes")).json(),
  }
}