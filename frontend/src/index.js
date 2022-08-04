
let state = {
  recipes: [],
  ingredients: [],
  recipe_ingredients: [],
  mealplans: [],
}

const APIURL = "http://localhost:8000"

//utilities
const daterange = (start, end) => {
  var arr = []
  for (var d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) arr.push(new Date(d))
  return arr
}

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
      }).then(r => r.json())
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
  let container = D.createElement("div")
  container.className = "mealplan-container"
  
  container.append(
    ...mealplans.map(MealCard)
  )

  return container
}

const DateRangeFilter = () => {
  let form = D.createElement("form")
  let start = D.createElement("input")
  let end = D.createElement("input")
  start.setAttribute("type", "date")
  end.setAttribute("type", "date")
  start.id = "start_date"
  end.id = "end_date"

  let start_label = D.createElement("label") 
  let end_label = D.createElement("label") 
  start_label.setAttribute("for", start.id)
  end_label.setAttribute("for", end.id)
  start_label.textContent = "Start date"
  end_label.textContent = "End date"

  //eventhandlers for changes

  //this will need a refactoring when shopping list is implemented
  const callback = () => {
    sd = start.value || "0000-00-00"
    ed = end.value || "9999-99-99"

    let show_data = state.mealplans.filter(mp => ((sd <= mp.date) && (mp.date <= ed)))

    let container = D.querySelector(".mealplan-container")
    container.replaceWith(Mealplan(show_data))
  }

  start.addEventListener("change", callback)
  end.addEventListener("change", callback)

  form.append(
    start_label,
    start,
    end_label,
    end,
  )
  return form
}

const CreateMealpanForm = () => {
  let form = D.createElement("form")
  let start = D.createElement("input")
  let end = D.createElement("input")
  start.setAttribute("type", "date")
  end.setAttribute("type", "date")
  start.id = "start_date"
  end.id = "end_date"
  let start_label = D.createElement("label")
  let end_label = D.createElement("label")
  start_label.setAttribute("for", start.id)
  end_label.setAttribute("for", end.id)
  start_label.textContent = "Start date"
  end_label.textContent = "End date"

  //set end date to start by default
  start.addEventListener("change", () => {
    if (!end.value) end.value = start.value
  }, {once: true}) 

  let mealinput = D.createElement("textarea")
  mealinput.id = "meals-input"
  mealinput.textContent = "lunch;2\ndinner;2"
  let meallabel = D.createElement("label")
  meallabel.setAttribute("for", mealinput.id)
  meallabel.textContent = "Meals"

  let submit = D.createElement("button")
  submit.textContent = "Create!"

  form.onsubmit = (ev) => {
    ev.preventDefault()

    if (!start.value) {
      alert("Please provide a start date")
      ev.stopImmediatePropagation()
      return
    }

    let sd = new Date(start.value)
    let ed = new Date(end.value)
    let meals = mealinput.value.split("\n").map(e => e.split(";"))
    
    let dates = daterange(sd, ed).map(d => d.toISOString().slice(0,10))

    let plans = dates.map(date => meals.map(([name, servings]) => (
      {
        date,
        name,
        servings,
      }  
    ))).flat()
    
    Promise.all(plans.map(api.mealplans.post))
      .then(data => state.mealplans = state.mealplans.concat(data).sort((a, b) => b.date > a.date ? -1 : 1))
      .then(() => {
        let container = D.querySelector(".mealplan-container")
        container.replaceWith(Mealplan(state.mealplans))
      })
  }

  form.append(start_label, start, end_label, end, meallabel, mealinput, submit)

  return form
}

const CreateMealplans = () => {
  let overlay = D.createElement("div")
  overlay.id = "overlay"

  let modal = D.createElement("div")
  modal.className = "modal"

  const closefunc = () => {
    modal.classList.remove("active")
    overlay.classList.remove("active")
  }
  
  let header = D.createElement("div")
  header.className = "modal-header"
  
  let headertext = D.createElement("div")
  headertext.className = "title"
  headertext.textContent = "Create mealplans"

  let closebutton = D.createElement("button")
  closebutton.className = "closebutton"
  closebutton.textContent = "\u00D7" //multiplication symbol
  closebutton.onclick = closefunc

  header.append(headertext, closebutton)
  
  let body = D.createElement("div")
  body.className = "modal-body"

  form = CreateMealpanForm()

  form.addEventListener("submit", closefunc)

  body.append(form)

  modal.append(header, body)

  return [modal, overlay]
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
  let save = D.createElement("button")
  save.textContent = "Save"
  
  save.onclick = () => {
    let container = D.querySelector(".mealplan-container")

    container.childNodes.forEach(card => {
      let plan_id = parseInt(card.getAttribute("id"))
      let recipe_id = parseInt(card.getElementsByTagName("select").item(0).value)
      
      const plan = state.mealplans.find(mp => mp.id === plan_id)
      const newPlan = {
        ...plan,
        recipe_id
      }
      
      //this isn't very efficient put shall do for now
      api.mealplans.put(plan_id, newPlan)
        .then(data => state.mealplans = state.mealplans.map(mp => mp.id === data.id ? data : mp))
    })
  }

  //modal stuff
  [modal, overlay] = CreateMealplans()

  let createbutton = D.createElement("button")
  createbutton.textContent = "Create!"
  createbutton.onclick = () => {
    modal.classList.add("active")
    overlay.classList.add("active")
  }

  return [
    DateRangeFilter(),
    createbutton,
    modal, 
    overlay,
    Mealplan(state.mealplans),
    save
  ]
}


//Event handlers


//Initial state
api.recipes.get()
  .then(data => state.recipes = data)
  .then(render(RecipesPage))

api.mealplans.get()
  .then(data => state.mealplans = data.sort((a,b) => b.date > a.date ? -1 : 1))
