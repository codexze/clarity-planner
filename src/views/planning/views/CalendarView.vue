<template>
  <div class="h-[calc(100vh-10rem)]">
    <NewAppointmentModal ref="newAppointmentModal" :selected-event="selectedEvent" @created="handleAppointmentCreated" @error="handleAppointmentError" @cancel="onCancelNewAppointment" />
    <AppointmentModal ref="appointmentModal" @updated="handleAppointmentUpdated" @error="handleAppointmentError" />
    <NewBlockedTimeModal ref="newBlockedTimeModal" :selected-event="selectedEvent" @error="handleAppointmentError" @cancel="onCancelNewAppointment" />
    <BlockedTimeModal ref="BlockedTimeModal" :selected-event="selectedEvent" @updated="handleAppointmentUpdated" @error="handleAppointmentError" />
    <BaseCalendar ref="fullCalendar" :config="config" :class-names="handleEventClassNames" :event-sources="eventSources" @blockmode="handleBlockMode" @select="handleDateSelect" @event-click="handleEventClick" @event-drop="handleEventDrop" @drop="handleDrop" @event-receive="handleEventReceive" @event-resize="handleEventResize" class="h-full" />
  </div>
</template>

<script>
import store from '@/store';
import { mapState, mapActions } from 'vuex';
import session from '@/core/utils/Session';

import BaseCalendar from '@/core/components/calendar/BaseCalendar.vue';

import NewAppointmentModal from '@/core/components/modals/NewAppointmentModal.vue';
import AppointmentModal from '@/core/components/modals/AppointmentModal.vue';
import NewBlockedTimeModal from '@/core/components/modals/NewBlockedTimeModal.vue';
import BlockedTimeModal from '@/core/components/modals/BlockedTimeModal.vue';

export default {
  components: {
    BaseCalendar,
    NewAppointmentModal,
    AppointmentModal,
    NewBlockedTimeModal,
    BlockedTimeModal,
  },
  data() {
    return {
      config: {},
      blockmode: false,
      selectedEvent: null,
    };
  },
  watch: {
    'employee.username': {
      handler(newUsername, oldUsername) {
        if (newUsername && newUsername !== oldUsername) {
          // Refresh calendar events when employee changes
          this.$nextTick(() => {
            if (this.$refs.fullCalendar) {
              this.$refs.fullCalendar.getApi().refetchEvents();
            }
          });
        }
      },
      immediate: false,
    },
  },
  computed: {
    ...mapState('employees', {
      settings: (state) => state.settings,
      employee: (state) => state.employee,
      employees: (state) => state.employees,
    }),
    defaultSource() {
      return [
        {
          id: 'appointments',
          events: this.fetchAppointments,
        },
        {
          id: 'blocked',
          events: this.fetchBlockedTime,
        },
        {
          id: 'reminder',
          events: this.fetchReminders,
        },
      ];
    },
    eventSources() {
      return this.defaultSource;
    },
  },
  methods: {
    ...mapActions('employees', ['getConfig', 'getEmployees']),
    ...mapActions('planning', ['rescheduleAppointment', 'rescheduleBlockedTime']),

    // Intelligent time slot suggestions
    // const suggestOptimalTimeSlots = (clientHistory, serviceRequirements) => {
    // Analyze client's appointment history
    // Consider service duration and requirements
    // Factor in travel time for onsite appointments
    // Return ranked suggestions
    // }

    // Conflict resolution with smart rescheduling
    // const handleScheduleConflict = (conflictingAppointments) => {
    // Suggest alternative time slots
    // Auto-negotiate with clients
    // Batch reschedule related appointments
    // }

    // Authenticated event fetch methods
    async fetchAppointments(info, successCallback, failureCallback) {
      try {
        if (!this.employee?.username) {
          successCallback([]);
          return;
        }
        const response = await session.get(`/api/v1/planning/appointments/employee/${this.employee.username}/`, {
          params: {
            start: info.startStr,
            end: info.endStr,
          },
        });
        successCallback(response.data);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
        failureCallback(error);
      }
    },

    async fetchBlockedTime(info, successCallback, failureCallback) {
      try {
        if (!this.employee?.username) {
          successCallback([]);
          return;
        }
        const response = await session.get(`/api/v1/planning/blocked/employee/${this.employee.username}/`, {
          params: {
            start: info.startStr,
            end: info.endStr,
          },
        });
        successCallback(response.data);
      } catch (error) {
        console.error('Failed to fetch blocked time:', error);
        failureCallback(error);
      }
    },

    async fetchReminders(info, successCallback, failureCallback) {
      try {
        if (!this.employee?.username) {
          successCallback([]);
          return;
        }
        const response = await session.get(`/api/v1/planning/reminders/employee/${this.employee.username}/`, {
          params: {
            start: info.startStr,
            end: info.endStr,
          },
        });
        successCallback(response.data);
      } catch (error) {
        console.error('Failed to fetch reminders:', error);
        failureCallback(error);
      }
    },

    // Modal methods
    getNewAppointmentModal() {
      return this.$refs.newAppointmentModal;
    },
    getAppointmentModal() {
      return this.$refs.appointmentModal;
    },
    getNewBlockedTimeModal() {
      return this.$refs.newBlockedTimeModal;
    },
    getBlockedTimeModal() {
      return this.$refs.BlockedTimeModal;
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
        this.getNewBlockedTimeModal().toggle();
      } else {
        this.getNewAppointmentModal().toggle();
      }
    },
    handleEventClick(clickInfo) {
      if (clickInfo.event.source.id === 'blocked') {
        const modal = this.getBlockedTimeModal();
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
        return this.rescheduleBlockedTime({
          id: event.id,
          start: event.startStr,
          end: event.endStr,
        })
          .then(() => {
            this.toastSuccess('BlockedTime time was updated successfully');
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
    const employee = await store.dispatch('employees/getEmployeeByUsername', to.params?.username);
    return next();
  },
  async beforeRouteEnter(to, from, next) {
    const employee = await store.dispatch('employees/getEmployeeByUsername', to.params?.username);
    return next();
  },
};
</script>
