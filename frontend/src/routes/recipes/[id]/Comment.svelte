<script>
  import NewComment from "./NewComment.svelte";

  export let id;
  export let recipe_id;
  export let parent_id;
  export let author;
  export let created;
  export let updated;
  export let comment;
  export let children = [];

  const display_created = created.slice(0, 10) + ' ' + created.slice(11, 19) + ' UTC';
  const display_updated = updated.slice(0, 10) + ' ' + updated.slice(11, 19) + ' UTC';
</script>

<div class="container">
  <p>{comment}</p>
  <i>{author}, {display_created}</i>
  {#if created !== updated}
    <i> (edited {display_updated})</i>
  {/if}
  <div>
    <button on:click={() => alert('Not implemented yet')}>Edit</button>
    <NewComment parent_id={id} recipe_id={recipe_id}/>
  </div>
  {#if children.length}
    {#each children as child}
      <svelte:self {...child.node} children={child.children} />
    {/each}
  {/if}
</div>

<style>
  .container {
    background-color: #f4f4f4;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    margin-top: 1rem;
    padding: 1rem;
  }
</style>
