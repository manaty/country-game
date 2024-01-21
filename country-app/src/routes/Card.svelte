<script>
    import { onMount } from 'svelte';
    export let country_index = 1;
    let flipped = false;
    let country_name = "";

    /**
	 * @type {string}
	 */
    let front_url=`https://media.githubusercontent.com/media/manaty/country-game/main/files/cards/1_Angola_front.png`;;

    /**
	 * @type {string}
	 */
    let back_url=`https://media.githubusercontent.com/media/manaty/country-game/main/files/cards/1_Angola_back.png`;

    /**
	 * @type {string | any[]}
	 */
    let rows = [];

    onMount(async () => {
        const csvUrl = "https://raw.githubusercontent.com/manaty/country-game/main/files/country%20game%20-%20no%20landmarks.csv";
        const response = await fetch(csvUrl);
        const csvText = await response.text();
        rows = csvText.split('\n').map(row => row.split(','));
        updateCountryName();
    });

    $: if (country_index) {
        updateCountryName();
        updateUrls();
    }

    function updateCountryName() {
        if (country_index <= rows.length) {
            country_name = rows[country_index-1][0]; // Assuming the country name is in the first column
        } else {
            country_name = "Angola";
        }
    }

    function updateUrls() {
        front_url = `https://media.githubusercontent.com/media/manaty/country-game/main/files/cards/${country_index}_${country_name.replace(/\s/g, '_')}_front.png`;
        back_url = `https://media.githubusercontent.com/media/manaty/country-game/main/files/cards/${country_index}_${country_name}_back.png`;
    }
</script>

	<button
		class="card"
		class:flipped={flipped}
		on:click={() => flipped = !flipped}
	>
		<div class="front" style={`--bg_url: url('${front_url}');`} >
		</div>
		<div class="back" style={`--bg_url: url('${back_url}');`}>
		</div>
	</button>

<style>

	.card {
		position: relative;
		aspect-ratio: 2.5 / 3.5;
		font-size: min(1vh, 0.25rem);
		height: 80%;
		border-radius: 2em;
		transform:  rotateZ(-90deg) rotateY(180deg);
		transition: transform 0.4s;
		transform-style: preserve-3d;
		padding: 0;
		user-select: none;
		cursor: pointer;
	}

	.card.flipped {
		transform: rotateY(0);
	}

	.front, .back {
		display: flex;
		align-items: center;
		justify-content: center;
		position: absolute;
		left: 0;
		top: 0;
        width: 100%;
        height: 100%;
		backface-visibility: hidden;
		border-radius: 2em;
		border: 1px solid;
		box-sizing: border-box;
		padding: 2em;
        background: var(--bg_url) no-repeat;
        background-size: cover;
	}

	.back {
     	transform: rotateY(180deg);
	}
</style>