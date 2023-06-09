<script lang="ts">
	import { scaleLinear } from "d3-scale";
	import createScatterPlot from "regl-scatterplot";
	import { createEventDispatcher, onDestroy, onMount } from "svelte";
	import { CONTINUOUS_COLOR_SCALE } from "./colors";
	import type {
		ReglScatterConfig,
		ReglScatterObject,
		ReglScatterPointDispatch,
		Points2D,
	} from "./index";
	import { WEBGL_EXTENT } from "./index";

	const dispatch = createEventDispatcher<{
		deselect: number[];
		select: number[];
		pointOver: ReglScatterPointDispatch;
		pointOut: ReglScatterPointDispatch;
		mount: ReglScatterObject;
	}>();

	export let width: number;
	export let height: number;
	export let data: Points2D;
	export let config: ReglScatterConfig = {};
	export let pointSize = 5;
	export let pointColor = "#6a1b9a";
	export let pointOutline = 3;
	export let style = "";

	let xScale = scaleLinear().domain(WEBGL_EXTENT); // between [-1, 1] -> canvas X
	let yScale = scaleLinear().domain(WEBGL_EXTENT); // between [-1, 1] -> canvas Y
	let scatterPtr: ReglScatterObject;
	let canvasEl: HTMLCanvasElement;
	let modeCssClass: "normal-mode" | "pan-mode" | "lasso-mode" = "normal-mode";

	$: scatterPtr?.set({
		pointSize,
	});

	$: scatterPtr?.set({
		width,
		height,
	});

	$: {
		// make sure this is not called before we actually create the scatterPtr
		if (scatterPtr && data?.x.length > 0) {
			draw(data);
		}
	}

	onMount(() => {
		init();
		dispatch("mount", scatterPtr);
	});

	onDestroy(() => {
		scatterPtr.destroy();
	});

	function init() {
		scatterPtr = createScatterPlot({
			canvas: canvasEl,
			width,
			height,
			xScale,
			yScale,
			...config,
		});

		scatterPtr.set({
			lassoColor: pointColor,
			pointColorHover: pointColor,
			pointColorActive: pointColor,
			backgroundColor: "#FFFFFF",
			pointOutlineWidth: pointOutline,
		});

		scatterPtr.set({
			colorBy: "category",
			pointColor: CONTINUOUS_COLOR_SCALE,
		});
		scatterPtr.set({
			colorBy: "value",
			pointColor: CONTINUOUS_COLOR_SCALE,
		});

		// listeners
		listenLasso();
		listenPointHover();
	}

	function draw(points: Points2D) {
		if (scatterPtr) {
			scatterPtr
				.draw(
					{
						x: points.x,
						y: points.y,
						category: points?.score,
						value: points?.score,
					},
					{ transition: true }
				)
				.then(() => {
					// let selIds = $selectionIds.ids as unknown[];
					// let selectedPoints = [];
					// points.ids.forEach((id: number | string, i) => {
					// 	if (selIds.includes(id)) {
					// 		selectedPoints.push(i);
					// 	}
					// });
					// scatterPtr.select(selectedPoints);
				});
		}
	}

	function listenPointHover() {
		if (scatterPtr) {
			scatterPtr.subscribe(
				"pointOut",
				(index) => {
					const canvasX = xScale(data.x[index]);
					const canvasY = yScale(data.y[index]);
					dispatch("pointOut", {
						index,
						canvasX,
						canvasY,
					});
				},
				null
			);
			scatterPtr.subscribe(
				"pointOver",
				(index) => {
					const canvasX = xScale(data.x[index]);
					const canvasY = yScale(data.y[index]);
					dispatch("pointOver", {
						index,
						canvasX,
						canvasY,
					});
				},
				null
			);
		}
	}

	function listenLasso() {
		if (scatterPtr) {
			scatterPtr.subscribe(
				"deselect",
				() => {
					dispatch("deselect", []);
				},
				null
			);
			scatterPtr.subscribe(
				"select",
				(d) => {
					if (d) {
						dispatch("select", d["points"]);
					}
				},
				null
			);
		}
	}
</script>

<svelte:window
	on:keydown={(e) => {
		if (e.key === "Shift") {
			modeCssClass = "lasso-mode";
		}
	}}
	on:keyup={() => {
		modeCssClass = "normal-mode";
	}}
	on:mousedown={() => {
		if (modeCssClass !== "lasso-mode") {
			modeCssClass = "pan-mode";
		}
	}}
	on:mouseup={() => {
		modeCssClass = "normal-mode";
	}}
/>

<canvas
	{style}
	class={modeCssClass}
	bind:this={canvasEl}
	on:mousemove
	on:mouseleave
	on:mouseenter
/>

<style>
	.normal-mode {
		cursor: default;
	}
	.pan-mode {
		cursor: move;
	}
	.lasso-mode {
		cursor: crosshair;
	}
</style>
