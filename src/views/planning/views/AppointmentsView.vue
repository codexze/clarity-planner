<template>
  <div class="p-8">
    <!-- Header Section -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Appointment Management</h1>
      <p class="mt-2 text-gray-600">Manage your appointments and scheduling</p>
    </div>

    <div class="relative overflow-x-auto p-4 bg-white shadow-md sm:rounded-lg">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <!-- <router-link :to="`/planning/${username}/appointments/new`" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150">
            <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
            New Appointment
          </router-link> -->
        </div>
      </div>

      <!-- Filters Section -->
      <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-4">
        <div>
          <label for="date-filter" class="block text-sm font-medium text-gray-700">Appointment Date</label>
          <div class="mt-1">
            <input type="text" id="date-filter" v-model="filters.appointment_date" @input="debouncedFilter" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150" placeholder="Search by date..." />
          </div>
        </div>
        <div>
          <label for="client-filter" class="block text-sm font-medium text-gray-700">Client Name</label>
          <div class="mt-1">
            <input type="text" id="client-filter" v-model="filters.client__name" @input="debouncedFilter" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150" placeholder="Search by client..." />
          </div>
        </div>
        <div>
          <label for="service-filter" class="block text-sm font-medium text-gray-700">Service Name</label>
          <div class="mt-1">
            <input type="text" id="service-filter" v-model="filters.service__name" @input="debouncedFilter" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150" placeholder="Search by service..." />
          </div>
        </div>
        <div class="flex items-end">
          <button @click="clearFilters" class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200">Clear Filters</button>
        </div>
      </div>
    </div>

    <!-- Appointments Table -->
    <div class="mt-6 relative overflow-x-auto bg-white shadow-md sm:rounded-lg">
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <div v-else>
        <table class="w-full text-sm text-left text-gray-500">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 cursor-pointer" @click="sort('appointment_date')">
                <div class="flex items-center">
                  Appointment Date
                  <font-awesome-icon :icon="['fas', 'sort']" class="ml-1 text-gray-400" />
                </div>
              </th>
              <th scope="col" class="px-6 py-3">Client</th>
              <th scope="col" class="px-6 py-3">Service</th>
              <th scope="col" class="px-6 py-3">Assigned to</th>
              <th scope="col" class="px-6 py-3">Location</th>
              <th scope="col" class="px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appointment in appointments" :key="appointment.id" class="bg-white border-b border-gray-200 hover:bg-gray-50">
              <td class="px-6 py-4 font-medium text-gray-900">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                    <font-awesome-icon :icon="['fas', 'calendar-check']" class="text-blue-600 text-sm" />
                  </div>
                  <div>
                    <p class="font-medium">{{ appointment.appointment_date ? toLocaleDate(appointment.appointment_date) : 'n/a' }}</p>
                    <span v-if="appointment.is_past" class="text-xs text-red-600">{{ appointment.start_time }} - {{ appointment.end_time }}</span>
                    <span v-else-if="appointment.is_future" class="text-xs text-green-600">{{ appointment.start_time }} - {{ appointment.end_time }}</span>
                    <span v-else class="text-xs text-amber-600">{{ appointment.start_time }} - {{ appointment.end_time }}</span>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'user']" class="mr-2 text-gray-400" />
                  <span>{{ appointment.client_name }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <div>
                  <p class="font-medium">{{ appointment.service_name }}</p>
                  <p class="text-xs text-gray-500">{{ appointment.service?.time_display || '' }}</p>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'user-tie']" class="mr-2 text-gray-400" />
                  <span>{{ appointment.employee_name }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <span v-if="appointment.is_onsite" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800">
                  <font-awesome-icon :icon="['fas', 'location-dot']" class="mr-1" />
                  On-site
                </span>
                <span v-else class="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                  <font-awesome-icon :icon="['fas', 'building']" class="mr-1" />
                  In-office
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center space-x-2">
                  <router-link :to="`/planning/${username}/appointments/${appointment.id}/view`" class="text-blue-600 hover:text-blue-800">
                    <font-awesome-icon :icon="['fas', 'eye']" />
                  </router-link>
                </div>
              </td>
            </tr>
            <tr v-if="appointments.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                <font-awesome-icon :icon="['fas', 'calendar']" class="text-4xl text-gray-300 mb-2" />
                <p>No appointments found</p>
                <router-link :to="`/planning/${username}/appointments/new`" class="text-blue-600 hover:text-blue-800">Create your first appointment</router-link>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-between px-6 py-3 bg-gray-50">
          <div class="text-sm text-gray-700">Showing {{ appointments.length }} of {{ count }} appointments</div>
          <div class="flex space-x-2">
            <button @click="previousPage" :disabled="isFirstPage" class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:from-gray-400 disabled:to-gray-500">Previous</button>
            <span class="px-3 py-1 text-sm">{{ currentPage }} / {{ totalPages }}</span>
            <button @click="nextPage" :disabled="isLastPage" class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:from-gray-400 disabled:to-gray-500">Next</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

import { MagnifyingGlassIcon, ArrowPathIcon, ChevronUpDownIcon } from '@heroicons/vue/24/solid';

export default {
  components: {
    MagnifyingGlassIcon,
    ArrowPathIcon,
    ChevronUpDownIcon,
  },
  data() {
    return {
      loading: false,
      username: null,

      count: null,
      currentPage: 1,
      pageSize: 5,
      totalPages: 1,
      sortBy: 'appointment_date',
      sortOrder: 'desc', // asc, desc
      selectedType: '',
      appointments: [],

      debouncedFilter: null,

      filters: {
        appointment_date: null,
        client__name: null,
        service__name: null,
      },
    };
  },
  computed: {
    ...mapState('planning', {
      settings: (state) => state.settings,
      employee: (state) => state.employee,
      employees: (state) => state.employees,
    }),
    sorting() {
      return this.sortOrder === 'asc' ? this.sortBy : `-${this.sortBy}`; // DRF sorting syntax
    },
    isFirstPage() {
      return this.currentPage === 1;
    },
    isLastPage() {
      return this.currentPage === this.totalPages;
    },
  },
  methods: {
    ...mapActions('planning', ['filterAppointments']),
    itemProvider() {
      this.loading = true;
      this.filterAppointments({
        page: this.currentPage,
        page_size: this.pageSize,
        ordering: this.sorting,
        appointment_date: this.filters.appointment_date || undefined,
        client__name: this.filters.client__name || undefined,
        service__name: this.filters.service__name || undefined,
      })
        .then((response) => {
          this.appointments = response.results;
          this.totalPages = Math.ceil(response.count / this.pageSize);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    sort(field) {
      if (this.sortBy === field) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortBy = field;
        this.sortOrder = 'asc';
      }
      this.currentPage = 1;
      this.itemProvider();
    },
    clearFilters() {
      this.filters = {
        appointment_date: null,
        client__name: null,
        service__name: null,
      };
      this.currentPage = 1;
      this.itemProvider();
    },
    nextPage() {
      if (!this.isLastPage) {
        this.currentPage++;
        this.itemProvider();
      }
    },
    previousPage() {
      if (!this.isFirstPage) {
        this.currentPage--;
        this.itemProvider();
      }
    },
  },
  mounted() {
    this.itemProvider();
  },
  created() {
    this.debouncedFilter = _.debounce(() => {
      this.currentPage = 1;
      this.itemProvider();
    }, 500);
  },
  async beforeRouteEnter(to, from, next) {
    return next((vm) => {
      vm.username = to.params.username;
    });
  },
  beforeDestroy() {
    this.debouncedFilter.cancel();
  },
};
</script>
