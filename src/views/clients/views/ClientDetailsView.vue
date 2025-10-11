<template>
  <div class="relative overflow-x-auto p-4 bg-gray-50">
    <div class="grid grid-cols-1 gap-x-6 gap-y-6 sm:grid-cols-6">
      <div class="sm:col-span-3 sm:col-start-1 space-y-6">
        <!-- Client Information Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'user']" class="mr-3 text-blue-600" />
              Client Information
            </h3>
            <p class="mt-1 text-sm text-gray-600">Manage client details and personal information</p>
          </div>

          <div class="p-6 space-y-6">
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
              <label for="surname" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'user-tag']" class="mr-2 text-gray-400" />
                Surname
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'user-tag']" class="text-gray-400" />
                </div>
                <input type="text" name="surname" id="surname" v-model="form.surname" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Enter surname" />
              </div>
            </div>

            <!-- Gender -->
            <div class="space-y-2">
              <label for="genders" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'venus-mars']" class="mr-2 text-gray-400" />
                Gender
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'venus-mars']" class="text-gray-400" />
                </div>
                <select id="genders" v-model="form.gender" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                  <option v-for="gender in genders" :key="gender.value" :value="gender.value">{{ gender.label }}</option>
                </select>
              </div>
            </div>

            <!-- Date of Birth -->
            <div class="space-y-2">
              <label for="date_of_birth" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'calendar']" class="mr-2 text-gray-400" />
                Date of Birth
              </label>
              <div class="relative">
                <VueDatePicker v-mask="'##-##-####'" :teleport="true" v-model="form.date_of_birth" placeholder="MM-DD-YYYY" format="MM-dd-yyyy" model-type="yyyy-MM-dd" :max-date="new Date()" :hide-navigation="['time']" prevent-min-max-navigation auto-position="top" text-input hide-input-icon input-class-name="rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" />
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

            <!-- Company -->
            <div class="space-y-2">
              <label for="company" class="flex items-center text-sm font-medium text-gray-900">
                <font-awesome-icon :icon="['fas', 'building']" class="mr-2 text-gray-400" />
                Company
              </label>
              <div class="relative">
                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <font-awesome-icon :icon="['fas', 'building']" class="text-gray-400" />
                </div>
                <select id="company" v-model="form.company" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                  <option :value="null">Select a company (optional)</option>
                  <option v-for="company in companies" :key="company.id" :value="company.id">{{ company.name }}</option>
                </select>
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
                      {{ form.is_active ? 'Active Client' : 'Inactive Client' }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ form.is_active ? 'Client is active and can book appointments' : 'Client is inactive and cannot book new appointments' }}
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
        <!-- Client Details Tabs Card -->
        <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <font-awesome-icon :icon="['fas', 'chart-line']" class="mr-3 text-blue-600" />
              Client Details
            </h3>
            <p class="mt-1 text-sm text-gray-600">View appointments, addresses, and reminders for this client</p>
          </div>

          <div class="px-6 py-4 border-b border-gray-100">
            <nav class="-mb-px flex space-x-8" aria-label="Tabs">
              <button v-for="tab in tabs" :key="tab.name" @click="currentTab = tab.name" :class="[currentTab === tab.name ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700', 'whitespace-nowrap border-b-2 py-2 px-1 text-sm font-medium transition-colors duration-150']">
                {{ tab.label }}
              </button>
            </nav>
          </div>

          <div class="p-6">
            <!-- Appointments Tab -->
            <div v-if="currentTab === 'appointments'">
              <QuickAppointmentTable :client="client" />
            </div>

            <!-- Addresses Tab -->
            <div v-if="currentTab === 'addresses'">
              <KnownAddressTable :client="client" />
            </div>

            <!-- Reminders Tab -->
            <div v-if="currentTab === 'reminders'">
              <ReminderTable :client="client" />
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

import QuickAppointmentTable from '@/core/components/quick-tables/QuickAppointmentTable.vue';
import KnownAddressTable from '@/core/components/quick-tables/KnownAddressTable.vue';
import ReminderTable from '@/core/components/quick-tables/ReminderTable.vue';

import { mapState, mapActions } from 'vuex';
export default {
  components: {
    VueDatePicker,
    QuickAppointmentTable,
    KnownAddressTable,
    ReminderTable,
  },
  data() {
    return {
      currentTab: 'appointments',
      tabs: [
        { name: 'appointments', label: 'Appointments' },
        { name: 'addresses', label: 'Addresses' },
        { name: 'reminders', label: 'Reminders' },
      ],

      form: new Form({
        id: null,
        consistency_token: null,
        first_name: null,
        surname: null,
        date_of_birth: null,
        gender: 'UNKNOWN',
        email: null,
        mobile: null,
        is_active: true,
        company: null,
      }),
    };
  },
  computed: {
    ...mapState('clients', {
      client: (state) => state.client,
      genders: (state) => state.genders,
    }),
    ...mapState('companies', {
      companies: (state) => state.companies,
    }),
  },
  watch: {
    client: {
      immediate: true,
      handler(val) {
        this.form.populate(val);
      },
    },
  },
  methods: {
    ...mapActions('clients', ['updateClientById']),
    handleSubmit() {
      this.updateClientById(this.form.formData()).then((response) => {
        store.commit('clients/SET_CLIENT', response);
        this.toastSuccess(`Client, ${this.client.name}, was updated successfully!`);
        // console.log(response);
      });
      // console.log(this.form.formData());
    },
    cancel() {
      this.$router.push({ path: '/clients' });
    },
  },
  async beforeRouteEnter(to, from, next) {
    const client = await store.dispatch('clients/getClientById', to.params.clientId);
    await store.dispatch('clients/getGenders');
    await store.dispatch('companies/getCompanies');

    to.meta.label = `${client.display}`;
    return next();
  },
  beforeDestroy() {
    store.commit('clients/SET_CLIENT', null);
  },
};
</script>
