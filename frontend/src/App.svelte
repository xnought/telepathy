<script lang="ts">
	import { Input, Label } from "flowbite-svelte";
	import ScatterPlot from "./ScatterPlot.svelte";
	import { Telepathy } from "./telepathy";
	Telepathy.query({ text: "dogs with hats" }).then((d) => console.log(d));

	let text = "test";
</script>

<main>
	<Label for="text">Text</Label>
	<Input id="text" bind:value={text} />
	<ScatterPlot />
</main>

<style>
</style>
