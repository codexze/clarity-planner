<template>
  <div class="relative overflow-x-auto p-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header Section -->
      <div class="mb-8">
        <div class="flex items-center space-x-4 mb-4">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-md">
            <font-awesome-icon :icon="['fas', 'briefcase']" class="text-white text-lg" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Create New Service</h1>
            <p class="text-sm text-gray-600">Set up a new service offering for your business</p>
          </div>
        </div>
      </div>

      <!-- Service Form Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900 flex items-center">
            <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-3 text-blue-600" />
            Service Information
          </h3>
          <p class="mt-1 text-sm text-gray-600">Enter the details for your new service offering</p>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column -->
            <div class="space-y-6">
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
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'tags']" class="text-gray-400" />
                  </div>
                  <select id="type" v-model="form.type_id" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
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
                  <font-awesome-icon :icon="['fas', 'file-alt']" class="mr-2 text-gray-400" />
                  Description
                </label>
                <div class="relative">
                  <textarea name="description" id="description" rows="3" v-model="form.description" class="block w-full rounded-lg border border-gray-300 bg-white py-3 px-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 resize-none" placeholder="Write a few sentences about this service..."></textarea>
                </div>
                <p class="text-xs text-gray-500">Write a few sentences about this service.</p>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Duration -->
              <div class="space-y-2">
                <label for="duration" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'clock']" class="mr-2 text-gray-400" />
                  Duration
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'clock']" class="text-gray-400" />
                  </div>
                  <VueDatePicker v-model="form.duration" auto-apply :teleport="true" text-input time-picker :start-time="startTime" :enable-seconds="false" :minute-increment="15" no-hours-overlay :format="'HH:mm'" placeholder="Select duration" hide-input-icon class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" />
                </div>
              </div>

              <!-- Price -->
              <div class="space-y-2">
                <label for="price" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'dollar-sign']" class="mr-2 text-gray-400" />
                  Price
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <span class="text-gray-400">$</span>
                  </div>
                  <input type="text" name="price" id="price" v-model="form.price" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-8 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="0.00" />
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
                        {{ form.is_active ? 'Available for Booking' : 'Not Available' }}
                      </p>
                      <p class="text-sm text-gray-500">
                        {{ form.is_active ? 'Service will be active and bookable by clients' : 'Service will be inactive and hidden from booking' }}
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

          <!-- Form Actions -->
          <div class="mt-8 pt-6 border-t border-gray-200 flex items-center justify-between">
            <div class="text-sm text-gray-600">
              <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1.5 text-blue-500" />
              Fields marked with
              <span class="text-red-500">*</span>
              are required
            </div>
            <div class="flex items-center space-x-4">
              <button @click="cancel" class="px-6 py-3 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 transition-all duration-200">
                <font-awesome-icon :icon="['fas', 'times']" class="mr-2" />
                Cancel
              </button>
              <button @click="handleSubmit" :disabled="!form.name" class="inline-flex items-center px-8 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-xl hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-lg">
                <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                Create Service
              </button>
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
      startTime: { hours: 0, minutes: 0 },
      form: new Form({
        consistency_token: '00000000',
        type_id: null,
        name: null,
        description: null,
        duration: null,
        price: null,
        is_active: false,
      }),
    };
  },
  computed: {
    ...mapState('services', {
      serviceTypes: (state) => state.types,
    }),
  },
  methods: {
    ...mapActions('services', ['createService']),
    handleSubmit() {
      this.createService(this.form.formData()).then((response) => {
        this.toastSuccess(`Service, ${response.name}, was created successfully!`);
        this.$router.push({ path: `/services/${response.id}/view` });
      });
    },
    cancel() {
      this.$router.go(-1);
    },
  },
  async beforeRouteEnter(to, from, next) {
    const types = await store.dispatch('services/getServiceTypes');
    // to.meta.label = `${service.name}`;
    return next();
  },
};
</script>
