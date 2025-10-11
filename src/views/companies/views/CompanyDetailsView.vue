<template>
  <div class="relative overflow-x-auto p-4 bg-gray-50">
    <div class="grid grid-cols-1 gap-x-6 gap-y-6 sm:grid-cols-6">
      <div class="sm:col-span-3 sm:col-start-1 space-y-6">
        <!-- Company Information Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'building']" class="mr-3 text-blue-600" />
              Company Information
            </h3>
            <p class="mt-1 text-sm text-gray-600">Manage company details and contact information</p>
          </div>

          <div class="p-6 space-y-6">
            <!-- Company Name -->
            <div class="space-y-2">
              <label for="name" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'building']" class="mr-2 text-gray-400" />
                Company Name
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'building']" class="text-gray-400" />
                </div>
                <input type="text" name="name" id="name" v-model="form.name" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter company name" />
              </div>
            </div>

            <!-- Address -->
            <div class="space-y-2">
              <label for="address" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2 text-gray-400" />
                Address
              </label>
              <div class="relative">
                <textarea name="address" id="address" v-model="form.address" rows="3" class="block w-full rounded-lg border border-gray-300 bg-white py-3 px-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 resize-none" placeholder="Enter company address"></textarea>
              </div>
            </div>

            <!-- Email -->
            <div class="space-y-2">
              <label for="email" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'envelope']" class="mr-2 text-gray-400" />
                Email
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'envelope']" class="text-gray-400" />
                </div>
                <input type="email" name="email" id="email" v-model="form.email" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="company@example.com" />
              </div>
            </div>

            <!-- Phone Number -->
            <div class="space-y-2">
              <label for="phone" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'phone']" class="mr-2 text-gray-400" />
                Phone Number
              </label>
              <div class="relative flex rounded-lg shadow-sm">
                <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">+</span>
                <input type="text" name="phone" id="phone" v-mask="['### ###-####', '## # ####-####', '# (###) ###-####']" v-model="form.phone" class="block w-full rounded-none rounded-r-lg border border-gray-300 py-3 pl-3 pr-3 text-sm text-gray-900 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="597 000-0000" />
              </div>
            </div>

            <!-- Website -->
            <div class="space-y-2">
              <label for="website" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'globe']" class="mr-2 text-gray-400" />
                Website
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'globe']" class="text-gray-400" />
                </div>
                <input type="url" name="website" id="website" v-model="form.website" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="https://www.company.com" />
              </div>
            </div>

            <!-- Active Status -->
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center transition-colors duration-200" :class="form.is_active ? 'bg-green-100' : 'bg-gray-100'">
                    <font-awesome-icon :icon="['fas', form.is_active ? 'check-circle' : 'pause-circle']" :class="form.is_active ? 'text-green-600' : 'text-gray-600'" />
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">
                      {{ form.is_active ? 'Active Company' : 'Inactive Company' }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ form.is_active ? 'Company is active and visible in the system' : 'Company is inactive and hidden from listings' }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center">
                  <input id="available" type="checkbox" v-model="form.is_active" class="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 transition-colors duration-200" />
                  <label for="available" class="ml-3 text-sm font-medium text-gray-700">Active</label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-6 flex items-center justify-between">
          <div class="text-sm text-gray-600">
            <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1.5 text-blue-500" />
            Fields marked with
            <span class="text-red-500">*</span>
            are required
          </div>
          <!-- Form Actions -->
          <div class="flex items-center space-x-4">
            <button @click="submit" class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 space-x-2">
              <font-awesome-icon :icon="['fas', 'save']" />
              <span>Save Changes</span>
            </button>
            <button @click="cancel" class="px-6 py-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-150 flex items-center space-x-2">
              <font-awesome-icon :icon="['fas', 'times']" />
              <span>Cancel</span>
            </button>
          </div>
        </div>
      </div>

      <div class="sm:col-span-3 sm:col-start-4">
        <!-- Company Details Tabs Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'chart-bar']" class="mr-3 text-blue-600" />
              Company Details
            </h3>
            <p class="mt-1 text-sm text-gray-600">View clients and statistics for this company</p>
          </div>

          <div class="px-6 py-4 border-b border-gray-100">
            <nav class="-mb-px flex space-x-8" aria-label="Tabs">
              <button v-for="tab in tabs" :key="tab.name" @click="currentTab = tab.name" :class="[currentTab === tab.name ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'whitespace-nowrap border-b-2 py-2 px-1 text-sm font-medium transition-colors duration-150']">
                {{ tab.label }}
              </button>
            </nav>
          </div>

          <div class="p-6">
            <!-- Clients Tab -->
            <div v-if="currentTab === 'clients'">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <h4 class="text-base font-medium text-gray-900">Associated Clients</h4>
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ companyClients.length }} {{ companyClients.length === 1 ? 'client' : 'clients' }}</span>
                </div>

                <div v-if="loadingClients" class="flex justify-center py-12">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>

                <div v-else-if="companyClients.length === 0" class="text-center py-12">
                  <font-awesome-icon :icon="['fas', 'users']" class="text-4xl text-gray-300 mb-4" />
                  <h5 class="text-lg font-medium text-gray-900 mb-2">No Associated Clients</h5>
                  <p class="text-gray-500">This company doesn't have any clients yet.</p>
                </div>

                <div v-else class="grid grid-cols-1 gap-3">
                  <div v-for="client in companyClients" :key="client.id" class="group relative flex items-center justify-between p-4 bg-gray-50 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200">
                    <div class="flex items-center space-x-3">
                      <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors duration-200">
                        <font-awesome-icon :icon="['fas', 'user']" class="text-blue-600" />
                      </div>
                      <div>
                        <p class="font-medium text-gray-900 group-hover:text-blue-900">{{ client.display }}</p>
                        <p class="text-sm text-gray-500 group-hover:text-blue-700">{{ client.email || 'No email provided' }}</p>
                      </div>
                    </div>
                    <router-link :to="`/clients/${client.id}/view`" class="inline-flex items-center px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-100 rounded-lg hover:bg-blue-200 transition-colors duration-150 group-hover:bg-blue-600 group-hover:text-white">
                      <span class="mr-1">View</span>
                      <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-xs" />
                    </router-link>
                  </div>
                </div>
              </div>
            </div>

            <!-- Statistics Tab -->
            <div v-if="currentTab === 'statistics'">
              <div class="space-y-6">
                <h4 class="text-base font-medium text-gray-900">Company Statistics</h4>

                <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                  <!-- Total Clients -->
                  <div class="bg-gray-50 border border-gray-200 rounded-xl p-5">
                    <div class="flex items-center">
                      <div class="flex-shrink-0">
                        <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                          <font-awesome-icon :icon="['fas', 'users']" class="text-blue-600" />
                        </div>
                      </div>
                      <div class="ml-4 flex-1">
                        <dt class="text-sm font-medium text-gray-500">Total Clients</dt>
                        <dd class="text-2xl font-semibold text-gray-900">{{ companyClients.length }}</dd>
                      </div>
                    </div>
                  </div>

                  <!-- Active Clients -->
                  <div class="bg-gray-50 border border-gray-200 rounded-xl p-5">
                    <div class="flex items-center">
                      <div class="flex-shrink-0">
                        <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                          <font-awesome-icon :icon="['fas', 'user-check']" class="text-green-600" />
                        </div>
                      </div>
                      <div class="ml-4 flex-1">
                        <dt class="text-sm font-medium text-gray-500">Active Clients</dt>
                        <dd class="text-2xl font-semibold text-gray-900">{{ activeClientsCount }}</dd>
                      </div>
                    </div>
                  </div>

                  <!-- Company Status -->
                  <div class="bg-gray-50 border border-gray-200 rounded-xl p-5">
                    <div class="flex items-center">
                      <div class="flex-shrink-0">
                        <div class="w-10 h-10 rounded-full flex items-center justify-center" :class="company?.is_active ? 'bg-green-100' : 'bg-red-100'">
                          <font-awesome-icon :icon="['fas', 'building']" :class="company?.is_active ? 'text-green-600' : 'text-red-600'" />
                        </div>
                      </div>
                      <div class="ml-4 flex-1">
                        <dt class="text-sm font-medium text-gray-500">Company Status</dt>
                        <dd :class="company?.is_active ? 'text-green-600' : 'text-red-600'" class="text-2xl font-semibold">
                          {{ company?.is_active ? 'Active' : 'Inactive' }}
                        </dd>
                      </div>
                    </div>
                  </div>
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
import store from '@/store';
import Form from '@/core/utils/Form';
import { mapState, mapActions } from 'vuex';

export default {
  data() {
    return {
      currentTab: 'clients',
      tabs: [
        { name: 'clients', label: 'Clients' },
        { name: 'statistics', label: 'Statistics' },
      ],
      companyClients: [],
      loadingClients: false,
      form: new Form({
        id: null,
        consistency_token: null,
        name: null,
        address: null,
        email: null,
        phone: null,
        website: null,
        is_active: true,
      }),
    };
  },
  computed: {
    ...mapState('companies', {
      company: (state) => state.company,
    }),
    activeClientsCount() {
      return this.companyClients.filter((client) => client.is_active).length;
    },
  },
  watch: {
    company: {
      immediate: true,
      handler(val) {
        if (val) {
          this.form.populate(val);
          this.loadCompanyClients();
        }
      },
    },
  },
  methods: {
    ...mapActions('companies', ['updateCompanyById']),
    ...mapActions('clients', ['filterClients']),
    submit() {
      this.updateCompanyById(this.form.formData()).then((response) => {
        store.commit('companies/SET_COMPANY', response);
        this.toastSuccess(`Company, ${this.company.name}, was updated successfully!`);
      });
    },
    cancel() {
      this.$router.push({ path: '/companies' });
    },
    async loadCompanyClients() {
      if (!this.company?.id) return;

      this.loadingClients = true;
      try {
        const response = await this.filterClients({
          company: this.company.id,
          page_size: 100, // Load all clients for this company
        });
        this.companyClients = response.results || response;
      } catch (error) {
        console.error('Failed to load company clients:', error);
        this.companyClients = [];
      } finally {
        this.loadingClients = false;
      }
    },
  },
  async beforeRouteEnter(to, from, next) {
    const company = await store.dispatch('companies/getCompanyById', to.params.companyId);
    to.meta.label = `${company.name}`;
    return next();
  },
  beforeDestroy() {
    store.commit('companies/SET_COMPANY', null);
  },
};
</script>
