<template>
  <!-- Modal backdrop with fixed position and overflow hidden -->
  <div v-if="visible" class="fixed inset-0 z-50 backdrop-blur-sm overflow-hidden">
    <!-- Modal container with scrollable content -->
    <div class="fixed inset-0 bg-gradient-to-t from-gray-700 overflow-y-auto">
      <div class="flex min-h-full items-center justify-center p-4">
        <div class="relative w-full max-w-6xl">
          <!-- Modal content -->
          <div class="relative bg-white rounded-xl shadow-lg max-h-[90vh] flex flex-col border border-gray-200">
            <div class="absolute right-0 top-0 hidden pt-4 pr-4 sm:block">
              <!-- Close button -->
            </div>
            <!-- Modal header (stays fixed) -->
            <div class="px-8 py-6 border-b border-gray-200">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-2xl font-semibold text-gray-900">Block Time Slot</h2>
                  <p class="mt-2 text-sm text-gray-600">Review and modify the blocked time slot information below.</p>
                </div>
                <button @click="close" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center transition-colors duration-150">
                  <font-awesome-icon :icon="['fas', 'xmark']" />
                  <span class="sr-only">Close modal</span>
                </button>
              </div>
            </div>

            <!-- Modal body (scrollable) -->
            <div class="px-6 py-4 bg-gray-50 overflow-y-auto flex-1">
              <div class="mt-8 grid grid-cols-1 gap-x-6 gap-y-6">
                <div class="space-y-6">
                  <!-- Time Blocking Card -->
                  <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
                    <div class="px-6 py-4 border-b border-gray-200">
                      <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                        <font-awesome-icon :icon="['fas', 'calendar-clock']" class="mr-3 text-blue-600" />
                        Schedule & Timing
                      </h3>
                      <p class="mt-1 text-sm text-gray-600">Set the time slot you want to block</p>
                    </div>

                    <div class="p-6 space-y-6">
                      <!-- Appointment Date -->
                      <div class="space-y-2">
                        <label class="flex items-center text-sm font-medium text-gray-900">
                          <font-awesome-icon :icon="['fas', 'calendar']" class="mr-2 text-gray-400" />
                          Date
                        </label>
                        <div class="relative">
                          <VueDatePicker hide-input-icon v-model="appointmentDate" :enable-time-picker="false" :min-date="new Date()" format="MMMM d, yyyy" class="block w-full" :disabled="true" input-class-name="rounded-lg border border-gray-300 bg-gray-50 py-3  pr-4 text-sm text-gray-600 cursor-not-allowed" />
                        </div>
                        <p class="text-xs text-gray-500 flex items-center">
                          <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1" />
                          Date cannot be changed from this view
                        </p>
                      </div>

                      <!-- Time Selection -->
                      <div class="grid grid-cols-2 gap-4">
                        <!-- Start Time -->
                        <div class="space-y-2">
                          <label for="start_time" class="flex items-center text-sm font-medium text-gray-900">Start Time</label>
                          <div class="relative">
                            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                              <font-awesome-icon :icon="['fas', 'clock']" class="text-gray-400" />
                            </div>
                            <select id="start_time" v-model="start_time" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                              <option value="">Select start time</option>
                              <option v-for="time in startTimes" :key="time" :value="time">{{ time }}</option>
                            </select>
                          </div>
                        </div>

                        <!-- End Time -->
                        <div class="space-y-2">
                          <label for="end_time" class="flex items-center text-sm font-medium text-gray-900">End Time</label>
                          <div class="relative">
                            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                              <font-awesome-icon :icon="['fas', 'clock']" class="text-gray-400" />
                            </div>
                            <select id="end_time" v-model="end_time" @change="calculateStartTime" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                              <option value="">Select end time</option>
                              <option v-for="time in endTimes" :key="time" :value="time">{{ time }}</option>
                            </select>
                          </div>
                        </div>
                      </div>

                      <!-- Duration Display -->
                      <div v-if="start_time && end_time" class="p-3 bg-blue-50 rounded-lg border border-blue-200">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center text-sm text-blue-700">
                            <font-awesome-icon :icon="['fas', 'clock']" class="mr-2" />
                            <span class="font-medium">Block Duration</span>
                          </div>
                          <span class="text-sm font-semibold text-blue-800">{{ calculateDuration() }}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Block Details Card -->
                  <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
                    <div class="px-6 py-4 border-b border-gray-200">
                      <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                        <font-awesome-icon :icon="['fas', 'ban']" class="mr-3 text-blue-600" />
                        Block Information
                      </h3>
                      <p class="mt-1 text-sm text-gray-600">Specify the reason and additional details</p>
                    </div>

                    <div class="p-6 space-y-6">
                      <!-- Reason Field -->
                      <div class="space-y-2">
                        <label for="reason" class="flex items-center text-sm font-medium text-gray-900">
                          <font-awesome-icon :icon="['fas', 'tag']" class="mr-2 text-gray-400" />
                          Reason for Blocking
                          <span class="text-red-500 ml-1">*</span>
                        </label>
                        <div class="relative">
                          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                            <font-awesome-icon :icon="['fas', 'tag']" class="text-gray-400" />
                          </div>
                          <input type="text" name="reason" id="reason" v-model="form.reason" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="e.g. Team meeting, Personal appointment, Break" required />
                        </div>
                        <p class="text-xs text-gray-500 flex items-center">
                          <font-awesome-icon :icon="['fas', 'lightbulb']" class="mr-1" />
                          Briefly describe why this time needs to be blocked
                        </p>
                      </div>

                      <!-- Notes Section -->
                      <div class="space-y-2">
                        <label for="notes" class="flex items-center text-sm font-medium text-gray-900">
                          <font-awesome-icon :icon="['fas', 'sticky-note']" class="mr-2 text-gray-400" />
                          Additional Notes
                        </label>
                        <div class="relative">
                          <textarea id="notes" v-model="form.notes" class="block w-full rounded-lg border border-gray-300 bg-white py-3 px-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 resize-none" rows="4" placeholder="Add any special instructions, context, or important details for this blocked time..."></textarea>
                          <div class="absolute bottom-3 right-3 text-xs text-gray-400 pointer-events-none">{{ form.notes?.length || 0 }}/500</div>
                        </div>
                        <p class="text-xs text-gray-500 flex items-center">
                          <font-awesome-icon :icon="['fas', 'lightbulb']" class="mr-1" />
                          Include any context or special instructions for this blocked period
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="border-t border-gray-100 px-6 py-4">
              <div class="flex items-center justify-between">
                <div class="text-xs text-gray-500">
                  <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1" />
                  This will prevent new bookings for the selected time
                </div>
                <div class="flex items-center space-x-3">
                  <button @click="close" class="px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-150 min-w-[90px]">Cancel</button>
                  <button @click="submit" :disabled="!form.reason || !start_time || !end_time" class="px-4 py-2.5 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600 min-w-[120px] flex items-center justify-center space-x-2">
                    <font-awesome-icon :icon="['fas', 'ban']" />
                    <span>Block Time</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import Form from '@/core/utils/Form';

import VueDatePicker from '@vuepic/vue-datepicker';
import { mapActions } from 'vuex';

import QuickClientTable from '../quick-tables/QuickClientTable.vue';

export default {
  components: {
    VueDatePicker,
    QuickClientTable,
  },
  props: {
    selectedEvent: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      visible: false,

      config: {},
      event: null,

      form: new Form({
        consistency_token: '00000000',
        start: null,
        end: null,
        reason: null,
        notes: null,
      }),

      start_time: null,
      end_time: null,

      intervalTime: [],
      employees: [],
    };
  },
  watch: {
    event: {
      handler(val) {
        if (val) {
          // Use moment.tz to ensure correct timezone handling
          const timezone = 'America/Paramaribo'; // Match Django settings
          this.start_time = moment.tz(val.start, timezone).format('HH:mm');
          this.end_time = moment.tz(val.end, timezone).format('HH:mm');

          // console.log("Extended props:", val.extendedProps);
          this.form.populate(val.extendedProps);
        }
      },
    },
    start_time: {
      handler(val) {
        if (val) {
          const timezone = 'America/Paramaribo'; // Match Django settings
          var date = moment.tz(this.event.start, timezone);
          const time = moment.tz(val, 'HH:mm', timezone);
          date.set({ h: time.get('h'), m: time.get('m') });
          this.form.start = date.format(); // Use format() instead of toISOString(true) to preserve timezone
          // console.log("Updated start time:", this.form.start);
        }
      },
    },
    end_time: {
      handler(val) {
        if (val) {
          var date = moment(this.event.end);
          date.set({ h: moment(val, 'HH:mm').get('h'), m: moment(val, 'HH:mm').get('m') });
          this.form.end = date.toISOString(true);
          // console.log("Updated end time:", this.form.only(["end"]));
        }
      },
    },
  },
  computed: {
    appointmentDate() {
      return this.toFullDate(this.event?.start);
    },
    eventStart() {
      return this.start_time;
    },
    eventEnd() {
      return this.end_time;
    },
    startTimes() {
      if (this.eventEnd) {
        let slice = this.intervalTime.findIndex((time) => time === this.eventEnd);
        return this.intervalTime.slice(0, slice);
      }
      return this.intervalTime;
    },
    endTimes() {
      if (this.eventStart) {
        let slice = this.intervalTime.findIndex((time) => time === this.eventStart);
        return this.intervalTime.slice(slice + 1, this.intervalTime.length);
      }
      return this.intervalTime;
    },
  },
  methods: {
    ...mapActions('planning', ['getConfig', 'loadIntervalTime', 'updateBlocked']),

    toggle() {
      this.visible = !this.visible;
    },
    calculateDuration() {
      if (!this.start_time || !this.end_time) return '';

      const start = moment(this.start_time, 'HH:mm');
      const end = moment(this.end_time, 'HH:mm');
      const duration = moment.duration(end.diff(start));

      const hours = Math.floor(duration.asHours());
      const minutes = duration.minutes();

      if (hours > 0 && minutes > 0) {
        return `${hours}h ${minutes}m`;
      } else if (hours > 0) {
        return `${hours}h`;
      } else {
        return `${minutes}m`;
      }
    },
    close() {
      this.start_time = null;
      this.end_time = null;
      this.type = null;
      this.form.reset(this.selectedEvent);
      this.visible = false;
      this.$emit('cancel');
    },
    submit() {
      // console.log("Submitting form:", this.form.data());
      this.updateBlocked(this.form.data())
        .then((response) => {
          this.$emit('updated', response);
          this.close();
        })
        .catch((error) => {
          this.$emit('error', 'updating', error);
        });
    },
  },
  async mounted() {
    this.config = await this.getConfig();
    this.intervalTime = await this.loadIntervalTime({
      start: this.config.slot.MIN,
      end: this.config.slot.MAX,
      interval: this.config.slot.INTERVAL,
    });
  },
};
</script>
