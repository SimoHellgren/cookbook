export async function load() {
  return {
    recipes: (await fetch("http://127.0.0.1:8000/recipes/")).json()
  }
}