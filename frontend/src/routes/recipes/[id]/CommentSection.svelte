<script>
  import Comment from './Comment.svelte';
  export let comments;

  // construct tree
  const lookup = new Map();
  const children = new Map([[0, []]]); // 0 is root

  comments
    .sort((a, b) => a.id - b.id)
    .forEach((comment) => {
      // add comment to lookup
      lookup.set(comment.id, comment);

      // initialize children
      children.set(comment.id, []);

      // add comment's id to it's parent's children
      const parent = comment.parent_id || 0;
      children.set(parent, children.get(parent).concat(comment.id));
    });

  //depth first search
  const walk = (i) => {
    let pair = { node: lookup.get(i), children: [] };

    const kids = children.get(i) || [];
    kids.forEach((child) => {
      pair.children.push(walk(child));
    });

    return pair;
  };

  const tree = children.get(0).map(walk);
</script>

{#each tree as { node, children }}
  <Comment {...node} {children} />
{/each}
