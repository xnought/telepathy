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
	let hoveringImage = false;
	let hoveringImageData = {
		x: 0,
		y: 0,
		src: "",
	};
	let padding = 25;
	let imageEl: HTMLImageElement;
	$: {
		transform = createScalesWebgGLExtent(data);
		transform.scale(data);
	}
</script>

<div class="container-scatter">
	<div>
		<ReglScatter
			{data}
			{width}
			{height}
			on:pointOver={(e) => {
				hoveringImage = true;
				hoveringImageData = {
					src: data["imagePath"][e.detail.index],
					x: e.detail.canvasX + padding,
					y: e.detail.canvasY + padding,
				};
				console.log(hoveringImageData);
			}}
			on:pointOut={() => {
				hoveringImage = false;
			}}
		/>
	</div>
	{#if hoveringImage}
		<div
			class="hover-container"
			style="position: absolute; left: {hoveringImageData.x}px; top: {hoveringImageData.y}px;"
		>
			<img
				src={`http://localhost:8000/${hoveringImageData.src.slice(2)}`}
			/>
		</div>
	{/if}
</div>

<style>
	.hover-container {
		/* width: 50px;
		height: 50px; */
		border: 1px solid red;
	}
	.container-scatter {
		position: relative;
	}
</style>
