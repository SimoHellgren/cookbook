<script>
    import Checkable from "./Checkable.svelte";
    import Tag from "../Tag.svelte";
    export let data 

    const tags = data.recipe.tags.split(",").filter(t => t)
</script>

<div class="container">
    <div class="ingredients">
        <h3>Ingredients</h3>
        <ul>
            {#each data.ingredients as i}
                <li>
                    <Checkable>
                        {i.ingredient.name} {i.quantity}{i.measure}
                    </Checkable>

                </li>
            {/each}
        </ul>
    </div>
    <div class="recipe">
        <header>
            <h1>{data.recipe.name}</h1>
            <p>{data.recipe.servings} servings</p>
            <p>Source: {data.recipe.source}</p>
            <div class="tag-grid">
                {#each tags as tag}
                    <Tag name={tag}/>
                {/each}
            </div>
        </header>
        <div class="method">
            <ul>
                {#each data.recipe.method.split("\n").filter(t => t) as line}
                    <li>
                        <Checkable>{line}</Checkable>
                    </li>
                {/each}
            </ul>

        </div>
    </div>
</div>


<style>
    .container {
        margin-top: 1rem;
        display: flex;
        gap: 1rem;
    }

    .ingredients {
        background-color: #f4f4f4;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        flex: 1;
    }

    .ingredients h3 {
        text-align: center;
    }
    
    h1 {
        margin: 0;
    }

    .recipe {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 0;
    }

    .recipe header {
        background-color: #f4f4f4;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        padding: 1rem;
    }
    
    .method {
        background-color: #f4f4f4;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    }
    
    ul {
        margin-left: 0.1rem;
        padding: 0;
    }

    li {
        list-style: none;
    }

    .tag-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

</style>