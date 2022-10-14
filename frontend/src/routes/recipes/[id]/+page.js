import api from '$lib/api'

export async function load({ fetch, params }) {
  const base = 'http://127.0.0.1:8000/recipes';
  const recipe = await api.recipes.get(params.id);
  const ingredients = (await fetch(`${base}/${params.id}/ingredients`)).json();
  const comments = (await fetch(`${base}/${params.id}/comments`)).json();
  return {
    recipe,
    ingredients,
    comments,
  };
}
