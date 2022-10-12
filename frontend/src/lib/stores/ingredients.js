import { writable } from 'svelte/store'

const BASE = "http://127.0.0.1:8000"

const initIngredients = () => {
  const { subscribe, set, update } = writable([]);

  fetch(BASE + "/ingredients")
    .then(response => response.json())
    .then(data => set(data))

  return {
    subscribe,
    set,
    update,
  }
}


export default initIngredients();
