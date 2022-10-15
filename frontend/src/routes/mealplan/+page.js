import api from '$lib/api'

export async function load({ fetch }) {
  return {
    mealplans: await api.mealplans.getAll(),
  };
}
