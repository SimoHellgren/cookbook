<script>
    import MealCard from "./MealCard.svelte";
    export let data;

    let startdate;
    let enddate;
    let hidedone = true;

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

    $: grouped = groupByDate(
        data.mealplans
            .filter(mp => mp.date >= (startdate || "0000") && mp.date <= (enddate || "9999"))
            .filter(mp => !hidedone || mp.state !== "done")
    )
</script>

<h1>Mealplans</h1>

<h3>Filter</h3>
<label>
    Start
    <input type="date" bind:value={startdate}>
</label>
<label>
    End
    <input type="date" bind:value={enddate}>
</label>
<label>
    Hide done
    <input type="checkbox" bind:checked={hidedone}>
</label>

{#each grouped as [date, meals]}
    <MealCard {date} {meals}/>
{/each}
