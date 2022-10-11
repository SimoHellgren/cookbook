export async function load({ params, fetch }) {
  const response = await fetch(`http://127.0.0.1:8000/recipes/${params.id}`)
  const recipe = await response.json()
  return recipe
}