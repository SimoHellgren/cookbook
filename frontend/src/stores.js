import { writable } from 'svelte/store'

const initRecipes = () => {
  const { subscribe, set, update } = writable([]);

  fetch("http://127.0.0.1:8000/recipes")
    .then(response => response.json())
    .then(data => set(data))

  return {
    subscribe,
    set,
    update
  }
}

export const recipes = initRecipes();
