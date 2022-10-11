<script>
    import RecipeForm from '$lib/components/RecipeForm.svelte'
    export let data;

</script>

<h1>Edit {data.recipe.name}</h1>

<RecipeForm
    {...data.recipe}
    ingredients={data.ingredients}
/>