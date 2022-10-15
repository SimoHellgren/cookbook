<script>
  import api from '$lib/api'
  import recipes from '$lib/stores/recipes';
  export let date;
  export let meals;

  let node;

  const save = () => meals.forEach((meal) => api.mealplans.update(meal.id, meal))

  const remove = (meal) => {
    api.mealplans.remove(meal.id)
      .then(data => {
        meals = meals.filter((m) => m.id != meal.id);
    
        // remove container if no meals - could probably be done smoother through a store
        if (!meals.length) node.parentNode.removeChild(node);
      })
  };
</script>

<div class="container" bind:this={node}>
  <header>
    {date}, {new Date(date).toLocaleDateString('en', { weekday: 'long' })}
    <button on:click={save}>Save</button>
  </header>
  {#each meals.sort((a, b) => a.position - b.position) as meal}
    <div class="meal">
      <input bind:value={meal.name} />
      (<input bind:value={meal.servings} style="width: 1rem;" />)
      <div>
        <select bind:value={meal.state}>
          <option>open</option>
          <option>bought</option>
          <option>done</option>
        </select>
        <select bind:value={meal.recipe_id}>
          <option value={null} />
          {#each $recipes as recipe}
            <option value={recipe.id}>{recipe.name}</option>
          {/each}
        </select>
        <button on:click={() => remove(meal)}>&times;</button>
      </div>
    </div>
  {/each}
</div>

<style>
  .container {
    background-color: #f4f4f4;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    margin: 1rem;
    padding: 0.5rem;
    width: fit-content;
  }

  .meal {
    display: flex;
  }
</style>
