<template>
	<FullCalendar ref="fullCalendar" :options="options" />
</template>

<script>
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import momentTimezonePlugin from "@fullcalendar/moment-timezone";

export default {
	props: {
		config: {
			default() {
				return {};
			},
		},
		classNames: {
			default() {
				return (args) => {};
			},
			type: Function,
		},
		eventSources: {
			default() {
				return [];
			},
		},
	},
	components: {
		FullCalendar,
	},
	data() {
		return {
			options: {
				plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, momentTimezonePlugin],
				initialView: "timeGridWeek",

				headerToolbar: {
					left: "prev,next today",
					center: "title",
					right: "timeGridDay,timeGridWeek,dayGridMonth",
				},
				navLinks: true, // can click day/week names to navigate views

				weekNumbers: true,

				businessHours: {
					daysOfWeek: [1, 2, 3, 4, 5],
					endTime: "20:00:00",
					startTime: "07:00:00",
				},
				nowIndicator: true,
				slotDuration: "00:30", // 30 mins
				slotMinTime: "05:00:00",
				slotMaxTime: "22:00:00",

				selectable: true,
				editable: true,

				eventClassNames: this.classNames,
				select: this.handleDateSelect,
				eventClick: this.handleEventClick,
				eventSources: this.eventSources,
			},
		};
	},
	watch: {
		config: {
			handler(val) {
				if (Object.keys(val.options).length > 0) {
					const calendar = this.getApi();

					calendar.batchRendering(() => {
						calendar.changeView(val.default_view);
						Object.keys(val.options).map((option) => {
							calendar.setOption(option, val?.options[option]);
						});
					});
				}
			},
		},
	},
	computed: {},
	methods: {
		getApi() {
			return this.$refs.fullCalendar.getApi();
		},
		gotoDate(date) {
			this.getApi().gotoDate(date);
		},
		addEvent(event) {
			this.getApi().addEvent(event);
		},
		setOption(prop, val) {
			this.getApi().setOption(prop, val);
		},
		changeView(view) {
			this.getApi().changeView(view);
		},
		refetchResource(resourceId) {
			const calendar = this.getApi();
			const resource = calendar.getEventSourceById(resourceId);
			resource.refetch();
		},
		refetchEvents() {
			const calendar = this.getApi();
			calendar.batchRendering(() => {
				calendar.removeAllEvents();
				calendar.refetchEvents();
			});
		},
		addEventSource(resource) {
			const calendar = this.getApi();
			calendar.addEventSource(resource);
		},
		removeEventResources(exclude) {
			const calendar = this.getApi();
			var sources = calendar.getEventSources();
			sources.map((source) => {
				if (!exclude.includes(source.id)) {
					source.remove();
				}
			});
		},
		handleDateSelect(selectInfo) {
			this.$emit("select", selectInfo);
		},
		handleEventClick(clickInfo) {
			this.$emit("event-click", clickInfo);
		},
	},
};
</script>
