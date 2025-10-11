<template>
  <div class="bg-white">
    <!-- Search and Filter Section -->
    <div class="p-4 border-b border-gray-200 bg-gray-50">
      <div class="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-sm font-medium text-gray-900 flex items-center">
            <font-awesome-icon :icon="['fas', 'search']" class="mr-2 text-gray-400" />
            Find Your Client
          </h4>
          <button @click="onCreateNew()" class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 hover:border-blue-300 transition-colors duration-150">
            <font-awesome-icon :icon="['fas', 'plus']" class="mr-1.5" />
            New Client
          </button>
        </div>
        <p class="text-xs text-gray-600 flex items-center">
          <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1" />
          Use the search and filters below to quickly find and select your client
        </p>
      </div>

      <!-- Search Filters Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div class="relative">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <font-awesome-icon :icon="['fas', 'user']" class="text-gray-400 text-sm" />
          </div>
          <input type="text" v-model="searchQuery" @input="debouncedSearch" class="block w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-9 pr-4 text-sm text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Search by name..." />
        </div>
        <div class="relative">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <font-awesome-icon :icon="['fas', 'calendar']" class="text-gray-400 text-sm" />
          </div>
          <input type="text" v-model="filters.date_of_birth" @input="debouncedSearch" class="block w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-9 pr-4 text-sm text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Birth date..." />
        </div>
        <div class="relative">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <font-awesome-icon :icon="['fas', 'phone']" class="text-gray-400 text-sm" />
          </div>
          <input type="text" v-model="filters.mobile" @input="debouncedSearch" class="block w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-9 pr-4 text-sm text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Phone number..." />
        </div>
      </div>

      <!-- Results Summary -->
      <div class="mt-3 flex items-center justify-between text-xs text-gray-600">
        <span v-if="!loading" class="flex items-center">
          <font-awesome-icon :icon="['fas', 'users']" class="mr-1" />
          {{ clients.length }} of {{ count || 0 }} clients
        </span>
        <span v-if="hasActiveFilters" class="flex items-center text-blue-600">
          <font-awesome-icon :icon="['fas', 'filter']" class="mr-1" />
          Filtered results
          <button @click="clearFilters" class="ml-2 text-blue-600 hover:text-blue-800 underline">Clear</button>
        </span>
      </div>
    </div>

    <!-- Client List -->
    <div class="divide-y divide-gray-200 max-h-96 overflow-y-auto">
      <!-- Loading State -->
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-flex items-center">
          <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin text-blue-600 text-xl mr-3" />
          <span class="text-gray-600">Searching clients...</span>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="clients.length === 0" class="p-8 text-center">
        <div class="flex flex-col items-center space-y-3">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
            <font-awesome-icon :icon="['fas', 'users']" class="text-2xl text-gray-400" />
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-900">No clients found</h3>
            <p class="text-xs text-gray-500 mt-1">
              {{ hasActiveFilters ? 'Try adjusting your search criteria' : 'Get started by adding your first client' }}
            </p>
          </div>
          <button @click="onCreateNew()" class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-150">
            <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
            Add First Client
          </button>
        </div>
      </div>

      <!-- Client Items -->
      <div v-else>
        <div v-for="client in clients" :key="client.id" @click="onSelect(client)" class="group p-4 hover:bg-blue-50 cursor-pointer transition-all duration-150 border-l-4 border-transparent hover:border-blue-500">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4 flex-1 min-w-0">
              <!-- Avatar -->
              <div class="w-12 h-12 rounded-full flex items-center justify-center transition-colors duration-150" :class="client.gender === 'MALE' ? 'bg-blue-100 group-hover:bg-blue-200' : client.gender === 'FEMALE' ? 'bg-pink-100 group-hover:bg-pink-200' : 'bg-purple-100 group-hover:bg-purple-200'">
                <font-awesome-icon :icon="['fas', client.gender === 'MALE' ? 'mars' : client.gender === 'FEMALE' ? 'venus' : 'venus-mars']" :class="client.gender === 'MALE' ? 'text-blue-600' : client.gender === 'FEMALE' ? 'text-pink-600' : 'text-purple-600'" />
              </div>

              <!-- Client Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2 mb-1">
                  <h3 class="text-sm font-semibold text-gray-900 truncate group-hover:text-blue-900 transition-colors duration-150">
                    {{ client.display }}
                  </h3>
                  <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">ID: {{ client.id }}</span>
                </div>

                <!-- Client Details -->
                <div class="flex items-center space-x-4 text-xs text-gray-600">
                  <div v-if="client.date_of_birth" class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'calendar']" class="mr-1.5 text-gray-400" />
                    <span>{{ toLocaleDate(client.date_of_birth) }}</span>
                  </div>
                  <div v-if="client.mobile" class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'phone']" class="mr-1.5 text-gray-400" />
                    <span>{{ client.mobile }}</span>
                  </div>
                  <div v-if="client.email" class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'envelope']" class="mr-1.5 text-gray-400" />
                    <span class="truncate">{{ client.email }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between px-4 py-3 bg-gray-50 border-t border-gray-200">
      <div class="text-sm text-gray-700">Showing {{ clients.length }} of {{ count }} clients</div>
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
import store from '@/store';
import { mapState, mapActions } from 'vuex';
import { debounce } from 'lodash';

export default {
  name: 'QuickClientTable',
  data() {
    return {
      loading: false,
      searchQuery: '',
      count: null,
      currentPage: 1,
      pageSize: 10,
      totalPages: 1,
      sortBy: 'surname',
      sortOrder: 'asc',
      clients: [],
      filters: {
        date_of_birth: '',
        email: '',
        mobile: '',
      },
    };
  },
  computed: {
    ...mapState('clients', {
      genders: (state) => state.genders,
    }),
    sorting() {
      return this.sortOrder === 'asc' ? this.sortBy : `-${this.sortBy}`; // DRF ordering syntax
    },
    isFirstPage() {
      return this.currentPage === 1;
    },
    isLastPage() {
      return this.currentPage >= this.totalPages;
    },
    hasActiveFilters() {
      return this.searchQuery || this.filters.date_of_birth || this.filters.mobile || this.filters.email;
    },
  },
  watch: {
    searchQuery() {
      this.debouncedSearch();
    },
    'filters.date_of_birth'() {
      this.currentPage = 1;
      this.itemProvider();
    },
    'filters.mobile'() {
      this.currentPage = 1;
      this.itemProvider();
    },
    'filters.email'() {
      this.currentPage = 1;
      this.itemProvider();
    },
  },
  methods: {
    ...mapActions('clients', ['filterClients']),
    itemProvider() {
      this.loading = true;
      this.filterClients({
        page: this.currentPage,
        page_size: this.pageSize,
        ordering: this.sorting,
        search: this.searchQuery || undefined,
        name: this.searchQuery || undefined, // Keep name for backward compatibility
        email: this.filters.email || undefined,
        mobile: this.filters.mobile || undefined,
        date_of_birth: this.filters.date_of_birth || undefined,
      })
        .then((response) => {
          this.clients = response.results;
          this.count = response.count;
          this.totalPages = Math.ceil(response.count / this.pageSize);
        })
        .finally(() => {
          setTimeout(() => {
            this.loading = false;
          }, 300);
        });
    },
    debouncedSearch: debounce(function () {
      this.currentPage = 1;
      this.itemProvider();
    }, 300),
    clearFilters() {
      this.searchQuery = '';
      this.filters = {
        date_of_birth: '',
        mobile: '',
        email: '',
      };
      this.currentPage = 1;
      this.itemProvider();
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage = this.currentPage - 1;
        this.itemProvider();
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage = this.currentPage + 1;
        this.itemProvider();
      }
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
    onSelect(client) {
      this.$emit('selected-client', client);
    },
  },
  mounted() {
    this.itemProvider();
  },
  async beforeRouteEnter(to, from, next) {
    const genders = await store.dispatch('clients/getGenders');
    return next();
  },
};
</script>
