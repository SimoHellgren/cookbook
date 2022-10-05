<script>
    import RecipeCard from './RecipeCard.svelte'
    export let data;
</script>


<h1>Recipes</h1>

<div class="recipecard-grid">
    {#each data.recipes as recipe}
        <RecipeCard {...recipe}/>
    {/each}
    
</div>

<style>
    .recipecard-grid {
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))
    }
</style>