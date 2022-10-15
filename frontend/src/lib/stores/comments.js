import { writable } from 'svelte/store'
import api from '$lib/api'

const makeStore = () => {
  const { subscribe, set, update } = writable([]);

  const getForId = (id) => api.recipes.comments.get(id).then(set)

  return {
    subscribe,
    getForId,
    update,
  }
}

export default makeStore();
