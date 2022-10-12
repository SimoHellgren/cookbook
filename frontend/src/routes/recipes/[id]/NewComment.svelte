<script>
    export let recipe_id;
    let author;
    let comment;
    let hidden = true;

    const onSubmit = async () => {
        alert(`posting comment:\n${comment}\n\nby ${author}\n\nto recipe ${recipe_id}`);
        hidden = true;
    }

    const cancel = () => {
        hidden = true;
        author = null;
        comment = null;
    }

</script>


<form on:submit|preventDefault={onSubmit} class:hidden={hidden}>
    <input bind:value={author} placeholder="author" />
    <textarea bind:value={comment} placeholder="comment..." />
    <div>
        <button type="submit">Save</button>
        <button type="button" on:click={cancel}>Cancel</button>
    </div>
</form>
<button on:click={() => hidden = false} class:hidden={!hidden}>New comment</button>

<style>
    form {
        display: flex;
        flex-direction: column;
        max-width: fit-content;
    }

    .hidden {
        display: none;
    }
</style>