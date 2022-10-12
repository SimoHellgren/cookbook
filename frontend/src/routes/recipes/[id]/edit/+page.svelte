<script>
  import recipes from '$lib/stores/recipes';
  import ingredients from '$lib/stores/ingredients';
  import RecipeForm from '$lib/components/RecipeForm.svelte';
  import { append } from 'svelte/internal';
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
        fetch(`http://127.0.0.1:8000/recipe_ingredients/${data.recipe.id}:${i.id}`, {
          method: 'DELETE',
        });
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

        fetch(`http://127.0.0.1:8000/recipes/${data.recipe.id}/ingredients`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(obj),
        });
      });

    //put rest
    const rest = data.ingredients.filter((ri) => !missing.map((m) => m.name).includes(ri.name));
    rest.map(({ name, ...ri }) => {
      const obj = {
        ...ri,
        recipe_id: data.recipe.id,
        ingredient_id: $ingredients.find((i) => i.name === name).id,
      };

      fetch(`http://127.0.0.1:8000/recipe_ingredients/${obj.recipe_id}:${obj.ingredient_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(obj),
      });
    });
  };
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
