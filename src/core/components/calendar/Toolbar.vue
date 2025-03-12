<template>
	<div>
		<h2 class="text-base/7 font-semibold text-gray-900">Quick Appointment</h2>
		<div v-for="(event, index) in slotEvents" :data-event="JSON.stringify(event)" :key="`event-${index}`">
			{{ event.title }}
		</div>
	</div>
</template>

<script>
import { Draggable } from "@fullcalendar/interaction";

export default {
	props: {
		slotEvents: {
			type: Array,
			default() {
				return [];
			},
		},
	},
	directives: {
		fcevent: {
			bind(el) {
				new Draggable(el);
			},
		},
	},
};
</script>
