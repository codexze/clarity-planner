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
									<p class="text-sm text-gray-500">View and edit appointment details</p>
								</div>

								<button @click="close" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center">
									<font-awesome-icon :icon="['fas', 'xmark']" />
									<span class="sr-only">Close modal</span>
								</button>
							</div>

							<!-- Modal body (scrollable) -->
							<div class="p-4 md:p-5 space-y-4 overflow-y-auto">
								<div class="grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 p-4">
									<div class="sm:col-span-2 sm:col-start-1">
										<label for="appointment_date" class="block text-sm/6 font-medium text-gray-900">Appointment Date</label>
										<div class="mt-2">
											<VueDatePicker v-model="appointmentDate" :enable-time-picker="false" :min-date="new Date()" format="MMMM d, yyyy" class="w-full" :disabled="true" />
										</div>
									</div>
									<div class="sm:col-span-2">
										<label for="name" class="block text-sm/6 font-medium text-gray-900">Start Time</label>
										<div class="mt-2">
											<select id="start_time" v-model="start_time" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg hover:bg-gray-100 focus:ring-blue-300 focus:border-blue-300 block w-full p-2.5">
												<option v-for="time in startTimes" :key="time" :value="time">{{ time }}</option>
											</select>
										</div>
									</div>
									<div class="sm:col-span-2">
										<label for="name" class="block text-sm/6 font-medium text-gray-900">End Time</label>
										<div class="mt-2">
											<select id="end_time" v-model="end_time" @change="calculateStartTime" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg hover:bg-gray-100 focus:ring-blue-300 focus:border-blue-300 block w-full p-2.5">
												<option v-for="time in endTimes" :key="time" :value="time">{{ time }}</option>
											</select>
										</div>
									</div>
									<div class="sm:col-span-12">
										<label for="notes" class="block text-sm/6 font-medium text-gray-900">Notes</label>
										<div class="mt-2">
											<textarea id="notes" v-model="form.notes" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg hover:bg-gray-100 focus:ring-blue-300 focus:border-blue-300 block w-full p-2.5" rows="3" placeholder="Add any additional notes here..."></textarea>
										</div>
									</div>

									<div v-if="client" class="sm:col-span-12">
										<!-- Client Accordion -->
										<div class="border border-gray-300 hover:border-blue-300 rounded-lg p-3">
											<span class="w-3/4">
												<div>
													<small class="text-gray-500">{{ client.id }}</small>
													{{ client.display }}

													<template v-if="client.gender == 'MALE'">
														<small class="text-gray-500">
															<font-awesome-icon :icon="['fas', 'mars']" />
														</small>
													</template>
													<template v-else-if="client.gender == 'FEMALE'">
														<small class="text-gray-500">
															<font-awesome-icon :icon="['fas', 'venus']" />
														</small>
													</template>
													<template v-else>
														<small class="text-gray-500">
															<font-awesome-icon :icon="['fas', 'venus-mars']" />
														</small>
													</template>
												</div>

												<div class="grid grid-cols-1 gap-x-1 gap-y-2 sm:grid-cols-6 mt-2">
													<div class="sm:col-span-2">
														<p class="text-sm font-normal text-gray-500">
															<font-awesome-icon :icon="['fas', 'cake-candles']" class="text-blue-500" />
															{{ client.date_of_birth ? toLocaleDate(client.date_of_birth) : "n/a" }}
														</p>
													</div>
													<div class="sm:col-span-2">
														<p class="text-sm font-normal text-gray-500">
															<font-awesome-icon :icon="['fas', 'phone']" class="text-blue-500" />
															{{ client.mobile ? client.mobile : "n/a" }}
														</p>
													</div>
													<div class="sm:col-span-2">
														<p class="text-sm font-normal text-gray-500">
															<font-awesome-icon :icon="['fas', 'at']" class="text-blue-500" />
															{{ client.email ? client.email : "n/a" }}
														</p>
													</div>
													<div class="sm:col-span-2">
														<p class="text-xs font-normal text-gray-400">
															<font-awesome-icon :icon="['fas', 'person-circle-plus']" class="text-blue-400" />
															{{ client.created ? toLocaleDateTime(client.created) : "n/a" }}
														</p>
													</div>
													<div class="sm:col-span-2 text-right">
														<p class="text-xs font-normal text-gray-400">
															<font-awesome-icon :icon="['fas', 'clock-rotate-left']" class="text-blue-400" />
															{{ client.last_appointment ? toLocaleDateTime(client.last_appointment) : "no previous appointments" }}
														</p>
													</div>
													<div class="sm:col-span-2 text-right">
														<p class="text-xs font-normal text-gray-400">
															<font-awesome-icon :icon="['far', 'calendar-check']" class="text-blue-400" />
															{{ client.next_appointment ? toLocaleDateTime(client.next_appointment) : "no next appointments" }}
														</p>
													</div>
												</div>
											</span>
										</div>
									</div>

									<div class="sm:col-span-2">
										<label for="onsite_address" class="block text-sm/6 font-medium text-gray-900">Onsite Address</label>
										<div class="mt-2">
											<div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
												<!-- <div class="shrink-0 text-base text-gray-500 select-none sm:text-sm/6">billybob@domain.com</div> -->
												<input type="text" list="onsite-address-list" name="onsite_address" id="onsite_address" v-model="form.onsite_address" :disabled="!form.is_onsite" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 disabled:bg-gray-100 disabled:border-gray-500 disabled:text-gray-700" placeholder="e.g. Surinamestraat 00" />

												<datalist id="onsite-address-list">
													<option v-for="(item, index) in addresses" :key="index">{{ item.address }}</option>
												</datalist>
											</div>
										</div>
									</div>

									<div class="sm:col-span-2">
										<div class="flex items-start mt-8">
											<div class="flex items-center h-5">
												<input id="onsite" type="checkbox" v-model="form.is_onsite" class="w-4 h-4 border border-gray-300 rounded-sm bg-gray-50 focus:ring-3 focus:ring-blue-300" @change="onSiteChange" />
											</div>
											<label for="onsite" class="ms-2 text-sm font-medium text-gray-900">Onsite?</label>
										</div>
									</div>
								</div>

								<div class="grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6 p-4">
									<div class="sm:col-span-2">
										<label for="name" class="block text-sm/6 font-medium text-gray-900">Service Type</label>
										<div class="mt-2">
											<select id="service_types" v-model="type" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg hover:bg-gray-100 focus:ring-blue-300 focus:border-blue-300 block w-full p-2.5">
												<option :value="null">Select a service type.</option>
												<option v-for="type in serviceTypes" :key="type.id" :value="type.id" class="flex items-center">
													{{ type.name }}
												</option>
											</select>
										</div>
									</div>
									<div class="sm:col-span-2">
										<label for="name" class="block text-sm/6 font-medium text-gray-900">Service</label>
										<div class="mt-2">
											<select id="service_types" v-model="form.service" :disabled="!type" @change="onServiceChange" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg hover:bg-gray-100 focus:ring-blue-300 focus:border-blue-300 block w-full p-2.5">
												<option :value="null">Select a service type.</option>
												<option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
											</select>

											<div class="flex items-center justify-between mt-2">
												<p v-if="this.selectedService" class="text-xs text-gray-400 pl-2">
													<font-awesome-icon :icon="['fas', 'plus-minus']" class="text-blue-500" />
													estimated duration:
													{{ this.selectedService.time_display }}
												</p>
												<p v-if="this.selectedService" class="text-xs text-right text-gray-400">
													<span class="text-blue-500">$</span>
													{{ this.selectedService.price }}
												</p>
											</div>
										</div>
									</div>
									<div class="sm:col-span-2">
										<label for="name" class="block text-sm/6 font-medium text-gray-900">Employee</label>
										<div class="mt-2">
											<select id="service_types" v-model="form.employee" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg hover:bg-gray-100 focus:ring-blue-300 focus:border-blue-300 block w-full p-2.5">
												<option :value="null">Select a employee.</option>
												<option v-for="employee in employees" :key="employee.id" :value="employee.id">{{ employee.name }}</option>
											</select>
										</div>
									</div>
									<div class="sm:col-span-12">
										<!-- Addons Section -->
										<div class="">
											<h4 class="text-lg font-medium text-gray-900 mb-4">Additional Services</h4>
											<div class="space-y-4">
												<!-- Search/Filter for addons -->
												<div class="relative">
													<input v-model="addonSearch" type="search" :disabled="!selectedService" class="w-full p-2.5 ps-10 text-sm border border-gray-300 rounded-lg bg-gray-50" placeholder="Search additional services..." />
													<font-awesome-icon :icon="['fas', 'search']" class="absolute left-3 top-3 text-gray-400" />
												</div>

												<!-- Addon items grid -->
												<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
													<div v-for="(addon, index) in filteredAddons" :key="addon.id" class="flex items-center p-3 border rounded-lg hover:bg-gray-50">
														<input :checked="form.addons.includes(addon.id)" :id="`addon-checkbox-${index}`" type="checkbox" :value="addon.id" :name="`addon-checkbox-${addon.id}`" v-model="form.addons" class="w-4 h-4 text-blue-600 rounded border-gray-300" @change="handleAddonChange" />
														<label :for="`addon-checkbox-${index}`" class="w-full ms-2">
															<h5 class="text-sm font-medium text-gray-900">{{ addon.name }}</h5>
															<p class="text-xs text-gray-500">{{ addon.time_display }} • ${{ addon.price }}</p>
														</label>
													</div>
												</div>
											</div>
										</div>
										<!-- Modal footer (stays fixed) -->
										<div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b">
											<button @click="submit" class="text-white bg-blue-500 hover:bg-blue-600 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Submit</button>
											<button @click="close" class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-600 focus:z-10 focus:ring-4 focus:ring-gray-100">Cancel</button>
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
import moment from "moment";

import Form from "@/core/utils/Form";

import VueDatePicker from "@vuepic/vue-datepicker";
import { mapActions } from "vuex";

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
				consistency_token: "00000000",
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
			addonSearch: "",

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
					// console.log("Event start time:", val.start, "Event end time:", val.end);
					// Use moment.tz to ensure correct timezone handling
					const timezone = "America/Paramaribo"; // Match Django settings
					this.start_time = moment.tz(val.start, timezone).format("HH:mm");
					this.end_time = moment.tz(val.end, timezone).format("HH:mm");

					// console.log("Extended props:", val.extendedProps);
					this.form.populate(val.extendedProps);

					// Load client
					this.client = await this.getClientById(val.extendedProps.client);
					if (this.client.known_addresses) {
						this.addresses = this.client.known_addresses;
					}

					// Load services and addons
					const service = await this.getServiceById(val.extendedProps.service);
					this.type = service.type.id;
					this.addons = await this.getAddonsByType(this.type);

					console.log("Loaded form:", this.form.formData());
				}
			},
		},
		start_time: {
			handler(val) {
				if (val) {
					const timezone = "America/Paramaribo"; // Match Django settings
					var date = moment.tz(this.event.start, timezone);
					const time = moment.tz(val, "HH:mm", timezone);
					date.set({ h: time.get("h"), m: time.get("m") });
					this.form.start = date.format(); // Use format() instead of toISOString(true) to preserve timezone
					// console.log("Updated start time:", this.form.start);
				}
			},
		},
		end_time: {
			handler(val) {
				if (val) {
					var date = moment(this.event.end);
					date.set({ h: moment(val, "HH:mm").get("h"), m: moment(val, "HH:mm").get("m") });
					this.form.end = date.toISOString(true);
					// console.log("Updated end time:", this.form.only(["end"]));
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
		selectedService() {
			return this.services.find((elem) => elem.id == this.form.service);
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
		filteredAddons() {
			return this.addons.filter((addon) => addon.name.toLowerCase().includes(this.addonSearch.toLowerCase()));
		},
	},
	methods: {
		...mapActions("clients", ["getClientById"]),
		...mapActions("services", ["getServiceById", "getServiceTypes", "getServicesByType", "getAddonsByType"]),
		...mapActions("staff", ["getEmployeesByServiceType"]),
		...mapActions("planning", ["getConfig", "loadIntervalTime", "updateAppointment"]),
		toggle() {
			this.visible = !this.visible;
		},
		calculateStartTime() {
			const { hours, minutes } = this.selectedService.duration;
			if (this.end_time) {
				const endMoment = moment(this.end_time, "HH:mm");
				const startMoment = endMoment.clone().subtract(hours, "hours").subtract(minutes, "minutes");
				this.start_time = startMoment.format("HH:mm");
			}
		},
		calculateEndTime() {
			const { hours, minutes } = this.selectedService.duration;
			if (this.start_time) {
				const startMoment = moment(this.start_time, "HH:mm");
				const endMoment = startMoment.clone().add(hours, "hours").add(minutes, "minutes");
				this.end_time = endMoment.format("HH:mm");
			}
		},

		onServiceChange() {
			this.form.service_price = this.selectedService.price;
			this.calculateEndTime();
		},
		onSiteChange() {
			// Clear onsite_address when toggling is_onsite
			this.form.onsite_address = null;
			// If switching to onsite and we have a client with known addresses, pre-fill with last used address
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

			// Calculate new end time
			const startMoment = moment(this.start_time, "HH:mm");
			const endMoment = startMoment.clone().add(minutes, "minutes");
			this.end_time = endMoment.format("HH:mm");
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
		handleAddonChange() {
			// Calculate total duration and update end time
			this.calculateTotalDuration();
			// Calculate total cost
			this.calculateTotalCost();
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
		getAddressId(addressText) {
			if (!addressText || !this.addresses) return null;
			const foundAddress = this.addresses.find((addr) => addr.address === addressText);
			return foundAddress ? foundAddress.id : null;
		},
		submit() {
			// Prepare form data with proper onsite_address handling
			const formData = this.form.data();

			// If is_onsite is true, convert address text to ID
			if (formData.is_onsite && formData.onsite_address) {
				formData.onsite_address = this.getAddressId(formData.onsite_address);
			} else {
				formData.onsite_address = null;
			}

			this.updateAppointment({ ...formData, id: this.event.id })
				.then((response) => {
					this.$emit("updated", response);
					this.close();
				})
				.catch((error) => {
					this.$emit("error", "updating", error);
				});
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
