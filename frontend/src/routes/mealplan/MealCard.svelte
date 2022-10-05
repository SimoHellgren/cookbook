<script>
    export let date;
    export let name;
    export let servings;
    export let state;
    export let recipe;
</script>


<div class="container">
    {date} {name} ({servings}) {state} {recipe.name || ""}
</div>


<style>
    .container {
        background-color: #f4f4f4;
        box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
        margin: 1rem;
        padding: 0.5rem;
        width: fit-content;
    }
</style>