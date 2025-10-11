<template>
  <div class="h-[calc(100vh-10rem)]">
    <NewAppointmentModal ref="newAppointmentModal" :selected-event="selectedEvent" @created="handleAppointmentCreated" @error="handleAppointmentError" @cancel="onCancelNewAppointment" />
    <AppointmentModal ref="appointmentModal" @updated="handleAppointmentUpdated" @error="handleAppointmentError" />
    <NewBlockedModal ref="newBlockedModal" :selected-event="selectedEvent" @error="handleAppointmentError" @cancel="onCancelNewAppointment" />
    <BlockedModal ref="BlockedModal" :selected-event="selectedEvent" @updated="handleAppointmentUpdated" @error="handleAppointmentError" />
    <BaseCalendar ref="fullCalendar" :config="config" :class-names="handleEventClassNames" :event-sources="eventSources" @blockmode="handleBlockMode" @select="handleDateSelect" @event-click="handleEventClick" @event-drop="handleEventDrop" @drop="handleDrop" @event-receive="handleEventReceive" @event-resize="handleEventResize" class="h-full" />
  </div>
</template>

<script>
import store from '@/store';
import { mapState, mapActions } from 'vuex';

import BaseCalendar from '@/core/components/calendar/BaseCalendar.vue';

import NewAppointmentModal from '@/core/components/modals/NewAppointmentModal.vue';
import AppointmentModal from '@/core/components/modals/AppointmentModal.vue';
import NewBlockedModal from '@/core/components/modals/NewBlockedModal.vue';
import BlockedModal from '@/core/components/modals/BlockedModal.vue';

export default {
  components: {
    BaseCalendar,
    NewAppointmentModal,
    AppointmentModal,
    NewBlockedModal,
    BlockedModal,
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
    ...mapState('planning', {
      settings: (state) => state.settings,
      employee: (state) => state.employee,
      employees: (state) => state.employees,
    }),
    defaultSource() {
      return [
        { id: 'appointments', url: `/api/planning/employees/${this.employee?.username}/appointments/` },
        { id: 'blocked', url: `/api/planning/employees/${this.employee?.username}/blocked/` },
        { id: 'reminder', url: `/api/planning/employees/${this.employee?.username}/reminders/` },
      ];
    },
    eventSources() {
      return this.defaultSource;
    },
  },
  methods: {
    ...mapActions('planning', ['getConfig', 'getEmployees', 'rescheduleAppointment', 'rescheduleBlocked']),

    // Modal methods
    getNewAppointmentModal() {
      return this.$refs.newAppointmentModal;
    },
    getAppointmentModal() {
      return this.$refs.appointmentModal;
    },
    getNewBlockedModal() {
      return this.$refs.newBlockedModal;
    },
    getBlockedModal() {
      return this.$refs.BlockedModal;
    },

    handleEventClassNames(args) {
      // Set color for blocked events
      if (args.event.source.id === 'blocked') {
        const color = this.config?.colors?.BLOCKED;
        this.$refs.fullCalendar.setOption('eventColor', color);
      }
      return args.classNames;
    },

    handleBlockMode(blockmode) {
      this.blockmode = blockmode;
      if (blockmode) {
        const color = this.config?.colors?.BLOCKED;
        this.$refs.fullCalendar.setOption('eventColor', color);
      } else {
        const color = this.config?.colors?.BLOCKED;
        this.$refs.fullCalendar.setOption('eventColor', color);
      }
    },
    handleDateSelect(selectInfo) {
      this.selectedEvent = selectInfo;
      if (this.blockmode) {
        this.getNewBlockedModal().toggle();
      } else {
        this.getNewAppointmentModal().toggle();
      }
    },
    handleEventClick(clickInfo) {
      if (clickInfo.event.source.id === 'blocked') {
        const modal = this.getBlockedModal();
        modal.event = clickInfo.event;
        modal.toggle();
      } else if (clickInfo.event.source.id === 'appointments') {
        const modal = this.getAppointmentModal();
        modal.event = clickInfo.event;
        modal.toggle();
      }
    },

    handleAppointmentCreated(appointment) {
      this.toastSuccess('Appointment was created successfully');
      this.$refs.fullCalendar.getApi().refetchEvents();
    },
    async handleAppointmentUpdated(appointment) {
      this.toastSuccess('Appointment was updated successfully');
      this.$refs.fullCalendar.getApi().refetchEvents();
    },
    handleAppointmentError(action, error) {
      this.toastError(`An error occurred while ${action} the appointment`);
    },

    async rescheduleEvent(event) {
      if (event.source.id === 'blocked') {
        return this.rescheduleBlocked({
          id: event.id,
          start: event.startStr,
          end: event.endStr,
        })
          .then(() => {
            this.toastSuccess('Blocked time was updated successfully');
            this.$refs.fullCalendar.getApi().refetchEvents();
          })
          .catch((error) => {
            this.toastError('Failed to update blocked time');
            this.$refs.fullCalendar.getApi().refetchEvents();
          });
      } else if (event.source.id === 'appointments') {
        return this.rescheduleAppointment({
          id: event.id,
          start: event.startStr,
          end: event.endStr,
        })
          .then(() => {
            this.toastSuccess('Appointment was updated successfully');
            this.$refs.fullCalendar.getApi().refetchEvents();
          })
          .catch((error) => {
            this.toastError('Failed to update appointment');
            this.$refs.fullCalendar.getApi().refetchEvents();
          });
      }
      this.rescheduleAppointment({
        id: event.id,
        start: event.startStr,
        end: event.endStr,
      })
        .then(() => {
          this.toastSuccess('Appointment was updated successfully');
          this.$refs.fullCalendar.getApi().refetchEvents();
        })
        .catch((error) => {
          this.toastError('Failed to update appointment');
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
    const employee = await store.dispatch('planning/getEmployeeByUsername', to.params?.username);
    return next();
  },
  async beforeRouteEnter(to, from, next) {
    const employee = await store.dispatch('planning/getEmployeeByUsername', to.params?.username);
    return next();
  },
};
</script>
