<script>
    import MealCard from "./MealCard.svelte";
    export let data;

</script>

<h1>Mealplans</h1>

    {#each data.mealplans as mealplan}
        <MealCard {...mealplan} recipe={data.recipes.find(r => r.id === mealplan.recipe_id) || {}}/>
    {/each}
