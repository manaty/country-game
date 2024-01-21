<script>
	let diceClass = 'dice';

	function rollDice() {
		const randomNumber = Math.floor(Math.random() * 6) + 1;
		diceClass = `dice show-${randomNumber}`;
	}
</script>

<div class="scene">
	<div class={diceClass}>
		<div class="face one">1</div>
		<div class="face two">2</div>
		<div class="face three">3</div>
		<div class="face four">4</div>
		<div class="face five">5</div>
		<div class="face six">6</div>
	</div>
</div>

<button on:click={rollDice}>Roll Dice</button>

<style>
	.scene {
		width: 200px;
		height: 200px;
		perspective: 1000px;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.dice {
		width: 100px;
		height: 100px;
		position: relative;
		transform-style: preserve-3d;
		transition: transform 1s;
	}

	.dice.show-1 {
		transform: rotateX(720deg) rotateY(720deg);
	}
	.dice.show-2 {
		transform: rotateX(810deg) rotateY(720deg);
	}
	.dice.show-3 {
		transform: rotateX(720deg) rotateY(810deg);
	}
	.dice.show-4 {
		transform: rotateX(720deg) rotateY(630deg);
	}
	.dice.show-5 {
		transform: rotateX(630deg) rotateY(720deg);
	}
	.dice.show-6 {
		transform: rotateX(720deg) rotateY(900deg);
	}

	.face {
		position: absolute;
		width: 100px;
		height: 100px;
		color: black;
		background: white;
		border: 1px solid #7e7b7b;
		line-height: 100px;
		font-size: 40px;
		text-align: center;
	}

	.one {
		transform: rotateY(0deg) translateZ(50px);
	}
	.two {
		transform: rotateY(90deg) translateZ(50px);
	}
	.three {
		transform: rotateY(180deg) translateZ(50px);
	}
	.four {
		transform: rotateY(-90deg) translateZ(50px);
	}
	.five {
		transform: rotateX(90deg) translateZ(50px);
	}
	.six {
		transform: rotateX(-90deg) translateZ(50px);
	}
</style>
