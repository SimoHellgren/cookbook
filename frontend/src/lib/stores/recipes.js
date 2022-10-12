import { writable } from 'svelte/store'

const BASE = "http://127.0.0.1:8000/recipes"

const initRecipes = () => {
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

    const recipe = await response.json()

    update(state => [...state, recipe])

    return recipe
  }

  const edit = async (id, data) => {
    const response = await fetch(BASE + `/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })

    const recipe = await response.json()

    update(state => state.map(r => r.id === id ? recipe : r))

    return recipe

  }

  return {
    subscribe,
    set,
    update,
    add,
    edit,
  }
}

export default initRecipes();