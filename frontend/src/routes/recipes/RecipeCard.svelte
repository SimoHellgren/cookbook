<script>
  import Tag from './Tag.svelte';
  export let id;
  export let name;
  export let servings;
  export let tags;
  export let method;
  export let source;
  export let created;
  export let updated;

  $: tagarray = tags.split(',').filter((t) => t);
</script>

<div class="container">
  <a href="/recipes/{id}">
    <h2>{name}</h2>
  </a>

  <div class="tag-grid">
    {#each tagarray as tag}
      <Tag name={tag} />
    {/each}
  </div>
</div>

<style>
  a {
    color: black;
    text-decoration: none;
  }

  .container {
    text-align: center;
    background-color: #f4f4f4;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .tag-grid {
    margin: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
</style>
