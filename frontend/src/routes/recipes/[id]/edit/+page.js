import api from '$lib/api'

export async function load({ params, fetch }) {
  const recipe = await api.recipes.get(params.id);
  const ingredients_data = await api.recipes.ingredients.get(params.id);

  const ingredients = ingredients_data
    .map((i) => ({
      name: i.ingredient.name,
      quantity: i.quantity,
      measure: i.measure,
      optional: i.optional,
      position: i.position,
    }))
    .sort((a, b) => a.position - b.position);

  return {
    recipe,
    ingredients,
  };
}
