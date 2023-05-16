<script lang="ts">
	import { Input, Label } from "flowbite-svelte";
	import ScatterPlot from "./ScatterPlot.svelte";
	import { Telepathy } from "./telepathy";
	Telepathy.test().then((res) => console.log(res));

	let text = "test";
</script>

<main>
	<Label for="text">Text</Label>
	<Input id="text" bind:value={text} />
	<ScatterPlot />
</main>

<style>
</style>
