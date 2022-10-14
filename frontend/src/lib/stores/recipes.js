import { writable } from 'svelte/store';
import api from '$lib/api'

const initRecipes = () => {
  const { subscribe, set, update } = writable([]);

  api.recipes.getAll().then(data => set(data));

  const create = (data) => api.recipes.create(data).then(d => update(s => {
    [...s, d]
    return d
  }))
  const edit = (id, data) => api.recipes
    .update(id, data)
    .then(data => update(state => state.map(s => s.id === data.id ? data : s)))

  const remove = (id) => api.recipes.remove(id).then(data => update(state => state.filter(s => s.id !== data.id)))

  return {
    subscribe,
    set,
    update,
    create,
    edit,
    remove,
  };
};

export default initRecipes();
