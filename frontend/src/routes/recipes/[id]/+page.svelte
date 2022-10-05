<script>
    export let data 
</script>

<h1>{data.recipe.name}</h1>
<p>{data.recipe.servings} servings</p>
<p>Source: {data.recipe.source}</p>
<p>{data.recipe.tags}</p>
<p>{data.recipe.method}</p>
<h2>Ingredients</h2>
<ul>
    {#each data.ingredients as i}
        <li>{i.ingredient.name} {i.quantity}{i.measure}</li>
    {/each}
</ul>