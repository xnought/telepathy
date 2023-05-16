<script lang="ts">
	import { Input, Label, Button } from "flowbite-svelte";
	import ScatterPlot from "./ScatterPlot.svelte";
	import { Telepathy, type QueryResponse } from "./telepathy";

	let text = "dogs with hats";
	let data: QueryResponse;
	let computing = false;
</script>

<main>
	<Label for="text">Text</Label>
	<Input id="text" bind:value={text} />
	<Button
		on:click={async () => {
			computing = true;
			data = await Telepathy.query({ text });
			computing = false;
		}}>Query Telepathy</Button
	>
	{#if computing}
		...computing
	{/if}
	<ScatterPlot {data} width={800} height={800} />
</main>

<style>
</style>
