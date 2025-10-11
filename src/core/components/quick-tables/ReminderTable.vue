<template>
  <div>
    <!-- Add/Edit Reminder Form -->
    <div v-if="formVisible" class="mb-8 bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-2xl p-8 shadow-lg transition-all duration-300">
      <!-- Form Header -->
      <div class="flex items-start justify-between mb-8">
        <div class="flex items-start space-x-4">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-md">
            <font-awesome-icon :icon="editMode ? 'edit' : 'plus-circle'" class="text-white text-lg" />
          </div>
          <div>
            <h3 class="text-xl font-bold text-gray-900 mb-1">{{ editMode ? 'Edit Reminder' : 'Create New Reminder' }}</h3>
            <p class="text-sm text-gray-600">{{ editMode ? 'Update the reminder details below' : 'Set up a new reminder to stay on top of client follow-ups' }}</p>
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
              <!-- Reminder Date -->
              <div class="group">
                <label for="appointment_date" class="flex items-center text-sm font-semibold text-gray-800 mb-3">
                  <div class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center mr-2 group-focus-within:bg-blue-200 transition-colors duration-150">
                    <font-awesome-icon icon="calendar-alt" class="text-blue-600 text-xs" />
                  </div>
                  Reminder Date
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <div class="relative">
                  <VueDatePicker v-mask="'##-##-####'" :teleport="true" v-model="form.appointment_date" placeholder="Select a date..." format="MM-dd-yyyy" model-type="yyyy-MM-dd" :min-date="new Date()" :hide-navigation="['time']" prevent-min-max-navigation auto-position="top" text-input class="block w-full px-4 py-3 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-medium transition-all duration-200 hover:border-blue-300" />
                </div>
                <p class="text-xs text-gray-500 mt-2">Choose when you want to be reminded</p>
              </div>

              <!-- Reason -->
              <div class="group">
                <label for="reason" class="flex items-center text-sm font-semibold text-gray-800 mb-3">
                  <div class="w-6 h-6 rounded-full bg-yellow-100 flex items-center justify-center mr-2 group-focus-within:bg-yellow-200 transition-colors duration-150">
                    <font-awesome-icon icon="bell" class="text-yellow-600 text-xs" />
                  </div>
                  Reminder Reason
                  <span class="text-red-500 ml-1">*</span>
                </label>
                <select id="reasons" v-model="form.reason" class="block w-full px-4 py-3 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm font-medium transition-all duration-200 hover:border-blue-300 bg-white">
                  <option :value="null" class="text-gray-400">Choose a reason...</option>
                  <option v-for="reason in reasons" :key="reason.value" :value="reason.value">{{ reason.label }}</option>
                </select>

                <!-- Custom Reason Input -->
                <div v-if="form.reason === 'OTHER'" class="mt-4 animate-fadeIn">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    <font-awesome-icon icon="edit" class="mr-1.5 text-gray-400" />
                    Custom Reason
                  </label>
                  <input type="text" name="other_reason" id="other_reason" v-model="form.other_reason" class="block w-full px-4 py-3 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm transition-all duration-200 hover:border-blue-300" placeholder="e.g., Follow-up call, Check satisfaction, Review progress..." />
                </div>
                <p class="text-xs text-gray-500 mt-2">What do you need to be reminded about?</p>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Global Reminder Toggle -->
              <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-200">
                <div class="flex items-start space-x-4">
                  <div class="flex items-center h-5 mt-1">
                    <input type="checkbox" v-model="form.global_reminder" class="w-5 h-5 text-purple-600 border-purple-300 rounded-lg focus:ring-purple-500 focus:ring-2 transition-colors duration-150" />
                  </div>
                  <div class="flex-1">
                    <label class="flex items-center text-sm font-semibold text-gray-800 mb-2">
                      <font-awesome-icon icon="globe" class="mr-2 text-purple-600" />
                      Global Reminder
                    </label>
                    <p class="text-sm text-gray-600 leading-relaxed">Enable this to make the reminder visible to all team members. Perfect for important follow-ups that require team coordination.</p>
                    <div class="mt-3 flex items-center text-xs">
                      <font-awesome-icon :icon="form.global_reminder ? 'users' : 'user'" class="mr-1.5" :class="form.global_reminder ? 'text-purple-600' : 'text-gray-400'" />
                      <span :class="form.global_reminder ? 'text-purple-700 font-medium' : 'text-gray-500'">
                        {{ form.global_reminder ? 'Visible to all team members' : 'Only visible to you' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Preview Card -->
              <div class="bg-gray-50 rounded-xl p-6 border border-gray-200">
                <h4 class="text-sm font-semibold text-gray-800 mb-3 flex items-center">
                  <font-awesome-icon icon="eye" class="mr-2 text-gray-500" />
                  Preview
                </h4>
                <div class="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                      <font-awesome-icon icon="bell" class="text-blue-600 text-sm" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">
                        {{ form.reason && form.reason !== 'OTHER' ? reasons?.find((r) => r.value === form.reason)?.label : form.other_reason || 'Reminder reason' }}
                      </p>
                      <p class="text-xs text-gray-500">
                        {{ form.appointment_date ? new Date(form.appointment_date).toLocaleDateString() : 'No date selected' }}
                      </p>
                    </div>
                  </div>
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
              {{ editMode ? 'Update Reminder' : 'Create Reminder' }}
            </button>
          </div>
        </div>
      </form>
    </div>
    <!-- Header Section -->
    <div class="space-y-4">
      <div class="flex items-center justify-between mb-2">
        <div>
          <p class="text-sm text-gray-600">Manage reminders and follow-up tasks for this client to ensure timely communication.</p>
        </div>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ reminders.length }} {{ reminders.length === 1 ? 'reminder' : 'reminders' }}</span>
      </div>

      <!-- Add Reminder Button -->
      <div class="flex justify-start mb-2">
        <button class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-150" @click="formVisible = true">
          <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
          Add Reminder
        </button>
      </div>
    </div>
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!loading && reminders.length === 0" class="text-center py-12">
      <font-awesome-icon icon="bell-slash" class="text-4xl text-gray-300 mb-4" />
      <h5 class="text-lg font-medium text-gray-900 mb-2">No Reminders Found</h5>
      <p class="text-gray-500 mb-4">This client doesn't have any reminders yet.</p>
      <button class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-150" @click="formVisible = true">
        <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
        Create First Reminder
      </button>
    </div>

    <!-- Reminder Cards -->
    <div v-else class="space-y-4">
      <div v-for="reminder in reminders" :key="reminder.id" class="group relative bg-gray-50 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 p-4">
        <div class="flex items-start justify-between">
          <!-- Main Content -->
          <div class="flex items-start space-x-4 flex-1">
            <!-- Date and Status -->
            <div class="flex-shrink-0">
              <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors duration-200">
                <font-awesome-icon icon="calendar-alt" class="text-blue-600" />
              </div>
              <div class="mt-2 flex justify-center">
                <span v-if="reminder.global_reminder" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  <font-awesome-icon icon="eye" class="mr-1" />
                  Global
                </span>
                <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  <font-awesome-icon icon="user" class="mr-1" />
                  Personal
                </span>
              </div>
            </div>

            <!-- Reminder Details -->
            <div class="flex-1 min-w-0">
              <!-- Date -->
              <div class="mb-3">
                <h5 class="text-base font-semibold text-gray-900 group-hover:text-blue-900">
                  {{ reminder.appointment_date ? toLocaleDate(reminder.appointment_date) : 'No date set' }}
                </h5>
                <div class="flex items-center text-sm text-gray-500 group-hover:text-blue-700 mt-1">
                  <font-awesome-icon icon="clock" class="mr-1.5" />
                  Reminder scheduled
                </div>
              </div>

              <!-- Reason Details -->
              <div class="bg-white rounded-lg p-3 border border-gray-100">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-full bg-yellow-100 flex items-center justify-center">
                    <font-awesome-icon :icon="reminder.icon || 'bell'" class="text-yellow-600 text-sm" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm font-medium text-gray-900">{{ reminder.reason }}</p>
                    <p v-if="reminder.reason === 'OTHER' && reminder.other_reason" class="text-xs text-gray-500 mt-1">
                      {{ reminder.other_reason }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex-shrink-0 ml-4">
            <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <!-- Edit Button -->
              <button @click="onEdit(reminder)" class="inline-flex items-center px-3 py-2 text-xs font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg border border-blue-200 hover:border-blue-300 transition-all duration-150 hover:shadow-sm" title="Edit reminder">
                <font-awesome-icon :icon="['fas', 'edit']" class="mr-1.5" />
                Edit
              </button>

              <!-- Delete Button -->
              <button @click="onDelete(reminder)" class="inline-flex items-center px-3 py-2 text-xs font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-lg border border-red-200 hover:border-red-300 transition-all duration-150 hover:shadow-sm" title="Delete reminder">
                <font-awesome-icon :icon="['fas', 'trash']" class="mr-1.5" />
                Delete
              </button>
            </div>

            <!-- Mobile/Always Visible Actions (for smaller screens) -->
            <div class="md:hidden flex items-center space-x-1">
              <button @click="onEdit(reminder)" class="inline-flex items-center justify-center w-8 h-8 text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-full border border-blue-200 hover:border-blue-300 transition-all duration-150" title="Edit reminder">
                <font-awesome-icon :icon="['fas', 'edit']" class="text-xs" />
              </button>

              <button @click="onDelete(reminder)" class="inline-flex items-center justify-center w-8 h-8 text-red-600 bg-red-50 hover:bg-red-100 rounded-full border border-red-200 hover:border-red-300 transition-all duration-150" title="Delete reminder">
                <font-awesome-icon :icon="['fas', 'trash']" class="text-xs" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Form from '@/core/utils/Form';

import VueDatePicker from '@vuepic/vue-datepicker';

import { ArrowPathIcon } from '@heroicons/vue/24/outline';

export default {
  props: {
    client: {
      type: Object,
      required: null,
    },
  },
  components: {
    VueDatePicker,
    ArrowPathIcon,
  },
  data() {
    return {
      loading: false,
      formVisible: false,
      editMode: false,

      form: new Form({
        id: null,
        consistency_token: '00000000',
        appointment_date: null,
        reason: null,
        other_reason: null,
        global_reminder: false,
      }),
      reminders: [],
    };
  },
  computed: {},
  methods: {
    ...mapActions('clients', ['getReminderReasons', 'getReminders']),
    ...mapActions('planning', ['createReminder', 'updateReminder', 'deleteReminder']),

    itemProvider() {
      this.loading = true;
      this.getReminders(this.client.id)
        .then((response) => {
          this.reminders = response;
        })
        .catch((errors) => {
          this.formatErrors(errors.response);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onSubmit() {
      const action = this.editMode ? this.updateReminder : this.createReminder;
      const payload = this.editMode ? { id: this.form.id, ...this.form } : { client: this.client.id, ...this.form };

      action(payload)
        .then(() => {
          this.formVisible = false;
          this.editMode = false;
          this.resetForm();
          this.itemProvider();
          const message = this.editMode ? 'Reminder updated successfully!' : 'Reminder created successfully!';
          this.toastSuccess(message);
        })
        .catch((errors) => {
          console.log(errors);
          this.toastError('An error occurred while saving the reminder.');
        });
    },

    resetForm() {
      this.form.reset();
      this.editMode = false;
    },

    onEdit(reminder) {
      this.editMode = true;
      this.form.populate(reminder);
      this.formVisible = true;
    },

    onDelete(reminder) {
      // Add confirmation dialog for better UX

      this.deleteReminder(reminder.id)
        .then(() => {
          this.itemProvider();
          this.toastSuccess('Reminder deleted successfully!');
        })
        .catch((error) => {
          console.error(error);
          this.toastError('An error occurred while deleting the reminder.');
        });
    },
    cancel() {
      this.formVisible = false;
      this.editMode = false;
      this.resetForm();
    },
  },
  mounted() {
    this.itemProvider();
  },
  created() {
    this.getReminderReasons().then((data) => {
      this.reasons = data;
    });
  },
  async beforeRouteEnter(to, from, next) {
    return next();
  },
};
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

/* Custom checkbox styling */
input[type='checkbox']:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e");
}

/* Smooth hover transitions for form elements */
.group:hover .w-6 {
  transform: scale(1.1);
  transition: transform 0.2s ease-in-out;
}

/* Enhanced focus states */
input:focus,
select:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Button hover effects */
button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}
</style>
