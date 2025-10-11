<template>
  <div class="p-8">
    <!-- Header Section -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Client Management</h1>
      <p class="mt-2 text-gray-600">Manage your clients and their details</p>
    </div>

    <div class="relative overflow-x-auto p-4 bg-white shadow-md sm:rounded-lg">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <router-link to="/clients/new" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150">
            <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
            New Client
          </router-link>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-5">
        <div>
          <label for="name-filter" class="block text-sm font-medium text-gray-700">Client Name</label>
          <div class="mt-1">
            <input type="text" id="name-filter" v-model="filters.name" @input="debouncedFilter" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150" placeholder="Search by name..." />
          </div>
        </div>
        <div>
          <label for="email-filter" class="block text-sm font-medium text-gray-700">Email</label>
          <div class="mt-1">
            <input type="email" id="email-filter" v-model="filters.email" @input="debouncedFilter" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150" placeholder="Search by email..." />
          </div>
        </div>
        <div>
          <label for="mobile-filter" class="block text-sm font-medium text-gray-700">Phone</label>
          <div class="mt-1">
            <input type="text" id="mobile-filter" v-model="filters.mobile" @input="debouncedFilter" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150" placeholder="Search by phone..." />
          </div>
        </div>
        <div>
          <label for="status-filter" class="block text-sm font-medium text-gray-700">Status</label>
          <div class="mt-1">
            <select id="status-filter" v-model="filters.is_active" @change="itemProvider" class="block w-full rounded-md border border-gray-200 py-2 px-3 text-sm text-gray-600 hover:border-gray-300 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-colors duration-150">
              <option :value="null">All Statuses</option>
              <option :value="true">Available</option>
              <option :value="false">Unavailable</option>
            </select>
          </div>
        </div>
        <div class="flex items-end">
          <button @click="clearFilters" class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200">Clear Filters</button>
        </div>
      </div>
    </div>

    <!-- Clients Table -->
    <div class="mt-6 relative overflow-x-auto bg-white shadow-md sm:rounded-lg">
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <div v-else>
        <table class="w-full text-sm text-left text-gray-500">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 cursor-pointer" @click="sort('surname')">
                <div class="flex items-center">
                  Client Name
                  <font-awesome-icon :icon="['fas', 'sort']" class="ml-1 text-gray-400" />
                </div>
              </th>
              <th scope="col" class="px-6 py-3">Date of Birth</th>
              <th scope="col" class="px-6 py-3">Email</th>
              <th scope="col" class="px-6 py-3">Phone</th>
              <th scope="col" class="px-6 py-3 cursor-pointer" @click="sort('is_active')">
                <div class="flex items-center">
                  Status
                  <font-awesome-icon :icon="['fas', 'sort']" class="ml-1 text-gray-400" />
                </div>
              </th>
              <th scope="col" class="px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="client in clients" :key="client.id" class="bg-white border-b border-gray-200 hover:bg-gray-50">
              <td class="px-6 py-4 font-medium text-gray-900">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                    <font-awesome-icon :icon="['fas', client.gender === 'MALE' ? 'mars' : client.gender === 'FEMALE' ? 'venus' : 'venus-mars']" class="text-blue-600 text-sm" />
                  </div>
                  <div>
                    <p class="font-medium">{{ client.display }}</p>
                    <div class="flex items-center space-x-1">
                      <font-awesome-icon v-if="client.company_details" :icon="['fas', 'building']" class="text-gray-400 text-xs" />
                      <span v-if="client.company_details" class="text-xs text-gray-500">{{ client.company_details.name }}</span>
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span>{{ toLocaleDate(client.date_of_birth) }}</span>
              </td>
              <td class="px-6 py-4">
                <span v-if="client.email" class="text-blue-600 hover:underline">
                  <a :href="`mailto:${client.email}`">{{ client.email }}</a>
                </span>
                <span v-else class="text-gray-400">—</span>
              </td>
              <td class="px-6 py-4">
                <span v-if="client.mobile">{{ client.mobile }}</span>
                <span v-else class="text-gray-400">—</span>
              </td>
              <td class="px-6 py-4">
                <span :class="client.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                  {{ client.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center space-x-2">
                  <router-link :to="`/clients/${client.id}/view`" class="text-blue-600 hover:text-blue-800">
                    <font-awesome-icon :icon="['fas', 'eye']" />
                  </router-link>
                  <button @click="toggleStatus(client)" :class="client.is_active ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'">
                    <font-awesome-icon :icon="client.is_active ? ['fas', 'ban'] : ['fas', 'check']" />
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="clients.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                <font-awesome-icon :icon="['fas', 'users']" class="text-4xl text-gray-300 mb-2" />
                <p>No clients found</p>
                <router-link to="/clients/new" class="text-blue-600 hover:text-blue-800">Create your first client</router-link>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-between px-6 py-3 bg-gray-50">
          <div class="text-sm text-gray-700">Showing {{ clients.length }} of {{ count }} clients</div>
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
import _ from 'lodash';

export default {
  data() {
    return {
      loading: false,
      count: null,
      currentPage: 1,
      pageSize: 10,
      totalPages: 1,
      sortBy: 'surname',
      filters: {
        name: null,
        email: null,
        mobile: null,
        is_active: null,
      },
      sortOrder: 'asc',
      clients: [],
      debouncedFilter: null,
    };
  },
  computed: {
    ...mapState('clients', {
      genders: (state) => state.genders,
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
    ...mapActions('clients', ['filterClients', 'updateClientById']),
    itemProvider() {
      this.loading = true;
      this.filterClients({
        page: this.currentPage,
        page_size: this.pageSize,
        ordering: this.sorting,
        name: this.filters.name || undefined,
        email: this.filters.email || undefined,
        mobile: this.filters.mobile || undefined,
        is_active: this.filters.is_active !== null ? this.filters.is_active : undefined,
      })
        .then((response) => {
          this.clients = response.results || response;
          this.count = response.count || response.length;
          this.totalPages = Math.ceil(this.count / this.pageSize);
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
        name: null,
        email: null,
        mobile: null,
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
    async toggleStatus(client) {
      try {
        await this.updateClientById({
          id: client.id,
          is_active: !client.is_active,
        });
        this.toastSuccess(`Client "${client.display}" status updated successfully!`);
        this.itemProvider();
      } catch (error) {
        this.toastError('Failed to update client status');
      }
    },
  },
  created() {
    this.debouncedFilter = _.debounce(() => {
      this.currentPage = 1;
      this.itemProvider();
    }, 500);
  },
  mounted() {
    this.itemProvider();
  },
};
</script>
