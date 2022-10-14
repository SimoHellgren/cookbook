<script>
  import api from '$lib/api'
  import recipes from '$lib/stores/recipes';
  import ingredients from '$lib/stores/ingredients';
  import RecipeForm from '$lib/components/RecipeForm.svelte';
  export let data;

  let current_ingredients = data.ingredients;

  const onSubmit = async () => {
    //put recipe
    recipes.edit(data.recipe.id, data.recipe);

    //remove deleted ingredients
    const deleted = current_ingredients
      .filter((a) => !data.ingredients.map((b) => b.name).includes(a.name))
      .map((ri) => $ingredients.find((i) => i.name === ri.name));
    await Promise.all(
      deleted.map((i) => {
        api.recipe_ingredients.remove(data.recipe.id, i.id);
      }),
    );

    //add new ingredients
    const missing = data.ingredients.filter((ri) => !$ingredients.find((i) => i.name === ri.name));
    await Promise.all(missing.map(ingredients.add));

    //new recipe_ingredients get POSTed
    data.ingredients
      .filter((ri) => !current_ingredients.find((ci) => ci.name === ri.name))
      .map(({ name, ...ri }) => {
        const obj = {
          ...ri,
          recipe_id: data.recipe.id,
          ingredient_id: $ingredients.find((i) => i.name === name).id,
        };

        api.recipes.ingredients.add(data.recipe.id, obj)
      });

    //put rest
    const rest = data.ingredients.filter((ri) => !missing.map((m) => m.name).includes(ri.name));
    api.recipe_ingredients.update_many(
      rest.map(({ name, ...ri }) => {
        return {
          ...ri,
          recipe_id: data.recipe.id,
          ingredient_id: $ingredients.find((i) => i.name === name).id,
      }})
    )
  }
</script>

<h1>Edit {data.recipe.name}</h1>

<RecipeForm
  bind:name={data.recipe.name}
  bind:servings={data.recipe.servings}
  bind:tags={data.recipe.tags}
  bind:source={data.recipe.source}
  bind:method={data.recipe.method}
  bind:ingredients={data.ingredients}
  submitForm={onSubmit}
/>
