
let state = {
  recipes: [],
  ingredients: [],
  recipe_ingredients: [],
  mealplans: []
}

const APIURL = "http://localhost:8000"

//api
let api = (function() {

  //default stuff
  const endpoint = path => {
    return {
      get: () => fetch(APIURL + path).then(r => r.json()),
      getId: id => fetch(APIURL + path + "/" + id).then(r => r.json()),
      post: data => fetch(APIURL + path, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      }).then(r => r.json()),
      put: (id, data) => fetch(APIURL + path + "/" + id, {
        method: "PUT",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
    }
  }
  
  //expose endpoints
  return {
      recipes: endpoint("/recipes"),
      ingredients: endpoint("/ingredients"),
      recipe_ingredients: endpoint("/recipe_ingredients"),
      mealplans: endpoint("/mealplans")
  }
  
})()

// DOM manipulation
let D = document
let $body = D.querySelector("body")
let $app = D.getElementById("app")

//components
const Navbar = () => {
  const pages = [
    ["Recipes", render(RecipesPage)], 
    ["Add recipe", () => alert("Not implemented :)")], 
    ["Mealplan", render(MealplanPage)], 
    ["Shopping list", () => alert("Not implemented :)")]
  ]
  
  let nav = D.createElement("nav")
  let ul = D.createElement("ul")

  pages.forEach(([page, callback]) => {
    let li = D.createElement("li")
    li.innerHTML = `<span class="navbar-link">${page}</span>`
    li.onclick = callback
    ul.appendChild(li)
  })

  nav.append(ul)
  
  // tbh not a huge fan of this
  $body.replaceChild(nav, $body.querySelector("nav"))
}

const TagGrid = (tags) => {
  let taggrid = D.createElement("div")
  taggrid.className = "tag-grid"

  let elements = tags.map(tag => {
    let elem = D.createElement("div")
    elem.className = "tag"
    elem.textContent = tag

    elem.onclick = (ev) => {
      ev.stopPropagation()
      alert("You clicked on tag " + tag)
    }

    return elem
  })

  taggrid.append(...elements)

  return taggrid
}

const RecipeCard = ({ id, name, servings, tags }) => {
  let card = D.createElement("div")
  card.setAttribute("class", "recipe-card")
  card.onclick = () => window.open(`recipe.html?recipe=${id}`)

  let h2 = D.createElement("h2")
  h2.textContent = `${name} (${servings})`
  card.appendChild(h2)

  if (tags !== "") {
    let taggrid = TagGrid(tags.split(","))
    card.appendChild(taggrid)
  }

  return card;
}

const RecipeGrid = (recipes) => {
  let $grid = D.createElement("div")
  $grid.className = "recipe-grid"
  let cards = recipes.map(RecipeCard)
  $grid.replaceChildren(...cards)

  return $grid
}

const RecipeSearch = () => {
    let $sidebar = D.createElement("div")
    $sidebar.className = "sidebar"

    let p = D.createElement("p")
    p.textContent = "Search recipes"

    let form = document.createElement("form")
    
    let input = D.createElement("input")
    input.placeholder = "Search by name"
    
    let submit = D.createElement("input")
    submit.setAttribute("type", "submit")
    submit.setAttribute("hidden", "")

    form.append(input, submit)

    form.onsubmit = (ev) => {
      ev.preventDefault()

      let data = state.recipes.filter(r => r.name.toLowerCase().includes(input.value.toLowerCase()))
      let $grid = D.querySelector(".recipe-grid")

      $grid.replaceWith(RecipeGrid(data))
    }

    let alltags = new Set(state.recipes.map(r => r.tags.split(",")).flat().filter(e => e !== ""))

    $sidebar.append(
      p,
      form,
      TagGrid([...alltags])
    )

    return $sidebar
}

const MealCard = (mealplan) => {
  let card = D.createElement("div")
  card.className = "mealcard"
  card.setAttribute("id", mealplan.id)
  card.setAttribute("data-date", mealplan.date)

  let header = D.createElement("div")
  header.className = "mealcard-header"
  header.textContent = `${mealplan.date} ${mealplan.name} (${mealplan.servings})`

  let recipedropdown = D.createElement("select")
  recipedropdown.append(
    new Option("", null, true), //empty choice as default
    ...state.recipes.map(r => new Option(r.name, r.id, false, false))
  )

  recipedropdown.value = mealplan.recipe_id

  card.append(header, recipedropdown)

  return card
}

const Mealplan = (mealplans) => {
  return mealplans.map(MealCard)
}

//pages
const render = page => {
  return () => {
    Navbar()
    $app.replaceChildren(...page())
  }
}

const RecipesPage = () => {
  return [
    RecipeSearch(),
    RecipeGrid(state.recipes)
  ]
}

const MealplanPage = () => {
  return [
    ...Mealplan(state.mealplans)
  ]
}


//Event handlers


//Initial state
api.recipes.get()
  .then(data => state.recipes = data)
  .then(render(RecipesPage))

api.mealplans.get()
  .then(data => state.mealplans = data)
