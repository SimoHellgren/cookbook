<script>
    import RecipeCard from './RecipeCard.svelte'
    export let data;

    $: alltags = [...new Set(data.recipes.map(r => r.tags.split(",")).flat())]

</script>


<h1>Recipes</h1>

<div class="container">
    <div class="sidebar">
        <input placeholder="Search by name">
        {#each alltags as tag}
            <div>{tag}</div>
        {/each}

    </div>

    <div class="recipecard-grid">
        {#each data.recipes as recipe}
            <RecipeCard {...recipe}/>
        {/each}
        
    </div>
</div>

<style>
    .container {
        display: grid;
        grid-auto-columns: minmax(0, 1fr);
    }

    .sidebar {
        grid-column: 1;
    }

    .recipecard-grid {
        grid-column: 2/6;
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))
    }
</style>