export async function load({ fetch }) {
  return {
    mealplans: (await fetch('http://127.0.0.1:8000/mealplans')).json(),
  };
}
