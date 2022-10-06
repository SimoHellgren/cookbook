<script>
    let name;
    let servings;
    let tags;
    let source;
    let method;

    const ingredientTemplate = {name: null, quantity: null, measure: null, optional: false} 
    let ingredients = [{...ingredientTemplate, position: 1}]

    const addIngredient = () => {
        // add new ingredient row and update positions
        ingredients = [...ingredients, {...ingredientTemplate}].map((ing, i) => ({
            ...ing,
            position: i+1
        }))
    }

    const removeIngredient = (position) => {
        // remove ingredient with position and reset positions
        ingredients = ingredients
            .filter(ing => ing.position !== position)
            .map((ing, i) => ({...ing, position: i+1}))
    }
</script>

<h1>Add recipe</h1>

<form>
    <div class="container">
        <div class="recipe-metadata">
            <input bind:value={name} placeholder="Name">
            <input type="number" bind:value={servings} placeholder="Servings">
            <input bind:value={tags} placeholder="Tags">
            <input bind:value={source} placeholder="Source">
        </div>
        <div class="recipe-method">
            <textarea bind:value={method} placeholder="Method"/>
        </div>
        <div class="ingredients">
            <button on:click|preventDefault={addIngredient}>Add ingredient</button>
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>Ingredient</th>
                        <th>Quantity</th>
                        <th>Measure</th>
                        <th>Optional</th>
                    </tr>
                </thead>
                <tbody>
                    {#each ingredients as ing}
                        <tr>
                            <td><button type="button" on:click|preventDefault={() => removeIngredient(ing.position)}>&times;</button></td>
                            <td><input bind:value={ing.name}></td>
                            <td><input type="number" bind:value={ing.quantity}></td>
                            <td><input placeholder="e.g. dl" bind:value={ing.measure}></td>
                            <td><input type="checkbox" bind:checked={ing.optional}></td>
                        </tr>   
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
    <button type="submit">Save</button>
</form>

<style>
    .container {
        display: grid;
        gap: 1rem;
        grid-template-rows: repeat(auto-fit, 1fr);
        grid-template-columns: repeat(auto-fit, 1fr);
    }

    .recipe-metadata {
        display: flex;
        gap: 1rem;
        flex-direction: column;
        grid-column: 1/2;
    }

    .recipe-method {
        grid-column: 2/4;
    }

    .ingredients {
        grid-column: 1/6;
    }

    textarea {
        width: 100%;
        height: 100%;
    }

</style>