<template>
  <div class="relative overflow-x-auto p-4 bg-gray-50">
    <div class="grid grid-cols-1 gap-x-6 gap-y-6 sm:grid-cols-6">
      <div class="sm:col-span-3 sm:col-start-1 space-y-6">
        <!-- Employee Information Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'user-tie']" class="mr-3 text-blue-600" />
              Employee Information
            </h3>
            <p class="mt-1 text-sm text-gray-600">Manage employee details and personal information</p>
          </div>

          <div class="p-6 space-y-6">
            <!-- Username -->
            <div class="space-y-2">
              <label for="username" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'user-tag']" class="mr-2 text-gray-400" />
                Username
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'user-tag']" class="text-gray-400" />
                </div>
                <input type="text" name="username" id="username" v-model="form.username" disabled class="block w-full rounded-lg border border-gray-300 bg-gray-50 py-3 pl-10 pr-4 text-sm text-gray-500 shadow-sm cursor-not-allowed" placeholder="e.g. johnsmith" />
              </div>
              <p class="text-xs text-gray-500">Username cannot be changed</p>
            </div>

            <!-- First Name -->
            <div class="space-y-2">
              <label for="first_name" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'user']" class="mr-2 text-gray-400" />
                First Name
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'user']" class="text-gray-400" />
                </div>
                <input type="text" name="first_name" id="first_name" v-model="form.first_name" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter first name" />
              </div>
            </div>

            <!-- Surname -->
            <div class="space-y-2">
              <label for="last_name" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'user-tag']" class="mr-2 text-gray-400" />
                Surname
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'user-tag']" class="text-gray-400" />
                </div>
                <input type="text" name="last_name" id="last_name" v-model="form.last_name" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter surname" />
              </div>
            </div>

            <!-- Date of Birth -->
            <div class="space-y-2">
              <label for="date_of_birth" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'calendar']" class="mr-2 text-gray-400" />
                Date of Birth
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'calendar']" class="text-gray-400" />
                </div>
                <VueDatePicker v-mask="'##-##-####'" :teleport="true" v-model="form.date_of_birth" placeholder="MM-DD-YYYY" format="MM-dd-yyyy" model-type="yyyy-MM-dd" :max-date="new Date()" :hide-navigation="['time']" prevent-min-max-navigation auto-position="top" text-input hide-input-icon class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" />
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
                <input type="email" name="email" id="email" v-model="form.email" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="name@example.com" />
              </div>
            </div>
            <!-- Phone Number -->
            <div class="space-y-2">
              <label for="mobile" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'phone']" class="mr-2 text-gray-400" />
                Phone Number
              </label>
              <div class="relative flex rounded-lg shadow-sm">
                <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">+</span>
                <input type="text" name="mobile" id="mobile" v-mask="['### ###-####', '## # ####-####', '# (###) ###-####']" v-model="form.mobile" class="block w-full rounded-none rounded-r-lg border border-gray-300 py-3 pl-3 pr-3 text-sm text-gray-900 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="597 000-0000" />
              </div>
            </div>

            <!-- Active Status -->
            <div class="space-y-4">
              <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center transition-colors duration-200" :class="form.is_active ? 'bg-green-100' : 'bg-gray-100'">
                    <font-awesome-icon :icon="['fas', form.is_active ? 'user-check' : 'user-slash']" :class="form.is_active ? 'text-green-600' : 'text-gray-600'" />
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">
                      {{ form.is_active ? 'Active Employee' : 'Inactive Employee' }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ form.is_active ? 'Employee is active and can perform services' : 'Employee is inactive and cannot be assigned to appointments' }}
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
            Changes will be saved to the employee's profile
          </div>
          <!-- Form Actions -->
          <div class="flex items-center space-x-4">
            <button @click="handleSubmit" :disabled="!form.dirty()" class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed space-x-2">
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
        <!-- Employee Services Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-3 text-blue-600" />
              Employee Services
            </h3>
            <p class="mt-1 text-sm text-gray-600">Select which services this employee can perform</p>
          </div>

          <div class="p-6">
            <!-- Service Selection Controls -->
            <div class="mb-6 flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <button type="button" @click="selectAllServices" class="text-sm text-blue-600 hover:text-blue-800 font-medium transition-colors duration-150" :disabled="allServicesSelected" :class="{ 'opacity-50 cursor-not-allowed': allServicesSelected }">Select All</button>
                <button type="button" @click="clearAllServices" class="text-sm text-gray-600 hover:text-gray-800 font-medium transition-colors duration-150" :disabled="noServicesSelected" :class="{ 'opacity-50 cursor-not-allowed': noServicesSelected }">Clear All</button>
              </div>
              <div class="text-sm text-gray-500">{{ selectedServicesCount }} of {{ totalServicesCount }} selected</div>
            </div>

            <!-- Loading State -->
            <div v-if="loadingServices" class="flex items-center justify-center py-8">
              <font-awesome-icon icon="spinner" spin class="text-blue-500 mr-2" />
              <span class="text-sm text-gray-600">Loading services...</span>
            </div>

            <!-- No Services Available -->
            <div v-else-if="!types || types.length === 0" class="text-center py-8">
              <font-awesome-icon :icon="['fas', 'spa']" class="text-gray-300 text-4xl mb-3" />
              <p class="text-sm text-gray-500">No services available</p>
            </div>

            <!-- Services Grid -->
            <div v-else class="grid grid-cols-1 gap-4">
              <div v-for="(type, index) in types" :key="type.id" class="relative flex items-start p-4 border rounded-lg transition-all duration-150" :class="[isServiceSelected(type.id) ? 'border-blue-300 bg-blue-50 ring-1 ring-blue-300' : 'border-gray-200 hover:bg-gray-50 hover:border-gray-300']">
                <div class="flex h-6 items-center">
                  <input :id="`type-checkbox-${type.id}`" type="checkbox" :value="type.id" v-model="form.services" :name="`type-checkbox-${type.id}`" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 transition-colors duration-150" :checked="isServiceSelected(type.id)" @change="onServiceChange(type.id)" />
                </div>
                <div class="ml-3 text-sm leading-6 flex-1">
                  <label :for="`type-checkbox-${type.id}`" class="font-medium text-gray-900 flex items-center cursor-pointer" :class="{ 'text-blue-900': isServiceSelected(type.id) }">
                    <font-awesome-icon :icon="getServiceIcon(type)" class="mr-2 transition-colors duration-150" :class="isServiceSelected(type.id) ? 'text-blue-600' : 'text-blue-500'" />
                    {{ type.name }}
                  </label>
                  <p v-if="type.description" class="text-xs text-gray-500 mt-1">
                    {{ type.description }}
                  </p>
                </div>
                <!-- Selected indicator -->
                <div v-if="isServiceSelected(type.id)" class="ml-2">
                  <font-awesome-icon :icon="['fas', 'check-circle']" class="text-blue-600 text-sm" />
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

import VueDatePicker from '@vuepic/vue-datepicker';
import { ChevronDownIcon } from '@heroicons/vue/24/solid';

import { mapState, mapGetters, mapActions } from 'vuex';
export default {
  components: {
    VueDatePicker,
    ChevronDownIcon,
  },
  data() {
    return {
      loadingServices: false,
      form: new Form({
        id: null,
        consistency_token: null,
        username: null,
        first_name: null,
        last_name: null,
        date_of_birth: null,
        email: null,
        mobile: null,
        is_active: null,
        services: [],
      }),
    };
  },
  computed: {
    ...mapState('staff', {
      employee: (state) => state.employee,
    }),
    ...mapState('services', {
      types: (state) => state.types,
    }),
    selectedServicesCount() {
      return Array.isArray(this.form.services) ? this.form.services.length : 0;
    },
    totalServicesCount() {
      return this.types ? this.types.length : 0;
    },
    allServicesSelected() {
      return this.selectedServicesCount === this.totalServicesCount && this.totalServicesCount > 0;
    },
    noServicesSelected() {
      return this.selectedServicesCount === 0;
    },
  },
  watch: {
    employee: {
      immediate: true,
      handler(val) {
        if (val) {
          this.form.populate(val);
          // Ensure form.services is always an array
          if (!Array.isArray(this.form.services)) {
            this.form.services = val.services || [];
          }
          // If services is an array of objects, extract IDs
          if (Array.isArray(this.form.services) && this.form.services.length > 0 && typeof this.form.services[0] === 'object') {
            this.form.services = this.form.services.map((service) => service.id || service);
          }
        }
      },
    },
  },
  methods: {
    ...mapActions('staff', ['updateEmployeeByUsername']),
    handleSubmit() {
      this.updateEmployeeByUsername(this.form.formData()).then((response) => {
        store.commit('staff/SET_EMPLOYEE', response);
        this.toastSuccess(`Employee, ${this.employee.name}, was updated successfully!`);
        // console.log(response);
      });
      // console.log(this.form.formData());
    },
    cancel() {
      this.$router.push({ path: '/staff' });
    },
    selectAllServices() {
      if (this.types && this.types.length > 0) {
        this.form.services = this.types.map((type) => type.id);
        this.toastInfo(`All ${this.types.length} services selected`);
      }
    },
    clearAllServices() {
      this.form.services = [];
      this.toastInfo('All services cleared');
    },
    isServiceSelected(serviceId) {
      // Ensure form.services is an array
      if (!Array.isArray(this.form.services)) {
        this.form.services = [];
        return false;
      }
      return this.form.services.includes(serviceId);
    },
    onServiceChange(serviceId) {
      // Optional: Add custom logic when a service is selected/deselected
      const isSelected = this.isServiceSelected(serviceId);
      const serviceName = this.types.find((type) => type.id === serviceId)?.name || 'Service';

      if (isSelected) {
        // Service was just selected
        console.log(`Service "${serviceName}" added to employee`);
      } else {
        // Service was just deselected
        console.log(`Service "${serviceName}" removed from employee`);
      }
    },
    getServiceIcon(type) {
      // Dynamic icon based on service type or fallback to spa icon
      const iconMap = {
        facial: 'face-smile',
        massage: 'hands',
        nail: 'hand-sparkles',
        hair: 'scissors',
        spa: 'spa',
        beauty: 'gem',
        wellness: 'heart',
        therapy: 'hands-holding-heart',
      };

      // Try to match service name with icon
      const serviceName = type.name.toLowerCase();
      for (const [key, icon] of Object.entries(iconMap)) {
        if (serviceName.includes(key)) {
          return ['fas', icon];
        }
      }

      // Default fallback
      return ['fas', 'spa'];
    },
    debugFormServices() {
      console.log('form.services:', this.form.services);
      console.log('form.services type:', typeof this.form.services);
      console.log('form.services is array:', Array.isArray(this.form.services));
      console.log('employee data:', this.employee);
      console.log('types:', this.types);
    },
  },
  mounted() {
    // Ensure form.services is always an array
    if (!Array.isArray(this.form.services)) {
      this.form.services = [];
    }
  },
  async beforeRouteEnter(to, from, next) {
    const employee = await store.dispatch('staff/getEmployeeByUsername', to.params.employeeId);
    const types = await store.dispatch('services/getServiceTypes');
    // to.meta.label = `${employee.name}`;
    return next();
  },
  beforeDestroy() {
    store.commit('staff/SET_EMPLOYEE', null);
  },
};
</script>
