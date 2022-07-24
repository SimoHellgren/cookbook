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
let $searchform = D.getElementById("search")
let $searchvalue = D.getElementById("search-value")

const createRecipeGridCard = ({ id, name, servings, tags }) => {
  let card = D.createElement("div")
  card.setAttribute("class", "recipe-card")

  let h2 = D.createElement("h2")
  h2.textContent = `${name} (${servings})`
  h2.onclick = () => fetchRecipe(id).then(r => alert(r.method))
  card.appendChild(h2)

  let taggrid = D.createElement("div")
  taggrid.setAttribute("class", "tag-grid")

  if (tags !== "") {
    tags.split(",").forEach(t => {
      let e = D.createElement("div")
      e.setAttribute("class", "tag")
      e.textContent = t
      taggrid.appendChild(e)
    })

    card.appendChild(taggrid)
  }

  return card;
}

const drawRecipeGrid = (recipes) => {
  let cards = recipes.map(createRecipeGridCard)
  $recipegrid.replaceChildren(...cards)
}

//Event handlers
const onSearchSubmit = (event) => {
  //consider hiding cards instead of destroying and recreating the elements
  event.preventDefault()
  drawRecipeGrid(state.recipes.filter(r => r.name.toLowerCase().includes($searchvalue.value.toLowerCase())))
}

$searchform.onsubmit = onSearchSubmit

//Initial state
fetchRecipes()
  .then(() => drawRecipeGrid(state.recipes))
  .then(_ => {
    // set search tags
    let container = D.getElementById("search-tags")
    alltags = new Set(state.recipes.map(r => r.tags.split(",")).flat().filter(e => e !== ""))

    alltags.forEach(t => {
      let e = D.createElement("div")
      e.setAttribute("class", "tag")
      e.textContent = t
      container.appendChild(e)
    })
  })