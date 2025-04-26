<template>
	<NewAppointmentModal ref="appointmentModal" />

	<!-- <Toolbar :slot-events="config.events" /> -->
	<BaseCalendar ref="fullCalendar" :config="config" :class-names="handleEventClassNames" :event-sources="eventSources" @select="handleDateSelect" @event-click="handleEventClick" />
</template>

<script>
import store from "@/store";
import { mapState, mapActions } from "vuex";

import Toolbar from "@/core/components/calendar/Toolbar.vue";
import BaseCalendar from "@/core/components/calendar/BaseCalendar.vue";

import NewAppointmentModal from "@/core/components/modals/NewAppointmentModal.vue";

export default {
	components: {
		Toolbar,
		BaseCalendar,
		NewAppointmentModal,
	},
	data() {
		return {
			config: {},
		};
	},
	watch: {},
	computed: {
		...mapState("planning", {
			settings: (state) => state.settings,
			employee: (state) => state.employee,
			employees: (state) => state.employees,
		}),
		defaultSource() {
			return [
				{ id: "appointments", url: `/api/planning/employees/${this.employee?.username}/appointments/` },
				{ id: "blocked", url: `/api/planning/employees/${this.employee?.username}/blocked/` },
			];
		},
		eventSources() {
			return this.defaultSource;
		},
	},
	methods: {
		...mapActions("planning", ["getConfig", "getEmployees"]),

		handleEventClassNames(args) {
			if (this.blockmode) {
				const color = this.config?.colors?.BLOCKED;
				this.$refs.fullCalendar.setOption("eventColor", color);
			}
			return args;
		},
		handleDateSelect(selectInfo) {
			this.$refs.appointmentModal.event = selectInfo;
			this.$refs.appointmentModal.toggle();
		},
		handleEventClick(clickInfo) {
			// console.log(clickInfo);
		},
		async handleMessageReceived(message) {},
	},
	async mounted() {
		this.config = await this.getConfig();
		await this.getEmployees();
		// this.$websocket.$on("messageReceived", this.handleMessageReceived);
		// this.$websocket.connect(`${window.location.host}/ws/connect/planning/?username=${this.employee?.username}`);
	},
	beforeDestroy() {
		// this.$websocket.$off('messageReceived', this.handleMessageReceived)
		// this.$websocket.disconnect()
	},
	async beforeRouteUpdate(to, from, next) {
		const employee = await store.dispatch("planning/getEmployeeByUsername", to.params?.username);
		return next();
	},
	async beforeRouteEnter(to, from, next) {
		const employee = await store.dispatch("planning/getEmployeeByUsername", to.params?.username);
		return next();
	},
};
</script>
