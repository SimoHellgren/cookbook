
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
let api = (function () {

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
      delete: id => fetch(APIURL + path + "/" + id, { method: "DELETE" })
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
      put: (recipe_id, ingredient_id, data) => fetch(
        `${APIURL}/recipe_ingredients/${recipe_id}:${ingredient_id}`,
        {
          method: "PUT",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }
      ).then(r => r.json()),
      delete: (recipe_id, ingredient_id) => fetch(
        `${APIURL}/recipe_ingredients/${recipe_id}:${ingredient_id}`, { method: "DELETE" }
      ).then(r => r.json()),
      put_many: (data) => fetch(
        `${APIURL}/recipe_ingredients/bulk`,
        {
          method: "PUT",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        }
      ),
    },
    mealplans: endpoint("/mealplans"),
    comments: endpoint("/comments"),
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


const renderRecipeGrid = () => {
  let $grid = D.querySelector(".recipe-grid")
  let tags = [...D.querySelectorAll(".tag.selected")].map(t => t.textContent)
  let search = D.getElementById("recipesearch")

  let data = state.recipes
    .filter(r => {
      // all selected tags must be found on recipe
      for (tag of tags) {
        if (!r.tags.split(",").includes(tag)) return false
      }
      return true
    })
    .filter(r => r.name.toLowerCase().includes(search.value.toLowerCase()))

  $grid.replaceWith(RecipeGrid(data))
}


const TagGrid = (tags) => {
  let taggrid = D.createElement("div")
  taggrid.className = "tag-grid"

  let elements = tags
    .sort()
    .map(tag => {
      let elem = D.createElement("div")
      elem.className = "tag"
      elem.textContent = tag

      elem.onclick = (ev) => {
        ev.stopPropagation()
        // find the tag in then sidebar and select that
        let tags = [...D.querySelectorAll(".sidebar .tag")]
        let target = tags.filter(t => t.textContent === tag)[0]
        target.classList.toggle("selected")
        renderRecipeGrid();
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
  input.id = "recipesearch"
  input.placeholder = "Search by name"

  let submit = D.createElement("input")
  submit.setAttribute("type", "submit")
  submit.setAttribute("hidden", "")

  form.append(input, submit)

  form.onsubmit = (ev) => {
    ev.preventDefault()
    renderRecipeGrid()
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

  let namediv = D.createElement("div")

  let [name] = Input({})
  name.className = "mealcard-mealname"
  name.value = mealplan.name

  let [servings] = Input({})
  servings.className = "mealcard-servingscount"
  servings.value = mealplan.servings

  namediv.append(mealplan.date, name, servings)

  let deletebutton = D.createElement("button")
  deletebutton.setAttribute("type", "button")
  deletebutton.textContent = "DELETE"

  let deletedialog = D.createElement("dialog")
  let deleteform = D.createElement("form")
  deleteform.method = "dialog"

  let confirm = D.createElement("button")
  confirm.setAttribute("type", "submit")
  confirm.setAttribute("value", "delete")
  confirm.textContent = "Delete"

  let cancel = D.createElement("button")
  cancel.setAttribute("value", "cancel")
  cancel.textContent = "Cancel"

  deleteform.append(
    `Do you really wish to delete ${mealplan.date} ${mealplan.name}?`,
    confirm,
    cancel,
  )

  deletedialog.append(deleteform)

  deletebutton.onclick = () => deletedialog.showModal()

  deletedialog.onclose = () => {
    if (deletedialog.returnValue === "delete") {
      api.mealplans.delete(mealplan.id)
    }
  }

  header.append(namediv, deletebutton)

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

  return [card, deletedialog]
}

const MealCardRow = (mealplans) => {
  let div = D.createElement("div")
  div.className = "mealcard-row"

  const date = mealplans[0].date
  const weekday = new Date(Date.parse(date)).toLocaleString('en-Us', { weekday: "long" })

  div.append(`${date} (${weekday})`)


  mealplans
    .sort((a, b) => a.position - b.position)
    .forEach(mp => {
      let [card, dialog] = MealCard(mp)
      div.append(card, dialog)
    })

  return div
}


const Mealplan = (mealplans) => {
  let container = D.createElement("div")
  container.className = "mealplan-container"

  // group mealplans by date
  m = new Map()
  mealplans.forEach(mp => {
    if (!m.has(mp.date)) {
      m.set(mp.date, [])
    }

    m.set(mp.date, [...m.get(mp.date), mp])
  })

  let rows = [...m].sort().map(([_, mps]) => MealCardRow(mps))

  container.append(
    ...rows
  )

  return container
}

const MealplanFilter = () => {
  let form = D.createElement("form")
  let [start_label, start] = Input({ id: "start_date", type: "date" }, "Start date")
  let [end_label, end] = Input({ id: "end_date", type: "date" }, "End date")

  let [done_label, donecheckbox] = Input({ id: "done-chechbox", type: "checkbox" }, "Hide done")
  donecheckbox.checked = true

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
  let [start_label, start] = Input({ id: "start_date", type: "date" }, "Start date")
  let [end_label, end] = Input({ id: "end_date", type: "date" }, "End date")

  //set end date to start by default
  start.addEventListener("change", () => {
    if (!end.value) end.value = start.value
  }, { once: true })

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

    let dates = daterange(sd, ed).map(d => d.toISOString().slice(0, 10))

    let plans = dates.map(date => meals.map(([name, servings], position) => (
      {
        date,
        name,
        servings,
        position: position + 1 + state.mealplans.filter(mp => mp.date === date).length,
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

const TableRow = (data, header) => {
  tag = header ? "th" : "td"

  let row = D.createElement("tr")

  let cells = data.map(x => {
    let cell = D.createElement(tag)
    cell.append(x)
    return cell
  })

  row.append(...cells)
  return row
}

const RecipeForm = () => {
  let form = D.createElement("form")

  let name = Input({ id: "name" }, "Recipe name")
  let servings = Input({ type: "number", id: "servings" }, "Servings")
  let tags = Input({ id: "tags" }, "Tags")
  let source = Input({ id: "source" }, "Source")

  let method = D.createElement("textarea")
  method.id = "method"

  let methodlabel = D.createElement("label")
  methodlabel.setAttribute("for", method.id)
  methodlabel.textContent = "Method"

  let table = D.createElement("table")
  let tablehead = D.createElement("thead")
  let colnames = ["", "Ingredient", "Quantity", "Measure", "Optional"]
  let headrow = TableRow(colnames, true)
  tablehead.append(headrow)
  table.append(tablehead)

  let tablebody = D.createElement("tbody")
  table.append(tablebody)

  const addRow = (i) => {
    let delbutton = D.createElement("button")
    delbutton.textContent = "\u00D7"
    delbutton.setAttribute("type", "button")

    let [ingredient] = Input({ id: "ingredient_" + i, list: "ingredientlist", autocomplete: "off" })
    let [quantity] = Input({ id: "quantity_" + i, type: "number", step: "any" })
    let [measure] = Input({ id: "measure_" + i, placeholder: "e.g dl" })
    let [optional] = Input({ id: "optional_" + i, type: "checkbox" })

    let up = D.createElement("button")
    up.textContent = "上" || "\u2191"
    up.setAttribute("type", "button")

    let down = D.createElement("button")
    down.textContent = "下" || "\u2193"
    down.setAttribute("type", "button")

    let row = TableRow([delbutton, ingredient, quantity, measure, optional, up, down])
    row.id = i

    up.onclick = () => {
      tablebody.insertBefore(row, row.previousSibling)
    }

    down.onclick = () => {
      tablebody.insertBefore(row.nextSibling, row)
    }

    delbutton.onclick = () => row.remove()

    tablebody.append(row)
  }

  addRow(0)

  let addrowbutton = D.createElement("button")
  addrowbutton.id = "add-row-button"
  addrowbutton.setAttribute("type", "button")
  addrowbutton.textContent = "Add row"
  addrowbutton.onclick = () => addRow(Number(tablebody.lastChild.id) + 1)

  let savebutton = D.createElement("button")
  savebutton.textContent = "Save"

  let datalist = D.createElement("datalist")
  datalist.id = "ingredientlist"

  form.append(
    ...name,
    ...servings,
    ...tags,
    ...source,
    methodlabel,
    method,
    table,
    addrowbutton,
    savebutton,
    datalist,
  )

  return form
}

const ParseFormData = (form) => {
  // gets the recipe, ingredients and recipe ingredients from a form
  const name = form.querySelector("#name").value
  const servings = form.querySelector("#servings").value
  const tags = form.querySelector("#tags").value
  const source = form.querySelector("#source").value
  const method = form.querySelector("#method").value
  const rows = [...form.querySelector("tbody").children]

  const recipe = {
    name,
    servings,
    tags,
    source,
    method,
  }

  const recipeingredients = rows.map((row, i) => {
    let [ingredient, quantity, measure, optional] = row.querySelectorAll("input")

    return {
      ingredient: ingredient.value,
      quantity: quantity.value,
      measure: measure.value,
      optional: optional.checked,
      position: i + 1, // +1 to index from 1
    }
  })

  const ingredients = recipeingredients.map(ri => ({ name: ri.ingredient }))

  return {
    recipe,
    ingredients,
    recipeingredients,
  }
}

const AddRecipe = () => {
  form = RecipeForm()

  let [modal, overlay, closefunc] = ModalOverlay("add-recipe-modal", "Add Recipe", form)

  form.onsubmit = async (ev) => {
    ev.preventDefault()
    ev.stopImmediatePropagation()

    const { recipe: recipe_data, ingredients, recipeingredients } = ParseFormData(form)

    //alert if recipe already exists
    if (state.recipes.find(r => r.name === recipe_data.name)) alert(`Recipe with name "${recipe_data.name}" already exists`)

    //missing ingredients
    const missing = ingredients.filter(a => !state.ingredients.map(b => b.name).includes(a.name))

    //create recipe and missing ingredients
    const [recipe, _] = await Promise.all([
      api.recipes.post(recipe_data),
      Promise.all(missing.map(api.ingredients.post)).then(res => state.ingredients = state.ingredients.concat(...res))
    ])

    //create recipe ingredients
    const ri_data = recipeingredients.map(ri => {
      const { ingredient: name, ...rest } = ri
      return {
        recipe_id: recipe.id,
        ingredient_id: state.ingredients.find(i => i.name === name).id,
        ...rest,
      }
    })

    ri_data.forEach(ri => api.recipes.ingredients.add(ri.recipe_id, ri))

    //reset the form
    form.reset()
    form.querySelector("tbody").innerHTML = ""

    //update state and re-render grid
    state.recipes = state.recipes.concat(recipe)
    let container = D.querySelector(".recipe-grid")
    container.replaceWith(RecipeGrid(state.recipes))
  }
  form.addEventListener("submit", closefunc)

  return [modal, overlay]
}

const EditRecipe = (recipe) => {
  let form = RecipeForm()

  let name = form.querySelector("#name")
  let servings = form.querySelector("#servings")
  let tags = form.querySelector("#tags")
  let source = form.querySelector("#source")
  let method = form.querySelector("#method")

  let addrowbutton = form.querySelector("#add-row-button")

  name.value = recipe.name
  servings.value = recipe.servings
  tags.value = recipe.tags
  method.value = recipe.method
  source.value = recipe.source

  let state_ingredients = state.recipe_ingredients.filter(ri => ri.recipe_id == recipe.id)

  //add ingredient rows - not pretty but shall do
  state_ingredients.slice(1).forEach(ri => addrowbutton.dispatchEvent(new Event("click")))

  let tablerows = [...form.querySelector("tbody").children]

  state_ingredients.map((ing, i) => {
    let [name, quantity, measure, optional] = tablerows[i].querySelectorAll("input")
    name.value = ing.ingredient.name
    quantity.value = ing.quantity
    measure.value = ing.measure
    optional.checked = ing.optional
  })

  form.onsubmit = async (ev) => {
    ev.preventDefault()
    ev.stopImmediatePropagation()

    const { recipe: recipe_data, ingredients, recipeingredients } = ParseFormData(form)

    //PUT recipe
    api.recipes.put(recipe.id, { id: recipe.id, ...recipe_data })

    //missing ingredients
    const missing = ingredients.filter(a => !state.ingredients.map(b => b.name).includes(a.name))

    //split RIs to existing (PUT), new (POST) and deleted (DELETE)
    let current_ing_names = state_ingredients.map(i => i.ingredient.name)
    let put_ris = recipeingredients.filter(ri => current_ing_names.includes(ri.ingredient))
    let post_ris = recipeingredients.filter(ri => !current_ing_names.includes(ri.ingredient))
    let delete_ris = state_ingredients.filter(ri =>
      !recipeingredients.map(i => i.ingredient).includes(ri.ingredient.name)
    )

    //PUT existing RIs
    api.recipe_ingredients.put_many(
      put_ris
        .map(ri => ({
          recipe_id: recipe.id,
          ingredient_id: state.ingredients.find(i => i.name === ri.ingredient).id,
          quantity: ri.quantity,
          measure: ri.measure,
          optional: ri.optional,
          position: ri.position,
        }))
    )
    //create missing ingredients, then POST new RIs
    Promise.all(missing.map(api.ingredients.post))
      .then(data => state.ingredients = state.ingredients.concat(data))
      .then(() =>
        // delete disappeared recipe ingredients
        // done before posting to avoid conflicts with position
        delete_ris.forEach(ri => {
          let ingredient_id = state.ingredients.find(i => i.name === ri.ingredient.name).id
          api.recipe_ingredients.delete(recipe.id, ingredient_id)
            .then(data => state.recipe_ingredients = state.recipe_ingredients.filter(
              i => (i.recipe_id !== data.recipe_id && i.ingredient_id !== data.ingredient_id)))
        })
      )
      .then(() =>
        post_ris.map(ri => ({
          recipe_id: recipe.id,
          ingredient_id: state.ingredients.find(i => i.name === ri.ingredient).id,
          quantity: ri.quantity,
          measure: ri.measure,
          optional: ri.optional,
          position: ri.position,
        })).forEach(ri => api.recipes.ingredients.add(recipe.id, ri))
      )
  }

  let [modal, overlay, closefunc] = ModalOverlay("edit-recipe-modal", "Edit Recipe: " + recipe.name, form)

  return [modal, overlay]

}

const ShoppingList = () => {
  let [modal, overlay, closefunc] = ModalOverlay("shoppinglist-modal", "Shopping list", "content")
  return [modal, overlay]
}

const MealplansToShoppinglist = (mealplans) => {
  let ingredientlist = mealplans
    .filter(mp => mp.recipe_id)
    .flatMap(meal => {
      const recipe = state.recipes.find(r => r.id === meal.recipe_id)
      const ingredients = state.recipe_ingredients.filter(ri => ri.recipe_id === recipe.id)
      const scale = meal.servings / recipe.servings

      const scaled_ingredients = ingredients.map(ing => ({
        ...ing,
        quantity: ing.quantity * scale
      }))

      return scaled_ingredients.map(ingredient => ({
        meal,
        recipe,
        ingredient,
      }))
    })

  let gb = new Map()
  ingredientlist.forEach(row => {
    let key = row.ingredient.ingredient.name + "_" + row.ingredient.measure

    if (!gb.has(key)) {
      gb.set(key, [])
    }

    gb.set(key, [...gb.get(key), row])
  })

  let entries = [...gb]
    .sort() // sort by keys (default behavior)
    .map(([key, items]) => {
      let [name, measure] = key.split("_")
      let total = items.reduce((r, e) => r + e.ingredient.quantity, 0)

      let details = D.createElement("details")
      let summary = D.createElement("summary")
      summary.textContent = `${name} - ${total} ${measure}`

      let detailrows = items.map(i => {
        let p = D.createElement("p")
        p.textContent = `${i.meal.date} ${i.meal.name}: ${i.recipe.name} \
        ${i.ingredient.quantity} ${i.ingredient.measure}`
        return p
      })

      details.append(
        summary,
        ...detailrows
      )
      return details
    })

  return entries

}

const IngredientList = (ingredients) => {
  let sidebar = D.createElement("div")
  sidebar.className = "sidebar"

  let p = D.createElement("h3")
  p.textContent = "Ingredients"

  let ul = D.createElement("ul")
  ul.className = "ingredientlist"

  ingredients.forEach(i => {
    let li = D.createElement("li")
    let text = `${i.ingredient.name} ${i.quantity}${i.measure}`
    if (i.optional) {
      text = "(" + text + ")"
    }

    let [label, checkbox] = Input({ type: "checkbox" }, text)
    checkbox.onclick = () => {
      label.classList.toggle("checked")
    }

    li.append(checkbox, label)
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

  let title = D.createElement("h1")
  title.textContent = recipe.name

  let scale_div = D.createElement("div")

  let [scale_label, scale_input] = Input({ type: "number", step: "any", value: recipe.servings }, "servings")
  scale_input.onchange = () => {
    let scaled_ingredients = state.recipe_ingredients
      .filter(i => i.recipe_id === recipe.id)
      .map(i => ({
        ...i,
        quantity: +(i.quantity * scale_input.value / recipe.servings).toFixed(2) // the + strips unnecessary decimal places
      }))

    let inglist = IngredientList(scaled_ingredients)

    D.querySelector(".sidebar").replaceWith(inglist)
  }

  scale_div.append(scale_input, scale_label)

  let source = D.createElement("div")
  source.append("Source: ")
  if (recipe.source && recipe.source.includes("http")) {
    let link = D.createElement("a")
    link.setAttribute("href", recipe.source)
    link.textContent = recipe.source
    link.onclick = (ev) => {
      ev.preventDefault()
      window.open(recipe.source)
    }
    source.append(link)
  } else {
    source.append(recipe.source)
  }


  header.append(title, scale_div, source)

  let [edit_modal, edit_overlay] = EditRecipe(recipe)

  let editbutton = D.createElement("button")
  editbutton.textContent = "EDIT"
  editbutton.onclick = () => {
    edit_modal.classList.add("active")
    edit_overlay.classList.add("active")
  }

  let deletebutton = D.createElement("button")
  deletebutton.className = "delete-button"
  deletebutton.textContent = "DELETE"

  let deletedialog = D.createElement("dialog")

  let dialogtitle = D.createElement("div")
  dialogtitle.textContent = `Are you sure?\nType in ${recipe.name} to delete it`

  let deleteform = D.createElement("form")
  deleteform.method = "dialog"

  let [confirmdelete, _] = Input({ id: "confirm-delete" })

  let okbutton = D.createElement("button")
  okbutton.setAttribute("type", "submit")
  okbutton.setAttribute("value", "")
  okbutton.textContent = "Delete"
  okbutton.disabled = true

  let cancelbutton = D.createElement("button")
  cancelbutton.textContent = "Cancel"
  cancelbutton.setAttribute("value", "cancel")

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
  header.append(editbutton, deletebutton, deletedialog)

  if (recipe.tags) {
    let taggrid = TagGrid(recipe.tags.split(","))
    header.appendChild(taggrid)
  }


  let method = D.createElement("div")
  method.className = "recipe-method"

  let ul = D.createElement("ul")
  if (recipe.method) {
    recipe.method.split("\n").forEach(line => {
      let li = D.createElement("li")

      let [label, checkbox] = Input({ type: "checkbox" }, line)
      checkbox.onclick = () => {
        label.classList.toggle("checked")
      }

      li.append(
        checkbox,
        label
      )
      ul.appendChild(li)
    }
    )
  }

  method.appendChild(ul)

  container.append(
    header,
    method,
    edit_modal,
    edit_overlay
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

const AddComentForm = (parent_id) => {
  let form = D.createElement("form")
  let [author_label, author] = Input({ type: "text" }, "Author")
  let comment = D.createElement("textarea")
  let [savebutton] = Input({ "type": "submit", "value": "Save comment" })
  savebutton.onclick = (ev) => {
    ev.preventDefault()
    api.comments.post({
      recipe_id: state.selected_recipe,
      comment: comment.value,
      parent_id: parent_id,
      author: author.value,
    }).then(data => { state.comments = state.comments.concat(data) })
  }

  form.append(author_label, author, comment, savebutton)
  return form
}

const EditCommentForm = (commentdata) => {
  let form = D.createElement("form")
  let [author_label, author] = Input({ type: "text" }, "Author")
  let comment = D.createElement("textarea")
  let [savebutton] = Input({ "type": "submit", "value": "Save comment" })

  author.value = commentdata.author
  comment.value = commentdata.comment

  savebutton.onclick = (ev) => {
    ev.preventDefault()
    api.comments.put(commentdata.id, {
      ...commentdata,
      comment: comment.value,
      author: author.value
    })
      .then(data => { state.comments = state.comments.concat(data) })
  }

  let [deletebutton] = Input({ "type": "button", "value": "DELETE" })
  deletebutton.className = "delete-button"
  deletebutton.onclick = () => {
    api.comments.delete(commentdata.id)
  }

  form.append(author_label, author, comment, savebutton, deletebutton)
  return form
}

const Comment = (comment) => {
  let container = D.createElement("div")
  container.className = "comment"

  let metadata = D.createElement("div")
  metadata.className = "comment-metadata"

  const created = new Date(Date.parse(comment.created))
  const updated = new Date(Date.parse(comment.updated))

  let metadata_text = `${comment.author}, ${created.toLocaleDateString('fi')} ${created.toLocaleTimeString('fi')} UTC`

  if (comment.created !== comment.updated) {
    metadata_text += ` (edited ${updated.toLocaleDateString('fi')} ${updated.toLocaleTimeString('fi')} UTC)`
  }

  metadata.textContent = metadata_text

  let commenttext = D.createElement("div")
  commenttext.className = "comment-text"
  commenttext.textContent = comment.comment

  let [editbutton] = Input({ "type": "button", "value": "Edit" })
  let [editmodal,] = ModalOverlay("edit-comment-modal", "Edit comment", EditCommentForm(comment))
  editbutton.onclick = () => {
    editmodal.classList.add("active")
  }

  let [replybutton] = Input({ "type": "button", "value": "Reply" })
  let msg_preview = comment.comment.split(" ").slice(0, 5).join(" ")
  let [replymodal,] = ModalOverlay("reply-comment-modal", `Reply to "${msg_preview}..."`, AddComentForm(comment.id))
  replybutton.onclick = () => {
    replymodal.classList.add("active")
  }

  container.append(commenttext, metadata, editbutton, editmodal, replymodal, replybutton)
  return container
}

const CommentSection = (comments) => {
  let container = D.createElement("div")
  container.className = "comments-container"

  let header = D.createElement("div")
  header.className = "comments-header"
  header.textContent = "Comments"

  let body = D.createElement("div")
  body.className = "comments-body"

  let footer = D.createElement("div")
  footer.className = "comments-footer"

  let [modal, overlay, closefunc] = ModalOverlay('create-comment-modal', "New comment", AddComentForm())
  let [createbutton] = Input({ 'type': 'button', 'value': 'New comment' })
  createbutton.onclick = () => modal.classList.add("active")

  footer.append(createbutton, modal)

  container.append(header, body, footer)

  // construct tree
  lookup = new Map()
  children = new Map([[0, []]]) // 0 as root

  comments.sort((a, b) => a.id - b.id).forEach(c => {
    lookup.set(c.id, c)

    children.set(c.id, [])

    let parent = c.parent_id || 0

    children.set(parent, children.get(parent).concat(c.id))

  })

  // gather comments depth first
  const walk = (node, parent) => {
    children.get(node).forEach(n => {
      let div = Comment(lookup.get(n))
      parent.append(div)

      walk(n, div)
    })
  }

  walk(0, body)

  return container
}

const RecipePage = () => {
  let recipe = state.recipes.find(r => r.id === state.selected_recipe)
  let ingredients = state.recipe_ingredients.filter(i => i.recipe_id === state.selected_recipe)
  let comments = state.comments.filter(i => i.recipe_id === state.selected_recipe)

  return [
    IngredientList(ingredients),
    RecipeView(recipe),
    CommentSection(comments),
  ]
}

const MealplanPage = () => {
  let save = D.createElement("button")
  save.textContent = "Save"

  save.onclick = () => {
    let container = D.querySelector(".mealplan-container")

    container.querySelectorAll(".mealcard").forEach(card => {
      let plan_id = parseInt(card.getAttribute("id"))
      let recipe_id = parseInt(card.getElementsByTagName("select").item(0).value)
      let mp_state = card.getElementsByTagName("select").item(1).value
      let name = card.querySelector(".mealcard-mealname").value
      let servings = parseInt(card.querySelector(".mealcard-servingscount").value)

      const plan = state.mealplans.find(mp => mp.id === plan_id)
      const newPlan = {
        ...plan,
        recipe_id,
        name,
        servings,
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
    Mealplan(state.mealplans.filter(mp => mp.state !== "done")),
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
  .then(() => {
    let datalist = D.getElementById("ingredientlist")
    datalist.append(
      ...state.ingredients
        .sort((a, b) => a.name >= b.name ? 1 : -1)
        .map(ing => new Option(ing.name))
    )
  })

api.recipe_ingredients.get()
  .then(data => state.recipe_ingredients = data.sort((a, b) => a.recipe_id - b.recipe_id || a.position - b.position))

api.mealplans.get()
  .then(data => state.mealplans = data.sort((a, b) => b.date > a.date ? -1 : 1))

api.comments.get()
  .then(data => state.comments = data)
