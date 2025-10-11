<template>
  <div>
    <!-- Header Section -->
    <div class="space-y-4">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-gray-600">View all appointments for this client, including past and upcoming sessions.</p>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ appointments.length }} {{ appointments.length === 1 ? 'appointment' : 'appointments' }}</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && appointments.length === 0" class="text-center py-12">
      <font-awesome-icon :icon="['fas', 'calendar-xmark']" class="text-4xl text-gray-300 mb-4" />
      <h5 class="text-lg font-medium text-gray-900 mb-2">No Appointments Found</h5>
      <p class="text-gray-500">This client doesn't have any appointments yet.</p>
    </div>

    <!-- Appointment Cards -->
    <div v-else class="space-y-4">
      <div v-for="appointment in appointments" :key="appointment.id" class="group relative bg-gray-50 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 p-4">
        <div class="flex items-start justify-between">
          <!-- Main Content -->
          <div class="flex items-start space-x-4 flex-1">
            <!-- Date & Status -->
            <div class="flex-shrink-0">
              <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors duration-200">
                <font-awesome-icon :icon="['fas', 'calendar-check']" class="text-blue-600" />
              </div>
              <div class="mt-2 flex justify-center">
                <span v-if="appointment.is_past" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  <font-awesome-icon :icon="['fas', 'history']" class="mr-1" />
                  Past
                </span>
                <span v-else-if="appointment.is_future" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <font-awesome-icon :icon="['fas', 'calendar']" class="mr-1" />
                  Future
                </span>
              </div>
            </div>

            <!-- Details -->
            <div class="flex-1 min-w-0">
              <!-- Date and Time -->
              <div class="flex items-center space-x-3 mb-3">
                <div>
                  <h5 class="text-base font-semibold text-gray-900 group-hover:text-blue-900">
                    {{ appointment.appointment_date ? toLocaleDate(appointment.appointment_date) : 'Date not available' }}
                  </h5>
                  <div class="flex items-center text-sm text-gray-500 group-hover:text-blue-700 mt-1">
                    <font-awesome-icon :icon="['fas', 'clock']" class="mr-1.5" />
                    {{ appointment.start_time }} - {{ appointment.end_time }}
                  </div>
                </div>
              </div>

              <!-- Service and Employee Info -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'user-tie']" class="text-blue-600 text-xs" />
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Team Member</p>
                      <p class="text-sm font-medium text-gray-900">{{ appointment.employee_name }}</p>
                    </div>
                  </div>

                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'scissors']" class="text-blue-600 text-xs" />
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Service</p>
                      <p class="text-sm font-medium text-gray-900">{{ appointment.service_name }}</p>
                    </div>
                  </div>
                </div>

                <div class="space-y-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'plus-circle']" class="text-blue-600 text-xs" />
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Add-ons</p>
                      <p class="text-sm font-medium text-gray-900">
                        {{ appointment.addons.length ? `${appointment.addons.length} add-on${appointment.addons.length > 1 ? 's' : ''}` : 'None' }}
                      </p>
                    </div>
                  </div>

                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-blue-50 flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'dollar-sign']" class="text-blue-600 text-xs" />
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Payment</p>
                      <p class="text-sm font-medium text-gray-900">${{ appointment.payment_amount }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex-shrink-0 ml-4">
            <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <!-- Edit Button -->
              <button @click="onEdit(appointment.id)" class="inline-flex items-center px-3 py-2 text-xs font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg border border-blue-200 hover:border-blue-300 transition-all duration-150 hover:shadow-sm" title="Edit appointment">
                <font-awesome-icon :icon="['fas', 'edit']" class="mr-1.5" />
                Edit
              </button>

              <!-- Invoice Button -->
              <button @click="onInvoice(appointment.id)" class="inline-flex items-center px-3 py-2 text-xs font-medium text-green-700 bg-green-50 hover:bg-green-100 rounded-lg border border-green-200 hover:border-green-300 transition-all duration-150 hover:shadow-sm" title="Create invoice">
                <font-awesome-icon :icon="['fas', 'file-invoice']" class="mr-1.5" />
                Invoice
              </button>
            </div>

            <!-- Mobile/Always Visible Actions (for smaller screens) -->
            <div class="md:hidden flex items-center space-x-1">
              <button @click="onEdit(appointment.id)" class="inline-flex items-center justify-center w-8 h-8 text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-full border border-blue-200 hover:border-blue-300 transition-all duration-150" title="Edit appointment">
                <font-awesome-icon :icon="['fas', 'edit']" class="text-xs" />
              </button>

              <button @click="onInvoice(appointment.id)" class="inline-flex items-center justify-center w-8 h-8 text-green-600 bg-green-50 hover:bg-green-100 rounded-full border border-green-200 hover:border-green-300 transition-all duration-150" title="Create invoice">
                <font-awesome-icon :icon="['fas', 'file-invoice']" class="text-xs" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-6 flex items-center justify-between">
      <div class="text-sm text-gray-700">Showing {{ appointments.length }} of {{ count || appointments.length }} appointments</div>
      <div class="flex items-center space-x-2">
        <button @click="previousPage" :disabled="isFirstPage" class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150">
          <font-awesome-icon :icon="['fas', 'chevron-left']" class="mr-1" />
          Previous
        </button>
        <span class="text-sm text-gray-600">Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="isLastPage" class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150">
          Next
          <font-awesome-icon :icon="['fas', 'chevron-right']" class="ml-1" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

import { ArrowPathIcon } from '@heroicons/vue/24/outline';

export default {
  props: {
    client: {
      type: Object,
      required: null,
    },
  },
  components: {
    ArrowPathIcon,
  },
  data() {
    return {
      loading: false,

      count: null,
      currentPage: 1,
      pageSize: 5,
      totalPages: 1,
      sortBy: 'start',
      sortOrder: 'desc',

      appointments: [],

      filters: {},
    };
  },
  computed: {
    sorting() {
      return this.sortOrder === 'asc' ? this.sortBy : `-${this.sortBy}`; // DRF ordering syntax
    },
    isFirstPage() {
      return this.currentPage === 1;
    },
    isLastPage() {
      return this.currentPage === this.totalPages;
    },
  },
  methods: {
    ...mapActions('clients', ['filterClientAppointments']),
    itemProvider() {
      this.loading = true;
      this.filterClientAppointments({
        client_id: this.client.id,
        page: this.currentPage,
        page_size: this.pageSize,
        ordering: this.sorting,
      })
        .then((response) => {
          this.appointments = response.results;
          this.totalPages = Math.ceil(response.count / this.pageSize);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    previousPage() {
      this.currentPage = this.currentPage - 1;
      this.itemProvider();
    },
    nextPage() {
      this.currentPage = this.currentPage + 1;
      this.itemProvider();
    },
    sort(column) {
      if (this.sortBy === column) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'; // Toggle order
      } else {
        this.sortBy = column;
        this.sortOrder = 'asc';
      }
      this.itemProvider();
    },
    onEdit(id) {
      //navigate to appointment details view
    },
    onInvoice(id) {
      //navigate to create invoice from appointment view
    },
  },
  mounted() {
    this.itemProvider();
  },
  async beforeRouteEnter(to, from, next) {
    return next();
  },
};
</script>
