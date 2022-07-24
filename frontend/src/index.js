const APIURL = "http://localhost:8000"

let state = {
  recipes: []
}

const fetchRecipes = () => fetch(`${APIURL}/recipes`)
  .then(r => r.json())
  .then(data => state.recipes = data)


const fetchRecipe = async (id) => {
  const response = await fetch(`${APIURL}/recipes/${id}`)
  recipe = await response.json()
  return recipe
}

// DOM manipulation
let D = document
let $recipegrid = D.getElementById("recipe-grid")

const createRecipeGridCard = ({ id, name, servings, tags }) => {
  let card = D.createElement("div")
  card.setAttribute("class", "recipe-card")

  let h2 = D.createElement("h2")
  h2.textContent = `${name} (${servings})`
  h2.onclick = () => fetchRecipe(id).then(r => alert(r.method))
  card.appendChild(h2)

  if (tags !== "") {
    tags.split(",").forEach(t => {
      let e = D.createElement("div")
      e.setAttribute("class", "tag")
      e.textContent = t
      card.appendChild(e)
    })
  }

  return card;
}

const drawRecipeGrid = () => {
  state.recipes.forEach(r => {
    let card = createRecipeGridCard(r)
    $recipegrid.appendChild(card)
  })
}


//Initial state
fetchRecipes()
  .then(drawRecipeGrid)
  .then(_ => {
    // set search tags
    let container = D.getElementById("search-tags")
    alltags = state.recipes.map(r => r.tags.split(",")).flat().filter(e => e !== "")

    alltags.forEach(t => {
      let e = D.createElement("div")
      e.setAttribute("class", "tag")
      e.textContent = t
      container.appendChild(e)
    })
  })