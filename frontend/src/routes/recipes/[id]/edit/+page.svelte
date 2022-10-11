<script>
    import RecipeForm from '$lib/components/RecipeForm.svelte'
    export let data;

</script>

<h1>Edit {data.name}</h1>

<RecipeForm
    name={data.name}
/>