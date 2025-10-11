<template>
  <div class="relative overflow-x-auto p-4">
    <div class="grid grid-cols-1 gap-x-6 gap-y-6 sm:grid-cols-6">
      <div class="sm:col-span-3 sm:col-start-1 space-y-6">
        <!-- Service Information Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-3 text-blue-600" />
              Service Information
            </h3>
            <p class="mt-1 text-sm text-gray-600">Manage service details, pricing, and availability</p>
          </div>

          <div class="p-6 space-y-6">
            <!-- Service Name -->
            <div class="space-y-2">
              <label for="name" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-2 text-gray-400" />
                Service Name
                <span class="text-red-500 ml-1">*</span>
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'briefcase']" class="text-gray-400" />
                </div>
                <input type="text" name="name" id="name" v-model="form.name" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="e.g. Hair & Makeup" />
              </div>
            </div>

            <!-- Service Type -->
            <div class="space-y-2">
              <label for="type" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'tags']" class="mr-2 text-gray-400" />
                Service Type
                <span class="text-red-500 ml-1">*</span>
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'tags']" class="text-gray-400" />
                </div>
                <select id="type" v-model="form.type_id" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                  <option :value="null">Select a service type</option>
                  <option v-for="type in serviceTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Description -->
            <div class="space-y-2">
              <label for="description" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'align-left']" class="mr-2 text-gray-400" />
                Description
                <span class="text-red-500 ml-1">*</span>
              </label>
              <div class="relative">
                <textarea name="description" id="description" rows="4" v-model="form.description" class="block w-full rounded-lg border border-gray-300 bg-white py-3 px-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 resize-none" placeholder="Write a few sentences about this service..."></textarea>
              </div>
              <p class="text-xs text-gray-500">Describe what this service includes and any special features.</p>
            </div>

            <!-- Duration -->
            <div class="space-y-2">
              <label for="duration" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'clock']" class="mr-2 text-gray-400" />
                Duration
                <span class="text-red-500 ml-1">*</span>
              </label>
              <div class="relative">
                <VueDatePicker v-model="form.duration" auto-apply :teleport="true" text-input time-picker :start-time="startTime" :enable-seconds="false" :minute-increment="15" no-hours-overlay :format="'HH:mm'" placeholder="Select duration" hide-input-icon input-class-name="rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" />
              </div>
            </div>

            <!-- Price -->
            <div class="space-y-2">
              <label for="price" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'dollar-sign']" class="mr-2 text-gray-400" />
                Price
                <span class="text-red-500 ml-1">*</span>
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <span class="text-gray-400 font-medium">$</span>
                </div>
                <input type="number" name="price" id="price" v-model="form.price" step="0.01" min="0" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-8 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="0.00" />
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
                      {{ form.is_active ? 'Service Available' : 'Service Unavailable' }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ form.is_active ? 'Service is active and available for booking' : 'Service is inactive and cannot be booked' }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center">
                  <input id="available" type="checkbox" v-model="form.is_active" class="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 transition-colors duration-200" />
                  <label for="available" class="ml-3 text-sm font-medium text-gray-700">Available</label>
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
          <div class="flex items-center space-x-4">
            <button @click="handleSubmit" :disabled="!form.dirty() || !form.name" class="inline-flex items-center px-8 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-xl hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-lg">
              <font-awesome-icon :icon="['fas', 'save']" class="mr-2" />
              Save Changes
            </button>
            <button @click="cancel" class="px-6 py-3 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 transition-all duration-200">
              <font-awesome-icon :icon="['fas', 'times']" class="mr-2" />
              Cancel
            </button>
          </div>
        </div>
      </div>

      <div class="sm:col-span-3 sm:col-start-4">
        <!-- Service Addons Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'plus-circle']" class="mr-3 text-blue-600" />
              Service Add-ons
            </h3>
            <p class="mt-1 text-sm text-gray-600">Manage additional services and extras for this service</p>
          </div>

          <div class="p-6">
            <AddonsTable :service="service" />
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

import { mapState, mapGetters, mapActions } from 'vuex';

import AddonsTable from '@/core/components/quick-tables/AddonsTable.vue';
export default {
  components: {
    VueDatePicker,
    AddonsTable,
  },
  data() {
    return {
      startTime: { hours: 0, minutes: 0 },
      form: new Form({
        id: null,
        consistency_token: null,
        type_id: null,
        name: null,
        description: null,
        duration: null,
        price: null,
        is_active: true,
      }),
    };
  },
  computed: {
    ...mapState('services', {
      service: (state) => state.service,
      serviceTypes: (state) => state.types,
    }),
  },
  watch: {
    service: {
      immediate: true,
      handler(val) {
        this.form.populate(val);
        this.form.type_id = val.type?.id;
      },
    },
  },
  methods: {
    ...mapActions('services', ['updateServiceById']),
    handleSubmit() {
      if (!this.form.name) {
        this.toastError('Service name is required');
        return;
      }

      this.updateServiceById(this.form.formData())
        .then((response) => {
          store.commit('services/SET_SERVICE', response);
          this.toastSuccess(`Service, ${this.service.name}, was updated successfully!`);
        })
        .catch((error) => {
          this.toastError('Failed to update service');
          console.error('Update service error:', error);
        });
    },
    cancel() {
      this.$router.go(-1);
    },
  },
  async beforeRouteEnter(to, from, next) {
    const service = await store.dispatch('services/getServiceById', to.params.serviceId);
    const types = await store.dispatch('services/getServiceTypes');
    to.meta.label = `${service.name}`;
    return next();
  },
  beforeDestroy() {
    store.commit('services/SET_SERVICE', null);
  },
};
</script>
