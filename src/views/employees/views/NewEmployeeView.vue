<template>
  <div class="relative overflow-x-auto p-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header Section -->
      <div class="mb-8">
        <div class="flex items-center space-x-4 mb-4">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-md">
            <font-awesome-icon :icon="['fas', 'user-plus']" class="text-white text-lg" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Create New Employee</h1>
            <p class="text-sm text-gray-600">Add a new employee to manage employee and service assignments</p>
          </div>
        </div>
      </div>

      <!-- Employee Form Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900 flex items-center">
            <font-awesome-icon :icon="['fas', 'user-tie']" class="mr-3 text-blue-600" />
            Employee Information
          </h3>
          <p class="mt-1 text-sm text-gray-600">Enter the personal and contact details for the new employee</p>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Username -->
              <div class="space-y-2">
                <label for="username" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'user-tag']" class="mr-2 text-gray-400" />
                  Username
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'user-tag']" class="text-gray-400" />
                  </div>
                  <input type="text" name="username" id="username" v-model="form.username" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="e.g. johnsmith" />
                </div>
                <p class="text-xs text-gray-500">Must be unique and cannot be changed later</p>
              </div>

              <!-- First Name -->
              <div class="space-y-2">
                <label for="first_name" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'user']" class="mr-2 text-gray-400" />
                  First Name
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'user']" class="text-gray-400" />
                  </div>
                  <input type="text" name="first_name" id="first_name" v-model="form.first_name" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter first name" />
                </div>
              </div>

              <!-- Surname -->
              <div class="space-y-2">
                <label for="last_name" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'user-tag']" class="mr-2 text-gray-400" />
                  Surname
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'user-tag']" class="text-gray-400" />
                  </div>
                  <input type="text" name="last_name" id="last_name" v-model="form.last_name" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter surname" />
                </div>
              </div>

              <!-- Date of Birth -->
              <div class="space-y-2">
                <label for="date_of_birth" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'calendar']" class="mr-2 text-gray-400" />
                  Date of Birth
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 z-10">
                    <font-awesome-icon :icon="['fas', 'calendar']" class="text-gray-400" />
                  </div>
                  <VueDatePicker v-mask="'##-##-####'" :teleport="true" v-model="form.date_of_birth" placeholder="MM-DD-YYYY" format="MM-dd-yyyy" model-type="yyyy-MM-dd" :max-date="new Date()" :hide-navigation="['time']" prevent-min-max-navigation auto-position="top" text-input hide-input-icon class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" />
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Email -->
              <div class="space-y-2">
                <label for="email" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'envelope']" class="mr-2 text-gray-400" />
                  Email
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'envelope']" class="text-gray-400" />
                  </div>
                  <input type="email" name="email" id="email" v-model="form.email" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="employee@company.com" />
                </div>
              </div>

              <!-- Phone Number -->
              <div class="space-y-2">
                <label for="mobile" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'phone']" class="mr-2 text-gray-400" />
                  Phone Number
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative flex rounded-lg shadow-sm">
                  <span class="inline-flex items-center px-3 rounded-l-lg border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">+</span>
                  <input type="text" name="mobile" id="mobile" v-mask="['### ###-####', '## # ####-####', '# (###) ###-####']" v-model="form.mobile" required class="block w-full rounded-none rounded-r-lg border border-gray-300 py-3 pl-3 pr-3 text-sm text-gray-900 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="597 000-0000" />
                </div>
              </div>

              <!-- Initial Password -->
              <div class="space-y-2">
                <label for="password" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'lock']" class="mr-2 text-gray-400" />
                  Initial Password
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'lock']" class="text-gray-400" />
                  </div>
                  <input type="password" name="password" id="password" v-model="form.password" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter initial password" />
                </div>
                <p class="text-xs text-gray-500">Employee can change this after first login</p>
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
                        {{ form.is_active ? 'Active Employee' : 'Inactive Employee' }}
                      </p>
                      <p class="text-sm text-gray-500">
                        {{ form.is_active ? 'Employee will be active and able to log in' : 'Employee will be inactive and unable to log in' }}
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
              <button @click="handleSubmit" :disabled="!form.username || !form.first_name || !form.last_name || !form.email || !form.mobile || !form.password" class="inline-flex items-center px-8 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 border border-transparent rounded-xl hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-lg">
                <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                Create Employee
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
import { mapActions } from 'vuex';

export default {
  components: {
    VueDatePicker,
  },
  data() {
    return {
      form: new Form({
        consistency_token: '00000000',
        username: null,
        first_name: null,
        last_name: null,
        date_of_birth: null,
        email: null,
        mobile: null,
        password: null,
        is_active: true,
      }),
    };
  },
  methods: {
    ...mapActions('employees', ['createEmployee']),
    handleSubmit() {
      if (!this.form.username || !this.form.first_name || !this.form.last_name || !this.form.email || !this.form.mobile || !this.form.password) {
        this.toastError('Please fill in all required fields');
        return;
      }

      this.createEmployee(this.form.formData())
        .then((response) => {
          this.toastSuccess(`Employee, ${response.first_name} ${response.last_name}, was created successfully!`);
          this.$router.push({ path: `/employees/${response.username}/view` });
        })
        .catch((error) => {
          this.toastError('Failed to create employee');
          console.error('Create employee error:', error);
        });
    },
    cancel() {
      this.$router.go(-1);
    },
  },
};
</script>
