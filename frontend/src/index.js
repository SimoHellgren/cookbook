
let state = {
  recipes: [],
  ingredients: [],
  recipe_ingredients: [],
  mealplans: [],
  selected_recipe: 1,
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
      }).then(r => r.json()),
      delete: id => fetch(APIURL + path + "/" + id, {method: "DELETE"})
        .then(r => r.json())
    }
  }
  
  //expose endpoints
  return {
      recipes: {
        ...endpoint("/recipes"),
        ingredients: {
          add: (recipe_id, data) => fetch(`${APIURL}/recipes/${recipe_id}/ingredients`, {
            method: "POST",
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          }).then(r => r.json())
        }
      },
      ingredients: endpoint("/ingredients"),
      recipe_ingredients: {
        ...endpoint("/recipe_ingredients"),
        delete: (recipe_id, ingredient_id) => fetch(
          `${APIURL}/recipe_ingredients/${recipe_id}:${ingredient_id}`, {method: "DELETE"}
          ).then(r => r.json()),
      },
      mealplans: endpoint("/mealplans")
  }
  
})()

// DOM manipulation
let D = document
let $body = D.querySelector("body")
let $app = D.getElementById("app")

//components
const Input = (params, label) => {
  let inp = D.createElement("input")
  Object.entries(params).forEach(([key, val]) => inp.setAttribute(key, val))

  if (label) {
    var lab = D.createElement("label")
    lab.setAttribute("for", inp.id)
    lab.textContent = label
    return [lab, inp]
  }

  return [inp]
}

const Navbar = () => {
  const pages = [
    ["Recipes", render(RecipesPage)], 
    ["Add recipe", () => {
      let modal = D.getElementById("add-recipe-modal")
      let overlay = D.querySelector("#overlay")
      modal.classList.add("active")
      overlay.classList.add("active")
    }], 
    ["Mealplan", render(MealplanPage)],
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
  card.onclick = () => {
    state.selected_recipe = id
    render(RecipePage)()
  }

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

  let statedropdown = D.createElement("select")
  statedropdown.append(
    ...["open", "bought", "done"].map(s => new Option(s, s, false, false))
  )
  statedropdown.value = mealplan.state

  card.append(header, recipedropdown, statedropdown)

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

const MealplanFilter = () => {
  let form = D.createElement("form")
  let [start_label, start] = Input({id: "start_date", type: "date"}, "Start date")
  let [end_label, end] = Input({id: "end_date", type: "date"}, "End date")
  
  let [done_label, donecheckbox] = Input({id: "done-chechbox", type: "checkbox"}, "Hide done")
  donecheckbox.checked = false

  //eventhandlers for changes
  const callback = () => {
    sd = start.value || "0000-00-00"
    ed = end.value || "9999-99-99"

    let show_done = !donecheckbox.checked

    let show_data = state.mealplans
      .filter(mp => ((sd <= mp.date) && (mp.date <= ed)))
      .filter(mp => show_done || mp.state !== "done")

    let container = D.querySelector(".mealplan-container")
    container.replaceWith(Mealplan(show_data))
  }

  start.onchange = callback
  end.onchange = callback
  donecheckbox.onchange = callback

  form.append(
    start_label,
    start,
    end_label,
    end,
    done_label,
    donecheckbox,
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
  form = CreateMealpanForm()
  let [modal, overlay, closefunc] = ModalOverlay("create-mealplans-modal", "Create Mealplans", form)
  
  form.addEventListener("submit", closefunc)
  
  return [modal, overlay]
}

const ModalOverlay = (id, title, content) => {
  let overlay = D.createElement("div")
  overlay.id = "overlay"

  let modal = D.createElement("div")
  modal.className = "modal"
  modal.id = id

  const closefunc = () => {
    modal.classList.remove("active")
    overlay.classList.remove("active")
  }

  let header = D.createElement("div")
  header.className = "modal-header"
  
  let headertext = D.createElement("div")
  headertext.className = "title"
  headertext.textContent = title

  let closebutton = D.createElement("button")
  closebutton.className = "closebutton"
  closebutton.textContent = "\u00D7" //multiplication symbol
  closebutton.onclick = closefunc

  header.append(headertext, closebutton)
  
  let body = D.createElement("div")
  body.className = "modal-body"

  body.append(content)

  modal.append(header, body)

  return [modal, overlay, closefunc]
}

const AddRecipe = () => {
  form = AddRecipeForm()
  let [modal, overlay, closefunc] = ModalOverlay("add-recipe-modal", "Add Recipe", form)
  form.addEventListener("submit", closefunc)

  return [modal, overlay]
}

const TableRow = (data, header) => {
  tag = header ? "th" : "td"

  let row = D.createElement("tr")

  let cells = data.map(x => {
    let cell = D.createElement(tag)
    cell.append(...x)
    return cell
  })

  row.append(...cells)
  return row
}

const AddRecipeForm = () => {
  let form = D.createElement("form")

  let name = Input({id: "name"}, "Recipe name")
  let servings = Input({type: "number", id: "servings"}, "Servings")
  let tags = Input({id: "tags"}, "Tags")

  let method = D.createElement("textarea")
  method.id = "method"

  let methodlabel = D.createElement("label")
  methodlabel.setAttribute("for", method.id)
  methodlabel.textContent = "Method"

  let table = D.createElement("table")
  let tablehead = D.createElement("thead")
  let colnames = ["Ingredient", "Quantity", "Measure", "Optional"]
  let headrow = TableRow(colnames, true)
  tablehead.append(headrow)
  table.append(tablehead)

  let tablebody = D.createElement("tbody")
  table.append(tablebody)

  const addRow = (i) => {
    let ingredient = Input({id: "ingredient_" + i, list: "ingredientlist", autocomplete: "off"})
    let quantity = Input({id: "quantity_" + i, type: "number", step: "0.01"})
    let measure = Input({id: "measure_" + i, placeholder: "e.g dl"})
    let optional = Input({id: "optional_" + i, type: "checkbox"})

    let row = TableRow([ingredient, quantity, measure, optional])

    tablebody.append(row)
  }

  addRow(0)

  let addrowbutton = D.createElement("button")
  addrowbutton.setAttribute("type", "button")
  addrowbutton.textContent = "Add row"
  addrowbutton.onclick = () => addRow(tablebody.children.length)

  let savebutton = D.createElement("button")
  savebutton.textContent = "Save"

  form.onsubmit = async (ev) => {
    ev.preventDefault()
    ev.stopImmediatePropagation()

    //prepare recipe
    const recipe_data = {
      name: name[1].value,
      servings: servings[1].value,
      tags: tags[1].value,
      method: method.value,
    }

    //prepare ingredients
    let rows = [...tablebody.children]
    let recipeingredients = rows.map(row => {
      [ingredient, quantity, measure, optional] = row.querySelectorAll("input")
      
      return {
        ingredient: ingredient.value,
        quantity: quantity.value,
        measure: measure.value,
        optional: optional.checked
      }
    })

    //alert if recipe already exists
    if (state.recipes.find(r => r.name === recipe_data.name)) alert(`Recipe with name "${recipe_data.name}" already exists`)

    //missing ingredients
    const missing = recipeingredients.filter(ri => !state.ingredients.map(i => i.name).includes(ri.ingredient)).map(x => ({name: x.ingredient}))
    
    
    //create recipe and missing ingredients
    const [recipe, _] = await Promise.all([
      api.recipes.post(recipe_data),
      Promise.all(missing.map(api.ingredients.post)).then(res => state.ingredients = state.ingredients.concat(...res))
    ])

    //create recipe ingredients
    const ri_data = recipeingredients.map(ri => {
      return {
        recipe_id: recipe.id,
        ingredient_id: state.ingredients.find(i => i.name === ri.ingredient).id,
        quantity: ri.quantity,
        measure: ri.measure,
        optional: ri.optional
      }
    })

    ri_data.forEach(ri => api.recipes.ingredients.add(ri.recipe_id, ri))

    //reset the form
    form.reset()
    tablebody.innerHTML = ""
    addRow(0)

    //update state and re-render grid
    state.recipes = state.recipes.concat(recipe)
    let container = D.querySelector(".recipe-grid")
    container.replaceWith(RecipeGrid(state.recipes))
  }

  form.append(
    ...name,
    ...servings,
    ...tags,
    methodlabel,
    method,
    table,
    addrowbutton,
    savebutton
  )
  
  return form
}

const ShoppingList = () => {
  let [modal, overlay, closefunc] = ModalOverlay("shoppinglist-modal", "Shopping list", "content")
  return [modal, overlay]
}

const MealplansToShoppinglist = (mealplans) => {
  let list = mealplans.map(meal => {
    let li = document.createElement("li")
    let recipe = state.recipes.find(r => r.id === meal.recipe_id)
    if (!recipe) return

    let ingredients = state.recipe_ingredients.filter(i => i.recipe_id === recipe.id)

    const scale = meal.servings / recipe.servings
    const scaled_ingredients = ingredients.map(ing => ({
      ...ing, quantity: ing.quantity * scale
    }))

    li.textContent = `${recipe.name} (${meal.name} ${meal.date}, ${meal.servings} servings)`
    
    let ul = document.createElement("ul")

    scaled_ingredients.forEach(ing => {
      let li = document.createElement("li")
      let text = `${ing.ingredient.name} ${ing.quantity}${ing.measure}`
      if (ing.optional) {text = `(${text})`}
      li.textContent = text
      ul.appendChild(li)
    })

    li.appendChild(ul)
    return li
  })

  return list
}

const IngredientList = (ingredients) => {
  let sidebar = D.createElement("div")
  sidebar.className = "sidebar"

  let p = D.createElement("h3")
  p.textContent = "Ingredients"

  let ul = D.createElement("ul")

  ingredients.forEach(i => {
    let li = D.createElement("li")
    let text = `${i.ingredient.name} ${i.quantity}${i.measure}`
    if (i.optional) {
      text = "(" + text + ")"
    }
    li.textContent = text
    ul.appendChild(li)
  })

  sidebar.append(
    p,
    ul
  )

  return sidebar
} 

const RecipeView = (recipe) => {
  let container = D.createElement("div")
  container.className = "recipe-container"

  let header = D.createElement("div")
  header.className = "recipe-header"
  header.textContent = `${recipe.name} (${recipe.servings} servings)`

  let deletebutton = D.createElement("button")
  deletebutton.className = "delete-button"
  deletebutton.textContent = "DELETE"

  let deletedialog = D.createElement("dialog")

  let dialogtitle = D.createElement("div")
  dialogtitle.textContent = `Are you sure?\nType in ${recipe.name} to delete it`

  let deleteform = D.createElement("form")
  deleteform.method = "dialog"

  let [confirmdelete, _] = Input({id: "confirm-delete"})

  let okbutton = D.createElement("button")
  okbutton.setAttribute("type", "submit")
  okbutton.setAttribute("value", "")
  okbutton.textContent = "Delete"
  okbutton.disabled = true
  
  let cancelbutton = D.createElement("button")
  cancelbutton.textContent = "Cancel"
  cancelbutton.setAttribute("value", "cancel")

  
  deletedialog.onclose = () => {
    console.log(deletedialog.returnValue)
  }
  
  deleteform.append(confirmdelete, okbutton, cancelbutton)
  
  confirmdelete.oninput = (ev) => {
    okbutton.value = ev.target.value
    let disabled = ev.target.value === recipe.name ? false : true
    okbutton.disabled = disabled
  }

  deletedialog.append(
    dialogtitle,
    deleteform,
    )

  deletedialog.onclose = () => {
    if (!(deletedialog.returnValue === recipe.name)) return


    let ris = state.recipe_ingredients.filter(ri => ri.recipe_id === recipe.id)  

    Promise.all(ris.map(ri => api.recipe_ingredients.delete(ri.recipe_id, ri.ingredient_id)))
      .then(() => api.recipes.delete(recipe.id))
      .then(() => {
        state.recipe_ingredients = state.recipe_ingredients.filter(ri => ri.recipe_id !== recipe.id)
        state.recipes = state.recipes.filter(r => r.id !== recipe.id)
      })
      .then(render(RecipesPage))    
  }
  
  deletebutton.onclick = () => deletedialog.showModal()
  header.append(deletebutton, deletedialog)

  if (recipe.tags) {
    let taggrid = TagGrid(recipe.tags.split(","))
    header.appendChild(taggrid)
  }

  
  let method = D.createElement("div")
  method.className = "recipe-method"
  
  let ul = D.createElement("ul")
  recipe.method.split("\n").forEach(line => {
    let li = D.createElement("li")
    li.textContent = line
    ul.appendChild(li)
  }
  )

  method.appendChild(ul)

  container.append(
    header,
    method
  )

  return container
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
    RecipeGrid(state.recipes),
    ...AddRecipe()
  ]
}

const RecipePage = () => {
  let recipe = state.recipes.find(r => r.id === state.selected_recipe)
  let ingredients = state.recipe_ingredients.filter(i => i.recipe_id === state.selected_recipe)

  return [
    IngredientList(ingredients),
    RecipeView(recipe),
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
      let mp_state = card.getElementsByTagName("select").item(1).value
      
      const plan = state.mealplans.find(mp => mp.id === plan_id)
      const newPlan = {
        ...plan,
        recipe_id,
        state: mp_state
      }
      
      //this isn't very efficient put shall do for now
      api.mealplans.put(plan_id, newPlan)
        .then(data => state.mealplans = state.mealplans.map(mp => mp.id === data.id ? data : mp))
    })
  }

  //modal stuff
  [mealplan_modal, mealplan_overlay] = CreateMealplans()

  let createbutton = D.createElement("button")
  createbutton.textContent = "Create!"
  createbutton.onclick = () => {
    mealplan_modal.classList.add("active")
    mealplan_overlay.classList.add("active")
  }

  [shoppinglist_modal, shoppinglist_overlay] = ShoppingList()

  let shoppinglistbutton = D.createElement("button")
  shoppinglistbutton.textContent = "Shopping list"
  shoppinglistbutton.onclick = () => {
    let start = D.getElementById("start_date").value || "0000-00-00" 
    let end = D.getElementById("end_date").value || "9999-99-99"
  
    let show_data = state.mealplans
      .filter(mp => start <= mp.date && mp.date <= end && mp.recipe_id)
      .filter(mp => mp.state === "open")
    let body = shoppinglist_modal.querySelector(".modal-body")
    
    body.replaceChildren(...MealplansToShoppinglist(show_data))

    shoppinglist_modal.classList.add("active")
    shoppinglist_overlay.classList.add("active")
  }

  return [
    MealplanFilter(),
    createbutton,
    mealplan_modal, 
    mealplan_overlay,
    shoppinglistbutton,
    shoppinglist_modal,
    shoppinglist_overlay,
    Mealplan(state.mealplans),
    save,
  ]
}


//Event handlers


//Initial state
api.recipes.get()
  .then(data => state.recipes = data)
  .then(render(RecipesPage))

api.ingredients.get()
  .then(data => state.ingredients = data)

api.recipe_ingredients.get()
  .then(data => state.recipe_ingredients = data)

api.mealplans.get()
  .then(data => state.mealplans = data.sort((a,b) => b.date > a.date ? -1 : 1))
