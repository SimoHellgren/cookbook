<script>
    import RecipeCard from './RecipeCard.svelte'
    let recipes = fetch("http://127.0.0.1:8000/recipes/").then(response => recipes = response.json())
</script>


<h1>Recipes</h1>
<ul>
    {#await recipes}
        <p>Fetching data</p>
    {:then recipes} 
        {#each recipes as recipe}
            <RecipeCard {...recipe}/>
        {/each}
    {/await}
</ul>