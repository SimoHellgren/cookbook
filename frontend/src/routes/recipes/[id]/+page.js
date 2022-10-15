import api from '$lib/api'
import comments from '$lib/stores/comments.js'

export async function load({ fetch, params }) {
  const recipe = await api.recipes.get(params.id);
  const ingredients = await api.recipes.ingredients.get(params.id);

  await comments.getForId(params.id)

  return {
    recipe,
    ingredients,
  };
}
