<script>
    import { recipes, ingredients } from '../../../stores.js' 
    import RecipeForm from '$lib/components/RecipeForm.svelte'
    let name;
    let servings;
    let tags = "";
    let source;
    let method;

    const submitForm = async () => {
        // create recipe and update state
        const recipe = await fetch("http://127.0.0.1:8000/recipes", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(
                {
                    name,
                    servings,
                    method,
                    tags,
                    source,
                }
            )
        }).then(r => r.json())
        $recipes = [...$recipes, recipe]

        // create missing ingredients and update state
        const missing = recipe_ingredients.filter(ri => !$ingredients.find(i => i.name == ri.name))
        const new_ingredients = await Promise.all(
            missing.map(ri =>fetch("http://127.0.0.1:8000/ingredients", {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name: ri.name})
                }).then(r => r.json())
            )
        )
        $ingredients = $ingredients.concat(new_ingredients)

        // connect ingredients with recipe
        recipe_ingredients.forEach(ri => {
            const data = {
                recipe_id: recipe.id,
                ingredient_id: $ingredients.find(i => i.name === ri.name).id,
                quantity: ri.quantity,
                measure: ri.measure,
                optional: ri.optional,
                position: ri.position,
            }

            fetch(`http://127.0.0.1:8000/recipes/${recipe.id}/ingredients`, {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
        })
    }

</script>

<h1>Add recipe</h1>
<RecipeForm
    {name}
    {servings}
    {source}
    {method}
    {submitForm}
/>

<style>
</style>