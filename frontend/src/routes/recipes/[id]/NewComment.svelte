<script>
  import comments from '$lib/stores/comments.js'
  export let recipe_id;
  export let parent_id = null;
  let author;
  let comment;
  let hidden = true;

  let buttonText = parent_id ? "Reply" : "New comment"

  const onSubmit = async () => {
    comments.create({
      recipe_id,
      comment,
      author,
      parent_id,
    })
    hidden = true;
  };

  const cancel = () => {
    hidden = true;
    author = null;
    comment = null;
  };
</script>

<form on:submit|preventDefault={onSubmit} class:hidden>
  <input bind:value={author} placeholder="author" />
  <textarea bind:value={comment} placeholder="comment..." />
  <div>
    <button type="submit">Save</button>
    <button type="button" on:click={cancel}>Cancel</button>
  </div>
</form>
<button on:click={() => (hidden = false)} class:hidden={!hidden}>{buttonText}</button>

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
