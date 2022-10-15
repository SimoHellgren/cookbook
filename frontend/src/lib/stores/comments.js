import { writable } from 'svelte/store'
import api from '$lib/api'

const makeStore = () => {
  const { subscribe, set, update } = writable([]);

  const getForId = (id) => api.recipes.comments.get(id).then(set)

  const create = (data) => api.comments.create(data).then(r => update(s => [...s, r]))

  return {
    subscribe,
    getForId,
    create,
  }
}

export default makeStore();
