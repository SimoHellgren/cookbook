import api from '$lib/api'

export async function load({ fetch, params }) {
  const recipe = await api.recipes.get(params.id);
  const ingredients = await api.recipes.ingredients.get(params.id);
  const comments = await api.recipes.comments.get(params.id);
  return {
    recipe,
    ingredients,
    comments,
  };
}
