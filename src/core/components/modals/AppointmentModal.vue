<template>
  <div>
    <!-- Modal backdrop with fixed position and overflow hidden -->
    <div v-if="visible" class="fixed inset-0 z-50 backdrop-blur-sm overflow-hidden">
      <!-- Modal container with scrollable content -->
      <div class="fixed inset-0 bg-gradient-to-t from-gray-700 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative w-full max-w-6xl">
            <!-- Modal content -->
            <div class="relative bg-white rounded-xl shadow-lg max-h-[90vh] flex flex-col border border-gray-200">
              <div class="absolute right-0 top-0 hidden pt-4 pr-4 sm:block">
                <!-- Close button -->
              </div>
              <!-- Modal header (stays fixed) -->
              <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-gray-200">
                <div class="px-6">
                  <h3 class="text-2xl font-semibold text-gray-900 mb-1">
                    <font-awesome-icon :icon="['fas', 'calendar-days']" />
                    Appointment Details
                  </h3>
                  <p class="text-sm text-gray-500">Review and modify the appointment information below.</p>
                </div>

                <button @click="close" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center">
                  <font-awesome-icon :icon="['fas', 'xmark']" />
                  <span class="sr-only">Close modal</span>
                </button>
              </div>

              <!-- Modal body (scrollable) -->
              <div class="px-6 py-4 bg-gray-50 overflow-y-auto flex-1">
                <div class="mt-8 grid grid-cols-1 gap-x-6 gap-y-6">
                  <div class="space-y-6">
                    <!-- Appointment Scheduling Card -->
                    <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
                      <div class="px-6 py-4 border-b border-gray-200">
                        <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                          <font-awesome-icon :icon="['fas', 'calendar-clock']" class="mr-3 text-blue-600" />
                          Schedule & Timing
                        </h3>
                        <p class="mt-1 text-sm text-gray-600">Set the appointment date and duration</p>
                      </div>

                      <div class="p-6 space-y-6">
                        <!-- Appointment Date -->
                        <div class="space-y-2">
                          <label class="flex items-center text-sm font-medium text-gray-900">
                            <font-awesome-icon :icon="['fas', 'calendar']" class="mr-2 text-gray-400" />
                            Date
                          </label>
                          <div class="relative">
                            <VueDatePicker hide-input-icon v-model="appointmentDate" :enable-time-picker="false" :min-date="new Date()" format="MMMM d, yyyy" class="block w-full" :disabled="true" input-class-name="rounded-lg border border-gray-300 bg-gray-50 py-3  pr-4 text-sm text-gray-600 cursor-not-allowed" />
                          </div>
                          <p class="text-xs text-gray-500 flex items-center">
                            <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1" />
                            Date cannot be changed from this view
                          </p>
                        </div>

                        <!-- Time Selection -->
                        <div class="grid grid-cols-2 gap-4">
                          <!-- Start Time -->
                          <div class="space-y-2">
                            <label for="start_time" class="flex items-center text-sm font-medium text-gray-900">Start Time</label>
                            <div class="relative">
                              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <font-awesome-icon :icon="['fas', 'clock']" class="text-gray-400" />
                              </div>
                              <select id="start_time" v-model="start_time" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                                <option v-for="time in startTimes" :key="time" :value="time">{{ time }}</option>
                              </select>
                            </div>
                          </div>

                          <!-- End Time -->
                          <div class="space-y-2">
                            <label for="end_time" class="flex items-center text-sm font-medium text-gray-900">End Time</label>
                            <div class="relative">
                              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <font-awesome-icon :icon="['fas', 'hourglass-end']" class="text-gray-400" />
                              </div>
                              <select id="end_time" v-model="end_time" @change="calculateStartTime" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                                <option v-for="time in endTimes" :key="time" :value="time">{{ time }}</option>
                              </select>
                            </div>
                          </div>
                        </div>

                        <!-- Duration Display -->
                        <div v-if="start_time && end_time" class="p-3 bg-blue-50 rounded-lg border border-blue-200">
                          <div class="flex items-center justify-between">
                            <div class="flex items-center text-sm text-blue-700">
                              <font-awesome-icon :icon="['fas', 'clock']" class="mr-2" />
                              <span class="font-medium">Total Duration</span>
                            </div>
                            <span class="text-sm font-semibold text-blue-800">{{ Math.floor(totalTime / 60) }}h {{ totalTime % 60 }}m</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="">
                    <!-- Client Selection -->
                    <div v-if="client" class="sm:col-span-12">
                      <!-- Client Information Card -->
                      <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
                        <div class="border-b border-gray-200 p-4 flex items-center justify-between">
                          <h4 class="text-lg font-semibold text-gray-900">Client Information</h4>
                          <button :disabled="true" class="text-sm text-gray-200">
                            <font-awesome-icon :icon="['fas', 'user-edit']" class="me-2" />
                            Change Client
                          </button>
                        </div>
                        <div class="p-6">
                          <!-- Client Header -->
                          <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center space-x-3">
                              <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                                <font-awesome-icon :icon="['fas', client.gender === 'MALE' ? 'mars' : client.gender === 'FEMALE' ? 'venus' : 'venus-mars']" class="text-blue-600 text-xl" />
                              </div>
                              <div>
                                <h3 class="text-lg font-semibold text-gray-900">{{ client.display }}</h3>
                                <p class="text-sm text-gray-500">Client ID: {{ client.id }}</p>
                              </div>
                            </div>
                          </div>

                          <!-- Client Details Grid -->
                          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-4">
                            <!-- Basic Information -->
                            <div class="space-y-3">
                              <div class="flex items-center space-x-3">
                                <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center">
                                  <font-awesome-icon :icon="['fas', 'cake-candles']" class="text-blue-600" />
                                </div>
                                <div>
                                  <p class="text-xs text-gray-500">Date of Birth</p>
                                  <p class="text-sm font-medium text-gray-900">
                                    {{ client.date_of_birth ? toLocaleDate(client.date_of_birth) : 'n/a' }}
                                  </p>
                                </div>
                              </div>
                              <div class="flex items-center space-x-3">
                                <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center">
                                  <font-awesome-icon :icon="['fas', 'phone']" class="text-blue-600" />
                                </div>
                                <div>
                                  <p class="text-xs text-gray-500">Phone</p>
                                  <p class="text-sm font-medium text-gray-900">{{ client.mobile || 'n/a' }}</p>
                                </div>
                              </div>
                              <div class="flex items-center space-x-3">
                                <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center">
                                  <font-awesome-icon :icon="['fas', 'at']" class="text-blue-600" />
                                </div>
                                <div>
                                  <p class="text-xs text-gray-500">Email</p>
                                  <p class="text-sm font-medium text-gray-900">{{ client.email || 'n/a' }}</p>
                                </div>
                              </div>
                            </div>

                            <!-- Timeline Information -->
                            <div class="col-span-2 grid grid-cols-3 gap-4 bg-gray-50 rounded-lg p-4">
                              <div class="text-center">
                                <div class="w-8 h-8 rounded-full bg-blue-50 mx-auto mb-2 flex items-center justify-center">
                                  <font-awesome-icon :icon="['fas', 'person-circle-plus']" class="text-blue-600" />
                                </div>
                                <p class="text-xs text-gray-500">Client Since</p>
                                <p class="text-sm font-medium text-gray-900">
                                  {{ client.created ? toLocaleDateTime(client.created) : 'n/a' }}
                                </p>
                              </div>
                              <div class="text-center">
                                <div class="w-8 h-8 rounded-full bg-blue-50 mx-auto mb-2 flex items-center justify-center">
                                  <font-awesome-icon :icon="['fas', 'clock-rotate-left']" class="text-blue-600" />
                                </div>
                                <p class="text-xs text-gray-500">Last Visit</p>
                                <p class="text-sm font-medium text-gray-900">
                                  {{ client.last_appointment ? toLocaleDateTime(client.last_appointment) : 'No previous visits' }}
                                </p>
                              </div>
                              <div class="text-center">
                                <div class="w-8 h-8 rounded-full bg-blue-50 mx-auto mb-2 flex items-center justify-center">
                                  <font-awesome-icon :icon="['far', 'calendar-check']" class="text-blue-600" />
                                </div>
                                <p class="text-xs text-gray-500">Next Visit</p>
                                <p class="text-sm font-medium text-gray-900">
                                  {{ client.next_appointment ? toLocaleDateTime(client.next_appointment) : 'No upcoming visits' }}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- <div v-else class="sm:col-span-12">
                    <button @click="toggleClientTable" class="w-full p-4 flex items-center justify-between text-left text-gray-900 font-medium border border-gray-200 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-300 transition-colors duration-150">
                      <div class="flex items-center space-x-3">
                        <div class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center">
                          <font-awesome-icon :icon="['fas', 'user-plus']" class="text-blue-600" />
                        </div>
                        <p class="text-sm text-blue-600">Select Client</p>
                      </div>
                      <font-awesome-icon :icon="['fas', 'chevron-down']" class="text-gray-400" :class="{ 'rotate-180': clientTableVisible }" />
                    </button>
                    <transition name="fade"></transition>
                    <div v-if="clientTableVisible" class="mt-4">
                      <QuickClientTable @selected-client="onSelectedClient" />
                    </div>
                  </div> -->

                    <!-- Service Selection Section -->
                    <div class="pt-6">
                      <!-- Location & Details Card -->
                      <div class="bg-white border border-gray-200 rounded-xl shadow-sm">
                        <div class="px-6 py-4 border-b border-gray-200">
                          <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                            <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-3 text-blue-600" />
                            Location & Notes
                          </h3>
                          <p class="mt-1 text-sm text-gray-600">Specify service location and additional details</p>
                        </div>

                        <div class="p-6 space-y-6">
                          <!-- Location Type Toggle -->
                          <div class="space-y-4">
                            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                              <div class="flex items-center space-x-3">
                                <div class="w-10 h-10 rounded-full flex items-center justify-center transition-colors duration-200" :class="form.is_onsite ? 'bg-green-100' : 'bg-blue-100'">
                                  <font-awesome-icon :icon="['fas', form.is_onsite ? 'location-dot' : 'building']" :class="form.is_onsite ? 'text-green-600' : 'text-blue-600'" />
                                </div>
                                <div>
                                  <p class="font-medium text-gray-900">
                                    {{ form.is_onsite ? 'On-site Service' : 'In-office Service' }}
                                  </p>
                                  <p class="text-sm text-gray-500">
                                    {{ form.is_onsite ? 'Service will be provided at client location' : 'Client will visit your location' }}
                                  </p>
                                </div>
                              </div>
                              <div class="flex items-center">
                                <input id="onsite" type="checkbox" v-model="form.is_onsite" @change="onSiteChange" class="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 transition-colors duration-200" />
                                <label for="onsite" class="ml-3 text-sm font-medium text-gray-700">On-site</label>
                              </div>
                            </div>

                            <!-- Address Input (shown when on-site is selected) -->
                            <div v-if="form.is_onsite" class="space-y-2 animate-fadeIn">
                              <label for="onsite_address" class="flex items-center text-sm font-medium text-gray-900">
                                <font-awesome-icon :icon="['fas', 'map-pin']" class="mr-2 text-gray-400" />
                                Service Address
                              </label>
                              <div class="relative">
                                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <font-awesome-icon :icon="['fas', 'home']" class="text-gray-400" />
                                </div>
                                <input type="text" list="onsite-address-list" name="onsite_address" id="onsite_address" v-model="form.onsite_address" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500/20 transition-all duration-200" placeholder="Enter the service address (e.g., 123 Main Street, City)" />
                                <datalist id="onsite-address-list">
                                  <option v-for="(item, index) in addresses" :key="index">{{ item.address }}</option>
                                </datalist>
                              </div>
                              <div v-if="addresses.length > 0" class="flex flex-wrap gap-2 mt-2">
                                <span class="text-xs text-gray-500">Recent addresses:</span>
                                <button v-for="(address, index) in addresses.slice(0, 3)" :key="index" @click="form.onsite_address = address.address" class="inline-flex items-center px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full hover:bg-green-200 transition-colors duration-150">
                                  <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-1" />
                                  {{ address.address.length > 30 ? address.address.substring(0, 30) + '...' : address.address }}
                                </button>
                              </div>
                            </div>
                          </div>

                          <!-- Notes Section -->
                          <div class="space-y-2">
                            <label for="notes" class="flex items-center text-sm font-medium text-gray-900">
                              <font-awesome-icon :icon="['fas', 'sticky-note']" class="mr-2 text-gray-400" />
                              Additional Notes
                            </label>
                            <div class="relative">
                              <textarea id="notes" v-model="form.notes" class="block w-full rounded-lg border border-gray-300 bg-white py-3 px-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 resize-none" rows="4" placeholder="Add any special instructions, preferences, or important notes for this appointment..."></textarea>
                              <div class="absolute bottom-3 right-3 text-xs text-gray-400 pointer-events-none">{{ form.notes?.length || 0 }}/500</div>
                            </div>
                            <p class="text-xs text-gray-500 flex items-center">
                              <font-awesome-icon :icon="['fas', 'lightbulb']" class="mr-1" />
                              Include client preferences, special requirements, or preparation instructions
                            </p>
                          </div>
                        </div>
                      </div>

                      <div class="bg-white border border-gray-200 rounded-xl shadow-sm mt-6">
                        <div class="px-6 py-4 border-b border-gray-200">
                          <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                            <font-awesome-icon :icon="['fas', 'scissors']" class="mr-3 text-blue-600" />
                            Service Details
                          </h3>
                          <p class="mt-1 text-sm text-gray-600">Configure the service and assign a team member</p>
                        </div>

                        <div class="p-6 space-y-6">
                          <!-- Service Type and Service Selection -->
                          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <!-- Service Type -->
                            <div class="space-y-2">
                              <label for="service_type" class="block text-sm font-medium text-gray-900">
                                <font-awesome-icon :icon="['fas', 'tags']" class="mr-2 text-gray-400" />
                                Service Category
                              </label>
                              <div class="relative">
                                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <font-awesome-icon :icon="['fas', 'layer-group']" class="text-gray-400" />
                                </div>
                                <select id="service_type" v-model="type" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200">
                                  <option :value="null" disabled>Choose a service category</option>
                                  <option v-for="serviceType in serviceTypes" :key="serviceType.id" :value="serviceType.id">
                                    {{ serviceType.name }}
                                  </option>
                                </select>
                              </div>
                              <p v-if="!type" class="text-xs text-gray-500 flex items-center mt-1">
                                <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1" />
                                Select a category to see available services
                              </p>
                            </div>

                            <!-- Service Selection -->
                            <div class="space-y-2">
                              <label for="service" class="block text-sm font-medium text-gray-900">
                                <font-awesome-icon :icon="['fas', 'cut']" class="mr-2 text-gray-400" />
                                Service
                              </label>
                              <div class="relative">
                                <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <font-awesome-icon :icon="['fas', 'scissors']" class="text-gray-400" />
                                </div>
                                <select id="service" v-model="form.service" :disabled="!type || services.length === 0" @change="onServiceChange" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed">
                                  <option :value="null" disabled>
                                    {{ !type ? 'Select a category first' : 'Choose a service' }}
                                  </option>
                                  <option v-for="service in services" :key="service.id" :value="service.id">
                                    {{ service.name }}
                                  </option>
                                </select>
                              </div>

                              <!-- Service Details -->
                              <div v-if="selectedService" class="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                                <div class="flex items-center justify-between">
                                  <div class="flex items-center space-x-4">
                                    <div class="flex items-center text-sm text-blue-700">
                                      <font-awesome-icon :icon="['fas', 'clock']" class="mr-2" />
                                      <span class="font-medium">{{ selectedService.time_display }}</span>
                                    </div>
                                    <div class="flex items-center text-sm text-blue-700">
                                      <font-awesome-icon :icon="['fas', 'dollar-sign']" class="mr-2" />
                                      <span class="font-semibold">${{ selectedService.price }}</span>
                                    </div>
                                  </div>
                                  <div class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full">Base Service</div>
                                </div>
                                <p v-if="selectedService.description" class="mt-2 text-xs text-blue-600">
                                  {{ selectedService.description }}
                                </p>
                              </div>
                            </div>
                          </div>

                          <!-- Employee Assignment -->
                          <div class="space-y-2">
                            <label for="employee" class="block text-sm font-medium text-gray-900">
                              <font-awesome-icon :icon="['fas', 'user-tie']" class="mr-2 text-gray-400" />
                              Assigned Team Member
                            </label>
                            <div class="relative">
                              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                <font-awesome-icon :icon="['fas', 'user']" class="text-gray-400" />
                              </div>
                              <select id="employee" v-model="form.employee" :disabled="!type || employees.length === 0" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-10 text-sm text-gray-900 shadow-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 disabled:bg-gray-50 disabled:cursor-not-allowed">
                                <option :value="null" disabled>
                                  {{ !type ? 'Select a service first' : employees.length === 0 ? 'No available team members' : 'Assign to team member' }}
                                </option>
                                <option v-for="employee in employees" :key="employee.id" :value="employee.id">
                                  {{ employee.name }}
                                </option>
                              </select>
                            </div>
                            <p v-if="employees.length === 0 && type" class="text-xs text-amber-600 flex items-center mt-1">
                              <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="mr-1" />
                              No team members available for this service type
                            </p>
                          </div>
                        </div>
                      </div>

                      <!-- Additional Services Section -->
                      <div v-if="selectedService" class="mt-6 bg-white border border-gray-200 rounded-xl shadow-sm">
                        <div class="px-6 py-4 border-b border-gray-200">
                          <div class="flex items-center justify-between">
                            <div>
                              <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                                <font-awesome-icon :icon="['fas', 'plus-circle']" class="mr-3 text-blue-600" />
                                Additional Services
                              </h3>
                              <p class="mt-1 text-sm text-gray-600">Enhance the appointment with optional add-ons</p>
                            </div>
                            <div v-if="form.addons.length > 0" class="text-right">
                              <div class="text-sm font-medium text-gray-900">{{ form.addons.length }} selected</div>
                              <div class="text-xs text-gray-500">+${{ totalAddonCost }}</div>
                            </div>
                          </div>
                        </div>

                        <div class="p-6">
                          <!-- Search Bar -->
                          <div class="relative mb-6">
                            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                              <font-awesome-icon :icon="['fas', 'search']" class="text-gray-400" />
                            </div>
                            <input v-model="addonSearch" type="search" class="block w-full rounded-lg border border-gray-300 bg-white py-3 pl-10 pr-4 text-sm text-gray-900 shadow-sm placeholder-gray-500 hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-200" placeholder="Search for additional services..." />
                          </div>

                          <!-- Add-ons Grid -->
                          <div v-if="filteredAddons.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div v-for="(addon, index) in filteredAddons" :key="addon.id" class="group relative flex items-start p-4 bg-gray-50 border-2 border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 cursor-pointer" :class="{ 'border-blue-500 bg-blue-50': form.addons.includes(addon.id) }" @click="toggleAddon(addon.id)">
                              <div class="flex items-center h-5">
                                <input :id="`addon-checkbox-${index}`" type="checkbox" :checked="form.addons" :value="addon.id" v-model="form.addons" class="w-5 h-5 text-blue-600 border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 transition-colors duration-200" @change="handleTimespanChange" @click.stop />
                              </div>
                              <div class="ml-4 flex-1 min-w-0">
                                <label :for="`addon-checkbox-${index}`" class="cursor-pointer">
                                  <div class="flex items-center justify-between mb-2">
                                    <h4 class="text-sm font-semibold text-gray-900 group-hover:text-blue-800 transition-colors duration-200">
                                      {{ addon.name }}
                                    </h4>
                                    <span class="text-lg font-bold text-blue-600">${{ addon.price }}</span>
                                  </div>
                                  <div class="flex items-center text-xs text-gray-600 mb-2">
                                    <font-awesome-icon :icon="['fas', 'clock']" class="mr-2" />
                                    <span>{{ addon.time_display }}</span>
                                  </div>
                                  <p v-if="addon.description" class="text-xs text-gray-500 line-clamp-2">
                                    {{ addon.description }}
                                  </p>
                                </label>
                              </div>
                            </div>
                          </div>

                          <!-- No Add-ons Available -->
                          <div v-else-if="addons.length === 0" class="text-center py-12">
                            <font-awesome-icon :icon="['fas', 'spa']" class="text-4xl text-gray-300 mb-4" />
                            <h3 class="text-lg font-medium text-gray-900 mb-2">No Additional Services Available</h3>
                            <p class="text-gray-500">This service type doesn't have any optional add-ons.</p>
                          </div>

                          <!-- No Search Results -->
                          <div v-else class="text-center py-8">
                            <font-awesome-icon :icon="['fas', 'search']" class="text-3xl text-gray-300 mb-3" />
                            <h3 class="text-md font-medium text-gray-900 mb-1">No matches found</h3>
                            <p class="text-sm text-gray-500">Try adjusting your search terms.</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="border-t border-gray-100 px-6 py-4">
                <div class="flex items-center justify-between">
                  <div class="text-xs text-gray-500">
                    <font-awesome-icon :icon="['fas', 'info-circle']" class="mr-1" />
                    This will update the appointment details
                  </div>
                  <div class="flex items-center space-x-3">
                    <button @click="close" class="px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-150 min-w-[90px]">
                      <font-awesome-icon :icon="['fas', 'times']" />
                      Cancel
                    </button>
                    <button @click="submit" class="px-4 py-2.5 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600 min-w-[120px] flex items-center justify-center space-x-2">
                      <font-awesome-icon :icon="['fas', 'save']" />
                      <span>Save Changes</span>
                    </button>
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
import moment from 'moment';

import Form from '@/core/utils/Form';

import VueDatePicker from '@vuepic/vue-datepicker';
import { mapActions } from 'vuex';

export default {
  components: {
    VueDatePicker,
  },
  data() {
    return {
      visible: false,
      clientsVisible: false,

      config: {},
      event: null,
      appointment: null,

      form: new Form({
        consistency_token: '00000000',
        start: null,
        end: null,
        client: null,
        is_onsite: false,
        onsite_address: null,
        service: null,
        service_price: null,
        employee: null,
        addons: [],
        notes: null,
      }),

      start_time: null,
      end_time: null,
      type: null,
      client: null,
      addresses: [],
      addonSearch: '',

      intervalTime: [],
      serviceTypes: [],
      services: [],
      addons: [],
      employees: [],
    };
  },
  watch: {
    event: {
      async handler(val) {
        if (val) {
          const timezone = 'America/Paramaribo';
          this.start_time = moment.tz(val.start, timezone).format('HH:mm');
          this.end_time = moment.tz(val.end, timezone).format('HH:mm');

          this.form.populate(val.extendedProps);

          this.form.onsite_address = val.extendedProps.onsite_address_details;

          // Load client
          this.client = await this.getClientById(val.extendedProps.client);
          if (this.client.known_addresses) {
            this.addresses = this.client.known_addresses;
          }

          // Load services and addons
          const service = await this.getServiceById(val.extendedProps.service);
          this.type = service.type.id;
          this.addons = await this.getAddonsByType(this.type);
        }
      },
    },
    start_time: {
      handler(val) {
        if (val) {
          const timezone = 'America/Paramaribo';
          var date = moment.tz(this.event.start, timezone);
          const time = moment.tz(val, 'HH:mm', timezone);
          date.set({ h: time.get('h'), m: time.get('m') });
          this.form.start = date.format();
        }
      },
    },
    end_time: {
      handler(val) {
        if (val) {
          var date = moment(this.event.end);
          date.set({ h: moment(val, 'HH:mm').get('h'), m: moment(val, 'HH:mm').get('m') });
          this.form.end = date.toISOString(true);
        }
      },
    },
    type: {
      async handler(val) {
        if (val) {
          this.services = await this.getServicesByType(val);
          this.addons = await this.getAddonsByType(val);
          this.employees = await this.getEmployeesByServiceType(val);
          this.form.service = this.services[0] ? this.services[0]?.id : null;

          if (!this.form.employee) {
            this.form.employee = this.employees[0] ? this.employees[0]?.id : null;
          }
        }
      },
    },
  },
  computed: {
    appointmentDate() {
      return this.toFullDate(this.event?.start);
    },
    eventStart() {
      return this.start_time;
    },
    eventEnd() {
      return this.end_time;
    },
    startTimes() {
      if (this.eventEnd) {
        let slice = this.intervalTime.findIndex((time) => time === this.eventEnd);
        return this.intervalTime.slice(0, slice);
      }
      return this.intervalTime;
    },
    endTimes() {
      if (this.eventStart) {
        let slice = this.intervalTime.findIndex((time) => time === this.eventStart);
        return this.intervalTime.slice(slice + 1, this.intervalTime.length);
      }
      return this.intervalTime;
    },
    totalTime() {
      let totalMinutes = 0;
      totalMinutes += this.selectedService?.duration.hours * 60 + this.selectedService?.duration.minutes;

      this.form.addons.forEach((addonId) => {
        const selectedAddon = this.addons.find((a) => a.id === addonId);
        if (selectedAddon) {
          totalMinutes += selectedAddon.additional_time.hours * 60 + selectedAddon.additional_time.minutes;
        }
      });
      return totalMinutes;
    },
    selectedService() {
      return this.services.find((elem) => elem.id == this.form.service);
    },
    filteredAddons() {
      return this.addons.filter((addon) => addon.name.toLowerCase().includes(this.addonSearch.toLowerCase()));
    },
    totalAddonCost() {
      return this.form.addons.reduce((total, addonId) => {
        const addon = this.addons.find((a) => a.id === addonId);
        return total + (addon ? Number(addon.price) : 0);
      }, 0);
    },
  },
  methods: {
    ...mapActions('clients', ['getClientById']),
    ...mapActions('services', ['getServiceById', 'getServiceTypes', 'getServicesByType', 'getAddonsByType']),
    ...mapActions('staff', ['getEmployeesByServiceType']),
    ...mapActions('planning', ['getConfig', 'loadIntervalTime', 'updateAppointment']),
    toggle() {
      this.visible = !this.visible;
    },
    calculateStartTime() {
      const { hours, minutes } = this.selectedService.duration;
      if (this.end_time) {
        const endMoment = moment(this.end_time, 'HH:mm');
        const startMoment = endMoment.clone().subtract(hours, 'hours').subtract(minutes, 'minutes');
        this.start_time = startMoment.format('HH:mm');
      }
    },
    calculateEndTime() {
      const { hours, minutes } = this.selectedService.duration;
      if (this.start_time) {
        const startMoment = moment(this.start_time, 'HH:mm');
        const endMoment = startMoment.clone().add(hours, 'hours').add(minutes, 'minutes');
        this.end_time = endMoment.format('HH:mm');
      }
    },

    onServiceChange() {
      this.form.service_price = this.selectedService.price;
      this.calculateEndTime();
    },
    onSiteChange() {
      this.form.onsite_address = null;
      if (this.form.is_onsite && this.client && this.client.known_addresses && this.client.known_addresses.length > 0) {
        this.form.onsite_address = this.client.known_addresses[0].address;
      }
    },
    calculateTotalDuration() {
      let minutes = 0;
      minutes += this.selectedService.duration.hours * 60 + this.selectedService.duration.minutes;

      this.form.addons.forEach((addonId) => {
        const selectedAddon = this.addons.find((a) => a.id === addonId);
        if (selectedAddon) {
          minutes += selectedAddon.additional_time.hours * 60 + selectedAddon.additional_time.minutes;
        }
      });

      const startMoment = moment(this.start_time, 'HH:mm');
      const endMoment = startMoment.clone().add(minutes, 'minutes');
      this.end_time = endMoment.format('HH:mm');
    },
    calculateTotalCost() {
      let totalCost = 0;
      totalCost += this.selectedService.price;

      this.form.addons.forEach((addonId) => {
        const selectedAddon = this.addons.find((a) => a.id === addonId);
        if (selectedAddon) {
          totalCost += selectedAddon.price;
        }
      });

      this.form.total_cost = totalCost;
    },
    handleTimespanChange() {
      this.calculateTotalDuration();
      this.calculateTotalCost();
    },
    getAddressId(addressText) {
      if (!addressText || !this.addresses) return null;
      const foundAddress = this.addresses.find((addr) => addr.address === addressText);
      return foundAddress ? foundAddress.id : null;
    },
    toggleAddon(addonId) {
      const index = this.form.addons.indexOf(addonId);
      if (index > -1) {
        this.form.addons.splice(index, 1);
      } else {
        this.form.addons.push(addonId);
      }
      this.handleTimespanChange();
    },
    submit() {
      const formData = this.form.data();

      this.updateAppointment({ ...formData, id: this.event.id })
        .then((response) => {
          this.$emit('updated', response);
          this.close();
        })
        .catch((error) => {
          this.$emit('error', 'updating', error);
        });
    },
    close() {
      this.event = null;
      this.appointment = null;
      this.start_time = null;
      this.end_time = null;
      this.type = null;
      this.form.reset();
      this.visible = false;
    },
  },
  async mounted() {
    this.config = await this.getConfig();
    this.intervalTime = await this.loadIntervalTime({
      start: this.config.slot.MIN,
      end: this.config.slot.MAX,
      interval: this.config.slot.INTERVAL,
    });

    this.serviceTypes = await this.getServiceTypes();
  },
};
</script>
