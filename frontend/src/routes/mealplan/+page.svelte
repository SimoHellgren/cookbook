<script>
    import {recipes} from '../../stores.js'
    import MealCard from "./MealCard.svelte";
    export let data;

    // group mealpans by date
    const groupByDate = (data) => {
        const m = new Map()

        data.forEach(row => {
            // initialize empty array
            if (!m.has(row.date)) m.set(row.date, [])

            m.set(row.date, [...m.get(row.date), row])
        })

        return [...m].sort()
    }

    $: grouped = groupByDate(data.mealplans)
</script>

<h1>Mealplans</h1>

{#each grouped as [date, meals]}
    <MealCard {date} {meals}/>
{/each}
