
const BASE = 'http://127.0.0.1:8000'

const endpoint = (path) => {
  const URL = BASE + '/' + path;

  const getAll = async () => {
    const response = await fetch(URL)
    return response.json()
  }

  const get = async (id) => {
    const response = await fetch(URL + '/' + id)
    return response.json()
  }

  const create = async (data) => {
    const response = await fetch(URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return response.json()
  }

  const update = async (id, data) => {
    const response = await fetch(URL, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return response.json()
  }

  const remove = async (id) => {
    const response = await fetch(URL + '/' + id, {
      method: 'DELETE',
    })
    return response.json()
  }

  return {
    getAll,
    get,
    create,
    update,
    remove,
  }
}

export default {
  recipes: endpoint('recipes'),
}