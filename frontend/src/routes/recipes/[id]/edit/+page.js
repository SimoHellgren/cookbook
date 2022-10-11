export async function load({ params, fetch }) {
  const recipe = await (await fetch(`http://127.0.0.1:8000/recipes/${params.id}`)).json()
  const ingredients_data = await (await fetch(`http://127.0.0.1:8000/recipes/${params.id}/ingredients`)).json()

  const ingredients = ingredients_data.map(i => ({
    name: i.ingredient.name,
    quantity: i.quantity,
    measure: i.measure,
    optional: i.optional,
    position: i.position,
  })).sort((a, b) => a.position - b.position)

  return {
    recipe, ingredients
  }
}