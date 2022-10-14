import api from '$lib/api'
import { writable } from 'svelte/store';

const initIngredients = () => {
  const { subscribe, set, update } = writable([]);

  api.ingredients.getAll().then(data => set(data))

  const add = async (data) => api.ingredients.create(data).then(d => {
    update(state => [...state, d])
    return d
  })

  return {
    subscribe,
    set,
    update,
    add,
  };
};

export default initIngredients();
