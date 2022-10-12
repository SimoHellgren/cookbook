import { writable } from 'svelte/store'

const BASE = "http://127.0.0.1:8000"

const initRecipes = () => {
  const { subscribe, set, update } = writable([]);

  fetch(BASE + "/recipes")
    .then(response => response.json())
    .then(data => set(data))

  return {
    subscribe,
    set,
    update,
  }
}

export default initRecipes();