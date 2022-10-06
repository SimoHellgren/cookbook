<script>
    export let checked = false;
</script>


<label class:selected={checked}>
    <input type="checkbox" bind:checked={checked}>
    <slot/>
</label>


<style>
    .selected {
        color: #c1c1c1;
        text-decoration: line-through;
    }
</style>