import { writable } from 'svelte/store'

const BASE = "http://127.0.0.1:8000/ingredients"

const initIngredients = () => {
  const { subscribe, set, update } = writable([]);

  fetch(BASE)
    .then(response => response.json())
    .then(data => set(data))

  const add = async (data) => {
    const response = await fetch(BASE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })

    const ingredient = await response.json()
    update(state => [...state, ingredient])

    return ingredient;
  }

  return {
    subscribe,
    set,
    update,
    add,
  }
}


export default initIngredients();
