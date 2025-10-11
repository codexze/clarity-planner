<template>
  <div class="relative overflow-x-auto p-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header Section -->
      <div class="mb-8">
        <div class="flex items-center space-x-4 mb-4">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-md">
            <font-awesome-icon :icon="['fas', 'building']" class="text-white text-lg" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Create New Company</h1>
            <p class="text-sm text-gray-600">Set up a new company to manage clients and business relationships</p>
          </div>
        </div>
      </div>

      <!-- Company Form Card -->
      <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900 flex items-center">
            <font-awesome-icon :icon="['fas', 'building']" class="mr-3 text-blue-600" />
            Company Information
          </h3>
          <p class="mt-1 text-sm text-gray-600">Enter the basic information for the new company</p>
        </div>

        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Company Name -->
              <div class="space-y-2">
                <label for="name" class="flex items-center text-sm font-medium text-gray-900">
                  <font-awesome-icon :icon="['fas', 'building']" class="mr-2 text-gray-400" />
                  Company Name
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <font-awesome-icon :icon="['fas', 'building']" class="text-gray-400" />
                  </div>
                  <input type="text" name="name" id="name" v-model="form.name" required class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter company name" />
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
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
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
                        {{ form.is_active ? 'Company will be active and visible in the system' : 'Company will be inactive and hidden from listings' }}
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
                Create Company
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
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      form: new Form({
        consistency_token: '00000000',
        name: null,
        address: null,
        email: null,
        phone: null,
        website: null,
        is_active: true,
      }),
    };
  },
  methods: {
    ...mapActions('companies', ['createCompany']),
    handleSubmit() {
      if (!this.form.name) {
        this.toastError('Company name is required');
        return;
      }

      this.createCompany(this.form.formData())
        .then((response) => {
          this.toastSuccess(`Company, ${response.name}, was created successfully!`);
          this.$router.push({ path: `/companies/${response.id}/view` });
        })
        .catch((error) => {
          this.toastError('Failed to create company');
          console.error('Create company error:', error);
        });
    },
    cancel() {
      this.$router.go(-1);
    },
  },
};
</script>
