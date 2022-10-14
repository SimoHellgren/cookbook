const BASE = 'http://127.0.0.1:8000'

const endpoint = (path) => {
  const URL = BASE + path;

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
    const response = await fetch(URL + '/' + id, {
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
  recipes: {
    ...endpoint('/recipes'),
    ingredients: {
      get: (id) => fetch(`${BASE}/recipes/${id}/ingredients`).then(d => d.json()),
      add: (recipe_id, data) => fetch(`${BASE}/recipes/${recipe_id}/ingredients`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }).then(d => d.json())
    },
    comments: {
      get: (id) => fetch(`${BASE}/recipes/${id}/comments`).then(d => d.json()),
    }
  },
  ingredients: endpoint('/ingredients'),
  recipe_ingredients: {
    ...endpoint('/recipe_ingredients'),
    update: (recipe_id, ingredient_id, data) =>
      fetch(`${BASE}/recipe_ingredients/${recipe_id}:${ingredient_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      }).then((r) => r.json()),
    remove: (recipe_id, ingredient_id) =>
      fetch(`${BASE}/recipe_ingredients/${recipe_id}:${ingredient_id}`, {
        method: 'DELETE',
      }).then((r) => r.json()),
    update_many: (data) =>
      fetch(`${BASE}/recipe_ingredients/bulk`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      }),
  },
  mealplans: endpoint('/mealplans'),
  comments: endpoint('/comments'),
}