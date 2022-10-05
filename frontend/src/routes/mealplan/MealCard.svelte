<script>
    import { recipes } from "../../stores";
    export let date
    export let meals

</script>


<div class="container">
    <header>
        {date}, {new Date(date).toLocaleDateString("en", {weekday: "long"})}
    </header>
    {#each meals as meal}
        <div class="meal">
            <div>
                {meal.name} ({meal.servings})
            </div>
            <div>
                <select value={meal.state}>
                    <option>open</option>
                    <option>bought</option>
                    <option>done</option>
                </select>
                <select value={meal.recipe_id}>
                    {#each $recipes as recipe}
                        <option value={recipe.id}>{recipe.name}</option>
                    {/each}
                </select>
            </div>
        </div>
    {/each}
</div>

<style>
    .container {
        background-color: #f4f4f4;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        margin: 1rem;
        padding: 0.5rem;
        width: fit-content;
    }

    .meal {
        display: flex;
    }
</style>