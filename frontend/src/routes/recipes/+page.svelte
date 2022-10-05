<script>
    import RecipeCard from './RecipeCard.svelte'
    let recipes = fetch("http://127.0.0.1:8000/recipes/").then(response => recipes = response.json())
</script>


<h1>Recipes</h1>

<div class="recipecard-grid">
    {#await recipes}
        <p>Fetching data</p>
    {:then recipes} 
        {#each recipes as recipe}
            <RecipeCard {...recipe}/>
        {/each}
    {/await}

</div>

<style>
    .recipecard-grid {
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))
    }
</style>