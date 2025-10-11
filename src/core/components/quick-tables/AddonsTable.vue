<template>
  <div>
    <!-- Add/Edit Addon Form -->
    <div v-if="formVisible" class="mb-8 bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-2xl p-8 shadow-lg transition-all duration-300">
      <!-- Form Header -->
      <div class="flex items-start justify-between mb-8">
        <div class="flex items-start space-x-4">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-md">
            <font-awesome-icon :icon="editMode ? 'edit' : 'plus-circle'" class="text-white text-lg" />
          </div>
          <div>
            <h3 class="text-xl font-bold text-gray-900 mb-1">{{ editMode ? 'Edit Service Addon' : 'Create New Addon' }}</h3>
            <p class="text-sm text-gray-600">{{ editMode ? 'Update the addon details below' : 'Add a new service addon to enhance your service offerings' }}</p>
          </div>
        </div>
        <button @click="cancel" class="text-gray-400 hover:text-gray-600 transition-colors duration-150">
          <font-awesome-icon icon="times" class="text-xl" />
        </button>
      </div>

      <form @submit.prevent="onSubmit" class="space-y-8">
        <!-- Form Fields -->
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Addon Name -->
              <div class="group">
                <label for="addon_name" class="flex items-center text-sm font-semibold text-gray-800 mb-3">
                  <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center mr-2 group-focus-within:bg-blue-200 transition-colors duration-150">
                    <font-awesome-icon icon="plus-circle" class="text-blue-600 text-xs" />
                  </div>
                  Addon Name
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <input type="text" name="addon_name" id="addon_name" v-model="form.name" required class="block w-full px-4 py-3 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-medium transition-all duration-200 hover:border-blue-300" placeholder="e.g. Full Face Wax" />
                </div>
                <p class="text-xs text-gray-500 mt-2">Enter a descriptive name for this addon</p>
              </div>

              <!-- Additional Time -->
              <div class="group">
                <label for="additional_time" class="flex items-center text-sm font-semibold text-gray-800 mb-3">
                  <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center mr-2 group-focus-within:bg-blue-200 transition-colors duration-150">
                    <font-awesome-icon icon="clock" class="text-blue-600 text-xs" />
                  </div>
                  Additional Duration
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <VueDatePicker v-model="form.additional_time" auto-apply :teleport="true" text-input time-picker :start-time="startTime" :enable-seconds="false" :minute-increment="15" no-hours-overlay :format="'HH:mm'" placeholder="Select duration..." hide-input-icon input-class-name="px-4 py-3 pl-10 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-medium transition-all duration-200 hover:border-blue-300" />
                </div>
                <p class="text-xs text-gray-500 mt-2">How much extra time does this addon require?</p>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Price -->
              <div class="group">
                <label for="addon_price" class="flex items-center text-sm font-semibold text-gray-800 mb-3">
                  <div class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center mr-2 group-focus-within:bg-green-200 transition-colors duration-150">
                    <font-awesome-icon icon="dollar-sign" class="text-green-600 text-xs" />
                  </div>
                  Addon Price
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <span class="text-gray-500 font-medium">$</span>
                  </div>
                  <input type="number" name="addon_price" id="addon_price" v-model="form.price" step="0.01" min="0" required class="block w-full pl-8 pr-4 py-3 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-medium transition-all duration-200 hover:border-blue-300" placeholder="0.00" />
                </div>
                <p class="text-xs text-gray-500 mt-2">Set the additional cost for this addon</p>
              </div>

              <!-- Service Types -->
              <div class="group">
                <label for="service_types" class="flex items-center text-sm font-semibold text-gray-800 mb-3">
                  <div class="w-6 h-6 rounded-full bg-yellow-100 flex items-center justify-center mr-2 group-focus-within:bg-yellow-200 transition-colors duration-150">
                    <font-awesome-icon icon="tags" class="text-yellow-600 text-xs" />
                  </div>
                  Compatible Service Types
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute top-3 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'tags']" class="text-gray-400" />
                  </div>
                  <select multiple name="service_types" id="service_types" v-model="form.type" class="block w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-medium transition-all duration-200 hover:border-blue-300 bg-white" size="4">
                    <option v-for="serviceType in serviceTypes" :key="serviceType.id" :value="serviceType.id" class="py-2">
                      {{ serviceType.name }}
                    </option>
                  </select>
                </div>
                <p class="text-xs text-gray-500 mt-2">Hold Ctrl (Cmd on Mac) to select multiple service types</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Status -->
        <div class="mt-8">
          <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
            <div class="flex items-start space-x-4">
              <div class="flex items-center h-5 mt-1">
                <input type="checkbox" v-model="form.is_active" class="w-5 h-5 text-green-600 border-green-300 rounded-lg focus:ring-green-500 focus:ring-2 transition-colors duration-150" />
              </div>
              <div class="flex-1">
                <label class="flex items-center text-sm font-semibold text-gray-800 mb-2">
                  <font-awesome-icon icon="check-circle" class="mr-2 text-green-600" />
                  Active Status
                </label>
                <p class="text-sm text-gray-600 leading-relaxed">Enable this addon to make it available for selection when booking services. Disabled addons will be hidden from clients.</p>
                <div class="mt-3 flex items-center text-xs">
                  <font-awesome-icon :icon="form.is_active ? 'eye' : 'eye-slash'" class="mr-1.5" :class="form.is_active ? 'text-green-600' : 'text-gray-400'" />
                  <span :class="form.is_active ? 'text-green-700 font-medium' : 'text-gray-500'">
                    {{ form.is_active ? 'Available for booking' : 'Hidden from clients' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="flex items-center justify-between pt-6 border-t border-blue-200">
          <div class="text-sm text-gray-600">
            <font-awesome-icon icon="info-circle" class="mr-1.5 text-blue-500" />
            All fields marked with
            <span class="text-red-500">*</span>
            are required
          </div>
          <div class="flex items-center space-x-4">
            <button type="button" @click="cancel" class="px-6 py-3 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 transition-all duration-200">
              <font-awesome-icon icon="times" class="mr-2" />
              Cancel
            </button>
            <button type="submit" class="inline-flex items-center px-8 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-xl hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5">
              <font-awesome-icon :icon="editMode ? 'save' : 'plus'" class="mr-2" />
              {{ editMode ? 'Update Addon' : 'Create Addon' }}
            </button>
          </div>
        </div>
      </form>
    </div>

    <!-- Header Section -->
    <div class="space-y-3">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-gray-600">Manage additional services and extras for this service.</p>
        </div>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ addons.length }} {{ addons.length === 1 ? 'addon' : 'addons' }}</span>
      </div>

      <!-- Search and Add Section -->
      <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
        <div class="flex items-center space-x-3 flex-1 mr-3">
          <!-- Search Input -->
          <div class="relative max-w-md flex-1">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <font-awesome-icon icon="search" class="text-gray-400" />
            </div>
            <input type="text" name="addon_search" id="addon_search" v-model="filters.addon" @keyup.enter="itemProvider" class="block w-full pl-10 pr-3 py-2.5 text-sm text-gray-900 placeholder:text-gray-400 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-blue-300" placeholder="Search by addon name..." />
          </div>

          <!-- Service Type Filter -->
          <div class="relative min-w-0 w-48">
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <font-awesome-icon icon="tags" class="text-gray-400" />
            </div>
            <select v-model="filters.type" @change="itemProvider" class="block w-full pl-10 pr-8 py-2.5 text-sm text-gray-900 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-blue-300 appearance-none">
              <option :value="null">All Service Types</option>
              <option v-for="serviceType in serviceTypes" :key="serviceType.id" :value="serviceType.id">
                {{ serviceType.name }}
              </option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <font-awesome-icon icon="chevron-down" class="text-gray-400 text-xs" />
            </div>
          </div>
        </div>
        <button class="inline-flex items-center px-4 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-lg hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200" @click="formVisible = true">
          <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
          Add Addon
        </button>
      </div>
    </div>
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && addons.length === 0" class="text-center py-12">
      <font-awesome-icon icon="plus-circle" class="text-4xl text-gray-300 mb-4" />
      <h5 class="text-lg font-medium text-gray-900 mb-2">No Addons Found</h5>
      <p class="text-gray-500 mb-4">This service doesn't have any addons yet. Create your first addon to enhance service offerings.</p>
      <button class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-150" @click="formVisible = true">
        <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
        Create First Addon
      </button>
    </div>

    <!-- Addon Cards -->
    <div v-else class="space-y-3">
      <div v-for="addon in addons" :key="addon.id" class="group relative bg-gray-50 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 p-4">
        <div class="flex items-start justify-between">
          <!-- Main Content -->
          <div class="flex items-start space-x-3 flex-1">
            <!-- Icon and Status -->
            <div class="flex-shrink-0">
              <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors duration-200">
                <font-awesome-icon icon="plus-circle" class="text-blue-600 text-sm" />
              </div>
              <div class="mt-1.5 flex justify-center"></div>
            </div>

            <!-- Addon Details -->
            <div class="flex-1 min-w-0">
              <!-- Name and ID -->
              <div class="mb-3">
                <h5 class="text-base font-semibold text-gray-900 group-hover:text-blue-900">
                  {{ addon.name }}
                </h5>
                <div class="flex items-center text-xs text-gray-500 mt-0.5">
                  <span v-if="addon.is_active" class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    <font-awesome-icon icon="check-circle" class="mr-1 text-xs" />
                    Active
                  </span>
                  <span v-else class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                    <font-awesome-icon icon="times-circle" class="mr-1 text-xs" />
                    Inactive
                  </span>
                </div>
              </div>

              <!-- Details Grid -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <!-- Duration -->
                <div class="bg-white rounded-md p-2.5 border border-gray-100">
                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center">
                      <font-awesome-icon icon="clock" class="text-blue-600 text-xs" />
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Duration</p>
                      <p class="text-sm font-medium text-gray-900">{{ addon.time_display || 'N/A' }}</p>
                    </div>
                  </div>
                </div>

                <!-- Price -->
                <div class="bg-white rounded-md p-2.5 border border-gray-100">
                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                      <font-awesome-icon icon="dollar-sign" class="text-green-600 text-xs" />
                    </div>
                    <div>
                      <p class="text-xs text-gray-500">Price</p>
                      <p class="text-sm font-medium text-gray-900">${{ addon.price }}</p>
                    </div>
                  </div>
                </div>

                <!-- Service Types -->
                <div class="bg-white rounded-md p-2.5 border border-gray-100">
                  <div class="flex items-start space-x-2">
                    <div class="w-6 h-6 rounded-full bg-yellow-100 flex items-center justify-center">
                      <font-awesome-icon icon="tags" class="text-yellow-600 text-xs" />
                    </div>
                    <div class="flex-1">
                      <p class="text-xs text-gray-500 mb-1">Types</p>
                      <div class="flex flex-wrap gap-1">
                        <span v-for="typeId in addon.type" :key="typeId" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                          {{ getServiceTypeName(typeId) }}
                        </span>
                        <span v-if="!addon.type || addon.type.length === 0" class="text-xs text-gray-400">None</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Actions -->
          <div class="flex-shrink-0 ml-3">
            <div class="flex items-center space-x-1.5 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <!-- Edit Button -->
              <button @click="onEdit(addon)" class="inline-flex items-center px-2.5 py-1.5 text-xs font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-md border border-blue-200 hover:border-blue-300 transition-all duration-150 hover:shadow-sm" title="Edit addon">
                <font-awesome-icon :icon="['fas', 'edit']" class="mr-1" />
                Edit
              </button>

              <!-- Status Toggle Button -->
              <button v-if="addon.is_active" @click="onDeactivate(addon)" class="inline-flex items-center px-2.5 py-1.5 text-xs font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-md border border-red-200 hover:border-red-300 transition-all duration-150 hover:shadow-sm" title="Deactivate addon">
                <font-awesome-icon :icon="['fas', 'ban']" class="mr-1" />
                Deactivate
              </button>
              <button v-else @click="onActivate(addon)" class="inline-flex items-center px-2.5 py-1.5 text-xs font-medium text-green-700 bg-green-50 hover:bg-green-100 rounded-md border border-green-200 hover:border-green-300 transition-all duration-150 hover:shadow-sm" title="Activate addon">
                <font-awesome-icon :icon="['fas', 'check']" class="mr-1" />
                Activate
              </button>
            </div>

            <!-- Mobile/Always Visible Actions (for smaller screens) -->
            <div class="md:hidden flex items-center space-x-1">
              <button @click="onEdit(addon)" class="inline-flex items-center justify-center w-7 h-7 text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-full border border-blue-200 hover:border-blue-300 transition-all duration-150" title="Edit addon">
                <font-awesome-icon :icon="['fas', 'edit']" class="text-xs" />
              </button>

              <button v-if="addon.is_active" @click="onDeactivate(addon)" class="inline-flex items-center justify-center w-7 h-7 text-red-600 bg-red-50 hover:bg-red-100 rounded-full border border-red-200 hover:border-red-300 transition-all duration-150" title="Deactivate addon">
                <font-awesome-icon :icon="['fas', 'ban']" class="text-xs" />
              </button>
              <button v-else @click="onActivate(addon)" class="inline-flex items-center justify-center w-7 h-7 text-green-600 bg-green-50 hover:bg-green-100 rounded-full border border-green-200 hover:border-green-300 transition-all duration-150" title="Activate addon">
                <font-awesome-icon :icon="['fas', 'check']" class="text-xs" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Pagination -->
    <div v-if="addons.length > 0" class="mt-4 flex justify-between items-center p-3 bg-gray-50 rounded-lg border border-gray-200">
      <button @click="previousPage" :disabled="isFirstPage" class="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
        <font-awesome-icon icon="chevron-left" class="mr-1.5" />
        Previous
      </button>
      <span class="text-sm font-medium text-gray-700">
        Page {{ currentPage }} of {{ totalPages }}
        <span class="text-gray-500 ml-1">({{ addons.length }})</span>
      </span>
      <button @click="nextPage" :disabled="isLastPage" class="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
        Next
        <font-awesome-icon icon="chevron-right" class="ml-1.5" />
      </button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

import VueDatePicker from '@vuepic/vue-datepicker';
import { ArrowPathIcon } from '@heroicons/vue/24/outline';
import Form from '@/core/utils/Form';

export default {
  props: {
    service: {
      type: Object,
      required: null,
    },
  },
  components: {
    ArrowPathIcon,
    VueDatePicker,
  },
  data() {
    return {
      loading: false,
      activeDropdown: null,
      formVisible: false,
      editMode: false,

      count: null,
      currentPage: 1,
      pageSize: 5,
      totalPages: 1,
      sortBy: 'name',
      sortOrder: 'asc',

      addons: [],

      filters: { addon: '', type: null, is_active: null },

      startTime: { hours: 0, minutes: 0 },
      form: new Form({
        id: null,
        consistency_token: '00000000',
        name: '',
        additional_time: null,
        price: '',
        is_active: true,
        type: [],
      }),
    };
  },
  watch: {
    service: {
      immediate: true,
      handler(newService) {
        if (newService) {
          this.filters.type = newService.type?.id;
          this.itemProvider();
        }
      },
    },
  },
  computed: {
    ...mapState('services', {
      serviceTypes: (state) => state.types,
    }),
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
    ...mapActions('services', ['filterAddons', 'updateAddonById', 'createAddon', 'activateAddon', 'deactivateAddon']),
    getServiceTypeName(typeId) {
      const serviceType = this.serviceTypes.find((type) => type.id === typeId);
      return serviceType ? serviceType.name : `Type ${typeId}`;
    },
    itemProvider() {
      this.loading = true;
      this.filterAddons({
        page: this.currentPage,
        page_size: this.pageSize,
        ordering: this.sorting,
        addon: this.filters.addon || undefined,
        type: this.filters.type || undefined,
        is_active: this.filters.is_active !== null ? this.filters.is_active : undefined,
      })
        .then((response) => {
          this.addons = response.results;
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

    onSubmit() {
      console.log(this.form.formData());
      const action = this.editMode ? this.updateAddonById : this.createAddon;
      const payload = this.form.formData();
      console.log(payload);
      action(payload)
        .then((response) => {
          this.toastSuccess(`Addon "${response.name}" ${this.editMode ? 'updated' : 'created'} successfully!`);
          this.formVisible = false;
          this.resetForm();
          this.itemProvider();
        })
        .catch((errors) => {
          console.log(errors);
          this.toastError('An error occurred while saving the addon.');
        });
    },

    resetForm() {
      this.form.reset();
      this.editMode = false;
    },
    onEdit(addon) {
      this.editMode = true;
      this.form.populate(addon);
      this.form.type = addon.type;
      this.formVisible = true;
      this.activeDropdown = null;
    },
    onActivate(addon) {
      const payload = { id: addon.id, consistency_token: addon.consistency_token };
      this.activateAddon(payload)
        .then(() => {
          this.toastSuccess(`Addon "${addon.name}" activated successfully!`);
          this.itemProvider();
        })
        .catch((errors) => {
          this.formatErrors(errors.response);
        })
        .finally(() => {
          this.activeDropdown = null;
        });
    },
    onDeactivate(addon) {
      const payload = { id: addon.id, consistency_token: addon.consistency_token };
      this.deactivateAddon(payload)
        .then(() => {
          this.toastSuccess(`Addon "${addon.name}" deactivated successfully!`);
          this.itemProvider();
        })
        .catch((errors) => {
          this.formatErrors(errors.response);
        })
        .finally(() => {
          this.activeDropdown = null;
        });
    },
    cancel() {
      this.formVisible = false;
      this.resetForm();
    },
  },
  beforeDestroy() {
    // Remove click outside listener
    document.removeEventListener('click', this.handleClickOutside);
  },
  created() {
    document.addEventListener('click', this.handleClickOutside);
  },
  mounted() {
    this.itemProvider();
  },
  async beforeRouteEnter(to, from, next) {
    const servicetypes = await this.$store.dispatch('services/getServiceTypes');
    return next();
  },
};
</script>
