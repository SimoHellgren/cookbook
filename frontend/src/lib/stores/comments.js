import { writable } from 'svelte/store'
import api from '$lib/api'

const makeStore = () => {
  const { subscribe, set, update } = writable([]);

  const getForId = (id) => api.recipes.comments.get(id).then(set)

  const create = (data) => api.comments.create(data).then(r => update(s => [...s, r]))

  const edit = (id, data) => api.comments.update(id, data).then(r => update(s => s.map(c => c.id === r.id ? r : c)))

  return {
    subscribe,
    getForId,
    create,
    update: edit,
  }
}

export default makeStore();
