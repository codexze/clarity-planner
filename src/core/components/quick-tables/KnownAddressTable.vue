<template>
  <div>
    <!-- Header Section -->
    <div class="space-y-4">
      <div class="flex items-center justify-between mb-2">
        <div>
          <p class="text-sm text-gray-600">View all addresses associated with this client, including their appointment history and status.</p>
        </div>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ addresses.length }} {{ addresses.length === 1 ? 'address' : 'addresses' }}</span>
      </div>

      <!-- Search Section -->
      <div class="relative max-w-md mb-2">
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <font-awesome-icon icon="search" class="text-gray-400" />
        </div>
        <input type="text" name="address_search" id="address_search" v-model="filters.address" @keyup.enter="itemProvider" class="block w-full pl-10 pr-3 py-2.5 text-sm text-gray-900 placeholder:text-gray-400 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-150" placeholder="Search by Address" />
      </div>
    </div>
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && addresses.length === 0" class="text-center py-12">
      <font-awesome-icon icon="map-marker-alt" class="text-4xl text-gray-300 mb-4" />
      <h5 class="text-lg font-medium text-gray-900 mb-2">No Addresses Found</h5>
      <p class="text-gray-500">This client doesn't have any addresses yet.</p>
    </div>

    <!-- Address Cards -->
    <div v-else class="space-y-4">
      <div v-for="address in addresses" :key="address.id" class="group relative bg-gray-50 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 p-4">
        <div class="flex items-start justify-between">
          <!-- Main Content -->
          <div class="flex items-start space-x-4 flex-1">
            <!-- Address Icon and Status -->
            <div class="flex-shrink-0">
              <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors duration-200">
                <font-awesome-icon icon="map-marker-alt" class="text-blue-600" />
              </div>
              <div class="mt-2 flex justify-center">
                <span v-if="address.is_active" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <font-awesome-icon icon="check-circle" class="mr-1" />
                  Active
                </span>
                <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  <font-awesome-icon icon="times-circle" class="mr-1" />
                  Inactive
                </span>
              </div>
            </div>

            <!-- Address Details -->
            <div class="flex-1 min-w-0">
              <!-- Address Info -->
              <div class="mb-3">
                <h5 class="text-base font-semibold text-gray-900 group-hover:text-blue-900">
                  {{ address.address }}
                </h5>
                <p class="text-sm text-gray-500 group-hover:text-blue-700 mt-1">Address ID: {{ address.id }}</p>
              </div>

              <!-- Appointment Status -->
              <div class="bg-white rounded-lg p-3 border border-gray-100">
                <div v-if="address.last_appointment_date" class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center">
                    <font-awesome-icon icon="history" class="text-red-600 text-sm" />
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">Last Appointment</p>
                    <p class="text-xs text-gray-500">{{ address.last_appointment_date ? toLocaleDate(address.last_appointment_date) : 'Date not available' }}</p>
                  </div>
                </div>
                <div v-else-if="address.next_appointment_date" class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                    <font-awesome-icon icon="calendar" class="text-green-600 text-sm" />
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">Next Appointment</p>
                    <p class="text-xs text-gray-500">{{ address.next_appointment_date ? toLocaleDate(address.next_appointment_date) : 'Date not available' }}</p>
                  </div>
                </div>
                <div v-else class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                    <font-awesome-icon icon="calendar-xmark" class="text-gray-400 text-sm" />
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-500">No Appointments</p>
                    <p class="text-xs text-gray-400">No scheduled appointments for this address</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex-shrink-0 ml-4">
            <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <!-- Activate/Deactivate Button -->
              <button v-if="address.is_active" @click="onDeactivate(address)" class="inline-flex items-center px-3 py-2 text-xs font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-lg border border-red-200 hover:border-red-300 transition-all duration-150 hover:shadow-sm" title="Deactivate address">
                <font-awesome-icon :icon="['fas', 'ban']" class="mr-1.5" />
                Deactivate
              </button>

              <button v-else @click="onActivate(address)" class="inline-flex items-center px-3 py-2 text-xs font-medium text-green-700 bg-green-50 hover:bg-green-100 rounded-lg border border-green-200 hover:border-green-300 transition-all duration-150 hover:shadow-sm" title="Activate address">
                <font-awesome-icon :icon="['fas', 'check']" class="mr-1.5" />
                Activate
              </button>
            </div>

            <!-- Mobile/Always Visible Actions (for smaller screens) -->
            <div class="md:hidden flex items-center">
              <button v-if="address.is_active" @click="onDeactivate(address)" class="inline-flex items-center justify-center w-8 h-8 text-red-600 bg-red-50 hover:bg-red-100 rounded-full border border-red-200 hover:border-red-300 transition-all duration-150" title="Deactivate address">
                <font-awesome-icon :icon="['fas', 'ban']" class="text-xs" />
              </button>

              <button v-else @click="onActivate(address)" class="inline-flex items-center justify-center w-8 h-8 text-green-600 bg-green-50 hover:bg-green-100 rounded-full border border-green-200 hover:border-green-300 transition-all duration-150" title="Activate address">
                <font-awesome-icon :icon="['fas', 'check']" class="text-xs" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-6 flex items-center justify-between">
      <div class="text-sm text-gray-700">Showing {{ addresses.length }} of {{ count || addresses.length }} addresses</div>
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
      sortBy: 'id',
      sortOrder: 'desc',

      addresses: [],

      filters: { address: '', is_active: null },
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
    ...mapActions('clients', ['filterKnownAddresses', 'updateKnownAddress']),
    itemProvider() {
      this.loading = true;
      this.filterKnownAddresses({
        client_id: this.client.id,
        page: this.currentPage,
        page_size: this.pageSize,
        ordering: this.sorting,
        address: this.filters.address || undefined,
        is_active: this.filters.is_active !== null ? this.filters.is_active : undefined,
      })
        .then((response) => {
          this.addresses = response.results;
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
    onActivate(address) {
      // Add confirmation for better UX

      const payload = { id: address.id, is_active: true, consistency_token: address.consistency_token };
      this.updateKnownAddress(payload)
        .then(() => {
          this.toastSuccess('Address activated successfully!');
          this.itemProvider();
        })
        .catch((errors) => {
          this.formatErrors(errors.response);
        });
    },
    onDeactivate(address) {
      // Add confirmation for better UX

      const payload = { id: address.id, is_active: false, consistency_token: address.consistency_token };
      this.updateKnownAddress(payload)
        .then(() => {
          this.toastSuccess('Address deactivated successfully!');
          this.itemProvider();
        })
        .catch((errors) => {
          this.formatErrors(errors.response);
        });
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
