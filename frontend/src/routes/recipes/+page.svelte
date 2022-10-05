<script>
    import RecipeCard from './RecipeCard.svelte'
    export let data;

    $: alltags = [...new Set(data.recipes.map(r => r.tags.split(",")).flat())]

    let search = "";
    $: showrecipes = data.recipes.filter(r => r.name.toLowerCase().includes(search.toLowerCase()))

</script>


<h1>Recipes</h1>

<div class="container">
    <div class="sidebar">
        <input placeholder="Search by name" bind:value={search}>
        {#each alltags as tag}
            <div>{tag}</div>
        {/each}

    </div>

    <div class="recipecard-grid">
        {#each showrecipes as recipe}
            <RecipeCard {...recipe}/>
        {/each}
        
    </div>
</div>

<style>
    .container {
        display: flex;
        gap: 1rem;
    }

    .recipecard-grid {
        flex: 1;
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))
    }
</style>