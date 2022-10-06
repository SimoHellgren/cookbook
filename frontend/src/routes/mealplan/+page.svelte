<script>
    import MealCard from "./MealCard.svelte";
    export let data;

    let filter_start;
    let filter_end;
    let hidedone = true;

    let create_start;
    let create_end;

    const checkStart = () => {
        // ensure create_start is on or before create_end by adjusting create_start
        if (!create_start || create_start > create_end) create_start = create_end
    }
    
    const checkEnd = () => {
        // ensure create_start is on or before create_end by adjusting create_end
        if (!create_end || create_start > create_end) create_end = create_start
    }

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
            .filter(mp => mp.date >= (filter_start || "0000") && mp.date <= (filter_end || "9999"))
            .filter(mp => !hidedone || mp.state !== "done")
    )

    const postMealplan = (data) => {
        return fetch("http://127.0.0.1:8000/mealplans", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
    } 

    const create = () => {
        // create lunch and dinner for two for each date
        for (var d = new Date(create_start); d <= new Date(create_end); d.setDate(d.getDate() +1)) {
            const base = {
                date: d.toISOString().slice(0, 10),
                servings: 2,
                state: "open",
            }

            Promise.all([
                postMealplan({...base, name: "lunch", position: 1}),
                postMealplan({...base, name: "dinner", position: 2}),
            ]).then(arr => Promise.all(arr.map(r => r.json())))
              .then(d => data.mealplans = [...data.mealplans, ...d])
        }

        create_start = null
        create_end = null
    }

</script>

<h1>Mealplans</h1>

<h3>Filter</h3>
<label>
    Start
    <input type="date" bind:value={filter_start}>
</label>
<label>
    End
    <input type="date" bind:value={filter_end}>
</label>
<label>
    Hide done
    <input type="checkbox" bind:checked={hidedone}>
</label>

{#each grouped as [date, meals]}
    <MealCard {date} {meals}/>
{/each}

<h3>Create</h3>
<p>Create a lunch and dinner for 2 people for each day between start and end</p>
<form on:submit|preventDefault={create}>
    <label>
        Start
        <input type="date" bind:value={create_start} on:change={checkEnd}>
    </label>
    <label>
        End
        <input type="date" bind:value={create_end} on:change={checkStart}>
    </label>
    <button type="submit">Go</button>
</form>