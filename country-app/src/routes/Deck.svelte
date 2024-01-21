<script>
	import { spring } from 'svelte/motion';
	import Card from './Card.svelte';

	let count = 1;

	const displayed_count = spring();
	$: displayed_count.set(count);
	$: offset = modulo($displayed_count, 1);

	/**
	 * @param {number} n
	 * @param {number} m
	 */
	function modulo(n, m) {
		// handle negative numbers
		return ((n % m) + m) % m;
	}
</script>

<div class="counter">
	<button on:click={() => (count -= 1)} aria-label="Previous card">
		<svg aria-hidden="true" viewBox="0 0 1 1">
			<path d="M1,0 L0,0.5 L1,1"/>
		</svg>
	</button>

	<div class="counter-viewport">
		<div class="counter-digits" style="transform: translate(0, {100 * offset}%)">
			<Card country_index={count}/>
		</div>
	</div>

	<button on:click={() => (count += 1)} aria-label="Next card">
		<svg aria-hidden="true" viewBox="0 0 1 1">
			<path d="M0,0 L1,0.5 L0,1" />
		</svg>
	</button>
</div>

<style>
	.counter {
		display: flex;
		border-top: 1px solid rgba(0, 0, 0, 0.1);
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);
		margin: 1rem 0;
	}

	.counter button {
		width: 2em;
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 0;
		background-color: transparent;
		touch-action: manipulation;
		font-size: 2rem;
	}


	svg {
		width: 50%;
		height: 50%;
	}

	path {
		vector-effect: non-scaling-stroke;
		stroke-width: 2px;
		stroke: #ffffff;
		fill: #efb71e;
	}

	.counter-viewport {
		width: 33em;
		height: 33em;
		overflow: hidden;
		text-align: center;
		position: relative;
	}

	.counter-digits {
		position: absolute;
		width: 100%;
		height: 100%;
	}

</style>
