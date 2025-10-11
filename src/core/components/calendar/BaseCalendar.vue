<template>
  <div class="h-full flex flex-col">
    <FullCalendar ref="fullCalendar" :options="options" class="flex-1 fc fc-media-screen fc-direction-ltr" />
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import momentTimezonePlugin from '@fullcalendar/moment-timezone';

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
        initialView: 'timeGridWeek',
        allDaySlot: true, // Enable the all-day slot
        allDayText: 'Reminders', // Custom label for the all-day slot

        customButtons: {
          blockmode: {
            text: 'block mode',
            click: (el) => {
              var button = el.target;
              if (button.classList.contains('active')) {
                button.classList.remove('active');
                this.$emit('blockmode', false);
              } else {
                button.classList.add('active');
                this.$emit('blockmode', true);
              }
            },
          },
        },

        headerToolbar: {
          left: 'prev,next today blockmode',
          center: 'title',
          right: 'timeGridDay,timeGridWeek,dayGridMonth',
        },
        navLinks: true, // can click day/week names to navigate views

        weekNumbers: true,

        businessHours: {
          daysOfWeek: [1, 2, 3, 4, 5],
          endTime: '20:00:00',
          startTime: '07:00:00',
        },
        nowIndicator: true,
        slotDuration: '00:30', // 30 mins
        slotMinTime: '05:00:00',
        slotMaxTime: '22:00:00',

        selectable: true,
        editable: true,
        droppable: true,
        dropAccept: '.fc-event',

        eventClassNames: this.classNames,
        select: this.handleDateSelect,
        eventClick: this.handleEventClick,
        eventDrop: this.handleEventDrop,
        eventReceive: this.handleEventReceive,
        eventResize: this.handleEventResize,
        eventDidMount: this.handleEventDidMount,
        eventSources: this.processEventSources(),
        eventContent: this.handleEventContent,
        height: '100%',
        aspectRatio: 4,
        expandRows: true,
        stickyHeaderDates: true,
        stickyFooterScrollbar: true,
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
    processEventSources() {
      return this.eventSources.map((source) => {
        if (source.id === 'reminder') {
          return {
            ...source,
            eventDataTransform: (event) => ({
              ...event,
              allDay: true, // Force all reminder events to be all-day events
              display: 'block', // Make reminders take up the full width
              icon: event.icon || ['fas', 'bell'], // Use event's icon or default to bell
              extendedProps: {
                ...event.extendedProps,
                isReminder: true,
              },
            }),
          };
        }
        return source;
      });
    },

    handleEventContent(arg) {
      if (arg.event.source?.id === 'reminder') {
        const icon = arg.event.extendedProps.icon || arg.event.icon || ['fas', 'bell'];
        return {
          html: `
            <div class="fc-event-main-frame">
              <div class="fc-event-title-container">
                <div class="fc-event-title fc-sticky">
                  <FontAwesomeIcon :icon="['fas', 'bell']" class="mr-2" />
                  ${arg.event.title}: ${arg.event.extendedProps.reason == 'OTHER' ? arg.event.extendedProps.other_reason : arg.event.extendedProps.reason}
                </div>
              </div>
            </div>
          `,
        };
      }
      return {
        html: `
		  <div class="fc-event-main-frame">
			<div class="fc-event-title-container">
			  <div class="fc-event-title fc-sticky">
				${arg.event.title}
			  </div>
			</div>
		  </div>
		`,
      };
    },
    handleDateSelect(selectInfo) {
      this.$emit('select', selectInfo);
    },
    handleEventClick(clickInfo) {
      this.$emit('event-click', clickInfo);
    },
    handleEventDrop(dropInfo) {
      // console.log("Event dropped:", dropInfo);
      this.$emit('event-drop', dropInfo);
    },
    handleEventReceive(receiveInfo) {
      // console.log("Event received:", receiveInfo);
      // this.$emit("event-receive", receiveInfo);
      // Remove the temporary event from calendar
      receiveInfo.event.remove();
    },
    handleEventResize(resizeInfo) {
      this.$emit('event-resize', resizeInfo);
    },
    handleEventDidMount(info) {
      this.$emit('event-did-mount', info);
    },
    handleDrop(dropInfo) {
      // Return false to indicate the event should be discarded
      this.$emit('drop', dropInfo);
      return false;
    },
  },
};
</script>

<style>
.fc-event-title i {
  margin-right: 0.5rem;
  font-size: 0.875rem;
}

/* Style for all-day reminders */
.fc-day-grid-event .fc-event-title i {
  margin-right: 0.5rem;
  font-size: 1rem;
}
</style>

<style>
button.fc-button.fc-button-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: oklch(54.6% 0.245 262.881);
  border-color: oklch(54.6% 0.245 262.881);
  color: white;
}

button.fc-button.fc-button-primary:hover,
button.fc-button.fc-button-primary:focus,
button.fc-button.fc-button-primary:active {
  background-color: oklch(62.3% 0.214 259.815);
  border-color: oklch(62.3% 0.214 259.815);
  color: white;
}

button.fc-button.fc-button-primary {
  background-color: oklch(54.6% 0.245 262.881);
  border-color: oklch(54.6% 0.245 262.881);
  color: white;
}

button.fc-button.fc-button-active {
  background-color: oklch(48.8% 0.243 264.376) !important;
  border-color: oklch(48.8% 0.243 264.376) !important;
  color: white;
}

button.fc-blockmode-button.fc-button.fc-button-primary.active {
  background-color: oklch(76.9% 0.188 70.08);
  border-color: oklch(76.9% 0.188 70.08);
  color: white;
}

button.fc-blockmode-button.fc-button.fc-button-primary.active:hover,
button.fc-blockmode-button.fc-button.fc-button-primary.active:focus,
button.fc-blockmode-button.fc-button.fc-button-primary.active:active {
  background-color: oklch(85.1% 0.16 70.08);
  border-color: oklch(85.1% 0.16 70.08);
  color: white;
}
</style>
