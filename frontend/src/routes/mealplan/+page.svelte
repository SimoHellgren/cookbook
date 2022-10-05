<script>
    export let data;
</script>

<h1>Mealplans</h1>
<ul>
    {#each data.mealplans as mealplan}
        <li>{mealplan.date} {mealplan.name}</li>
    {/each}
</ul>