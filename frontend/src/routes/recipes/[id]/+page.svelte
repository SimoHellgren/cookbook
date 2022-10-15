<script>
  import api from '$lib/api'
  import recipes from '$lib/stores/recipes';
  import Checkable from './Checkable.svelte';
  import Tag from '../Tag.svelte';
  import CommentSection from './CommentSection.svelte';
  import NewComment from './NewComment.svelte';
  export let data;

  const tags = data.recipe.tags.split(',').filter((t) => t);

  const remove = async () => {
    const really = window.confirm(`Really delete ${data.recipe.name}?`);

    if (really) {
      //delete recipe ingredients
      await Promise.all(
        data.ingredients.map((i) =>
          api.recipe_ingredients.remove(data.recipe.id, i.ingredient_id)
        ),
      );
      //delete recipe
      recipes.remove(data.recipe.id);
    }
  };
</script>

<div class="container">
  <div class="ingredients">
    <h3>Ingredients</h3>
    <ul>
      {#each data.ingredients as i}
        <li>
          <Checkable>
            {i.ingredient.name}
            {i.quantity}{i.measure}
          </Checkable>
        </li>
      {/each}
    </ul>
  </div>
  <div class="recipe">
    <header>
      <h1>{data.recipe.name}</h1>
      <p>{data.recipe.servings} servings</p>
      <p>Source: {data.recipe.source}</p>
      <div class="tag-grid">
        {#each tags as tag}
          <Tag name={tag} />
        {/each}
      </div>
      <a href={`/recipes/${data.recipe.id}/edit`}>edit</a>
      <button on:click={remove}>DELETE</button>
    </header>
    <div class="method">
      <ul>
        {#each data.recipe.method.split('\n').filter((t) => t) as line}
          <li>
            <Checkable>{line}</Checkable>
          </li>
        {/each}
      </ul>
    </div>
  </div>
  <div class="comments">
    <h2>Comments</h2>
    {#if !data.comments.length}
      <p>No comments yet</p>
    {:else}
      <CommentSection comments={data.comments} />
    {/if}
    <NewComment recipe_id={data.recipe.id} />
  </div>
</div>

<style>
  .container {
    margin-top: 1rem;
    display: grid;
    gap: 1rem;
    grid-template-columns: 1fr 3fr;
  }

  .ingredients {
    background-color: #f4f4f4;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    flex: 1;
    grid-column: 1/2;
    grid-row: 1/2;
  }

  .ingredients h3 {
    text-align: center;
  }

  h1 {
    margin: 0;
  }

  .recipe {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0;
    grid-column-start: 2;
    grid-row: 1/2;
  }

  .recipe header {
    display: grid;
    background-color: #f4f4f4;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
    padding: 1rem;
  }

  .method {
    background-color: #f4f4f4;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
  }

  .comments {
    grid-row-start: 2;
    grid-column-start: 2;
  }

  ul {
    margin-left: 0.1rem;
    padding: 0;
  }

  li {
    list-style: none;
  }

  .tag-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
</style>
