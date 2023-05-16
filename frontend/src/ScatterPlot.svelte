<script lang="ts">
	import ReglScatter from "./regl-scatter/ReglScatter.svelte";
	import {
		createScalesWebgGLExtent,
		type WebGLExtentScalers,
	} from "./regl-scatter";

	export let data = {
		x: [1, 2, 3],
		y: [3, 4, 5],
	};
	export let width = 500;
	export let height = 500;

	let transform: WebGLExtentScalers;
	$: {
		transform = createScalesWebgGLExtent(data);
		transform.scale(data);
	}
</script>

<div style="width: {width}px; height: {height}px;">
	<ReglScatter {data} {width} {height} />
</div>

<style>
	div {
		border: 1px solid black;
	}
</style>
