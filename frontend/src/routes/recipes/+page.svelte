<script>
    import recipes from '$lib/stores/recipes'
    import RecipeCard from './RecipeCard.svelte'
    import Tag from './Tag.svelte'

    $: alltags = [...new Set($recipes.map(r => r.tags.split(",")).flat())].filter(t => t)

    let search = "";
    let selectedtags = [];
    $: showrecipes = $recipes
        .filter(r => r.name.toLowerCase().includes(search.toLowerCase()))
        .filter(r => {
            let ts = r.tags.split(",")
            for (const tag of selectedtags) {
                if (!ts.includes(tag)) return false
            }
            return true
        })


    const toggleTag = (tag) => {
        if (selectedtags.includes(tag)) {
            selectedtags = selectedtags.filter(t => t !== tag)
        } else {
            selectedtags = [...selectedtags, tag]
        }
    }


</script>


<h1>Recipes</h1>

<div class="container">
    <div class="sidebar">
        <input placeholder="Search by name" bind:value={search}>
        <div class="tag-grid">
            {#each alltags as tag}
                <Tag name={tag} on:click={() => toggleTag(tag)}/>
            {/each}
        </div>

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

    .sidebar {
        padding: 1rem;
        background-color: #f4f4f4;
        text-align: center;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        height: fit-content;
    }

    .tag-grid {
        margin-top: 1rem;
        display: grid;
        gap: 0.5rem;
        grid-template-columns: 1fr 1fr;
    }

</style>