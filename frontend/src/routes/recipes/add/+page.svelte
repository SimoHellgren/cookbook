<script>
  import recipes from '$lib/stores/recipes';
  import ingredients from '$lib/stores/ingredients';
  import RecipeForm from '$lib/components/RecipeForm.svelte';
  let name;
  let servings;
  let tags = '';
  let source;
  let method;
  let recipe_ingredients = [];

  const submitForm = async () => {
    // create recipe and update state
    const recipe = await recipes.create({
      name,
      servings,
      method,
      tags,
      source,
    });

    // create missing ingredients and update state
    await Promise.all(
      recipe_ingredients
        .filter((ri) => !$ingredients.find((i) => i.name == ri.name))
        .map(ingredients.add),
    );

    // connect ingredients with recipe
    recipe_ingredients.forEach((ri) => {
      const data = {
        recipe_id: recipe.id,
        ingredient_id: $ingredients.find((i) => i.name === ri.name).id,
        quantity: ri.quantity,
        measure: ri.measure,
        optional: ri.optional,
        position: ri.position,
      };

      fetch(`http://127.0.0.1:8000/recipes/${recipe.id}/ingredients`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
    });
  };
</script>

<h1>Add recipe</h1>
<RecipeForm
  bind:name
  bind:servings
  bind:tags
  bind:source
  bind:method
  bind:ingredients={recipe_ingredients}
  {submitForm}
/>

<style>
</style>
