<template>
	<div class="h-[calc(100vh-10rem)]">
		<NewAppointmentModal ref="newAppointmentModal" :selected-event="selectedEvent" @created="handleAppointmentCreated" @error="handleAppointmentError" @cancel="onCancelNewAppointment" />
		<AppointmentModal ref="appointmentModal" @updated="handleAppointmentUpdated" @error="handleAppointmentError" />
		<BaseCalendar ref="fullCalendar" :config="config" :class-names="handleEventClassNames" :event-sources="eventSources" @blockmode="handleBlockMode" @select="handleDateSelect" @event-click="handleEventClick" @event-drop="handleEventDrop" @drop="handleDrop" @event-receive="handleEventReceive" @event-resize="handleEventResize" class="h-full" />
	</div>
</template>

<script>
import store from "@/store";
import { mapState, mapActions } from "vuex";

import BaseCalendar from "@/core/components/calendar/BaseCalendar.vue";

import NewAppointmentModal from "@/core/components/modals/NewAppointmentModal.vue";
import AppointmentModal from "@/core/components/modals/AppointmentModal.vue";

export default {
	components: {
		BaseCalendar,
		NewAppointmentModal,
		AppointmentModal,
	},
	data() {
		return {
			config: {},
			blockmode: false,
			selectedEvent: null,
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
		...mapActions("planning", ["getConfig", "getEmployees", "rescheduleAppointment"]),

		// Modal methods
		getNewAppointmentModal() {
			return this.$refs.newAppointmentModal;
		},
		getAppointmentModal() {
			return this.$refs.appointmentModal;
		},

		handleEventClassNames(args) {
			if (this.blockmode) {
				const color = this.config?.colors?.BLOCKED;
				this.$refs.fullCalendar.setOption("eventColor", color);
			}
			return args;
		},

		handleBlockMode(blockmode) {
			this.blockmode = blockmode;
			if (blockmode) {
				const color = this.config?.colors?.BLOCKED;
				this.$refs.fullCalendar.setOption("eventColor", color);
			} else {
				this.$refs.fullCalendar.setOption("eventColor", "");
			}
		},
		handleDateSelect(selectInfo) {
			this.selectedEvent = selectInfo;
			this.getNewAppointmentModal().toggle();
		},
		handleEventClick(clickInfo) {
			const modal = this.getAppointmentModal();
			modal.event = clickInfo.event;
			modal.toggle();
		},

		handleAppointmentCreated(appointment) {
			this.toastSuccess("Appointment was created successfully");
			this.$refs.fullCalendar.getApi().refetchEvents();
		},
		async handleAppointmentUpdated(appointment) {
			this.toastSuccess("Appointment was updated successfully");
			this.$refs.fullCalendar.getApi().refetchEvents();
		},
		handleAppointmentError(action, error) {
			this.toastError(`An error occurred while ${action} the appointment`);
		},

		async rescheduleEvent(event) {
			this.rescheduleAppointment({
				id: event.id,
				start: event.startStr,
				end: event.endStr,
			})
				.then(() => {
					this.toastSuccess("Appointment was updated successfully");
					this.$refs.fullCalendar.getApi().refetchEvents();
				})
				.catch((error) => {
					this.toastError("Failed to update appointment");
					this.$refs.fullCalendar.getApi().refetchEvents();
				});
		},

		handleEventDrop(dropInfo) {
			this.rescheduleEvent(dropInfo.event);
		},

		handleDrop(dropInfo) {
			this.selectedEvent = {
				...JSON.parse(dropInfo.draggedEl.dataset.event),
				start: dropInfo.date,
				end: dropInfo.date,
				allDay: dropInfo.allDay,
			};
			this.getNewAppointmentModal().toggle();
		},
		handleEventReceive(receiveInfo) {
			const modal = this.getNewAppointmentModal();
			modal.event = {
				start: receiveInfo.event.start,
				end: receiveInfo.event.end,
				allDay: receiveInfo.event.allDay,
			};
			modal.toggle();
		},
		handleEventResize(resizeInfo) {
			this.rescheduleEvent(resizeInfo.event);
		},

		onCancelNewAppointment(event) {
			this.$refs.fullCalendar.getApi().refetchEvents();
		},
	},
	async mounted() {
		this.config = await this.getConfig();
		await this.getEmployees();
	},

	beforeDestroy() {},
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
