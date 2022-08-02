const APIURL = "http://localhost:8000"

let state = {
  recipes: []
}

//api
let api = (function() {

  //default stuff
  const endpoint = path => {
    return {
      get: () => fetch(APIURL + path).then(r => r.json()),
      getId: id => fetch(APIURL + path + `/${id}`).then(r => r.json()),
      post: data => fetch(APIURL + path, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      }).then(r => r.json())
    }
  }
  
  //expose endpoints
  return {
      recipes: endpoint("/recipes"),
      ingredients: endpoint("/ingredients")
  }
  
})()


// DOM manipulation
let D = document
let $recipegrid = D.getElementById("recipe-grid")
let $searchform = D.getElementById("search")
let $searchvalue = D.getElementById("search-value")

const createRecipeGridCard = ({ id, name, servings, tags }) => {
  let card = D.createElement("div")
  card.setAttribute("class", "recipe-card")
  card.onclick = () => window.open(`recipe.html?recipe=${id}`)

  let h2 = D.createElement("h2")
  h2.textContent = `${name} (${servings})`
  card.appendChild(h2)

  let taggrid = D.createElement("div")
  taggrid.setAttribute("class", "tag-grid")

  if (tags !== "") {
    tags.split(",").forEach(tag => {
      let e = D.createElement("div")
      e.setAttribute("class", "tag")
      e.textContent = tag
      e.onclick = (event) => {
        event.stopPropagation()
        alert(`You clicked on tag ${tag}`)
      }
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
api.recipes.get()
  .then(data => state.recipes = data)
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