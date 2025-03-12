<template>
	<div>
		<!-- Modal -->
		<div v-if="visible" class="fixed top-0 left-0 right-0 bottom-0 z-50 flex items-center justify-center w-full h-full bg-gradient-to-t from-gray-700">
			<div class="relative p-4 w-full max-w-6xl max-h-full">
				<!-- Modal content -->
				<div class="relative bg-white rounded-lg shadow-sm">
					<!-- Modal header -->
					<div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-gray-200">
						<h3 class="text-xl font-semibold text-gray-900">
							<font-awesome-icon :icon="['fas', 'calendar-days']" />
							Appointments
						</h3>

						<button @click="close" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center">
							<font-awesome-icon :icon="['fas', 'xmark']" />
							<span class="sr-only">Close modal</span>
						</button>
					</div>

					<!-- Modal body -->
					<div class="p-4 md:p-5 space-y-4">
						<div class="grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
							<div class="sm:col-span-2">
								<label for="appointment_date" class="block text-sm/6 font-medium text-gray-900">Appointment Date</label>
								<div class="mt-2">
									<div class="flex items-center rounded-md bg-gray-200 pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
										<input type="text" name="appointment_date" id="appointment_date" v-model="appointmentDate" disabled class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="e.g. John" />
									</div>
								</div>
							</div>
							<div class="sm:col-span-2">
								<label for="name" class="block text-sm/6 font-medium text-gray-900">Start Time</label>
								<div class="mt-2">
									<select id="start_time" v-model="start_time" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
										<option v-for="time in startTimes" :key="time" :value="time">{{ time }}</option>
									</select>
								</div>
							</div>
							<div class="sm:col-span-2">
								<label for="name" class="block text-sm/6 font-medium text-gray-900">End Time</label>
								<div class="mt-2">
									<select id="end_time" v-model="end_time" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
										<option v-for="time in endTimes" :key="time" :value="time">{{ time }}</option>
									</select>
								</div>
							</div>
							<div class="sm:col-span-2">
								<label for="name" class="block text-sm/6 font-medium text-gray-900">Service Type</label>
								<div class="mt-2">
									<select id="service_types" v-model="type" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
										<option v-for="type in serviceTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
									</select>
								</div>
							</div>
							<div class="sm:col-span-2">
								<label for="name" class="block text-sm/6 font-medium text-gray-900">Service</label>
								<div class="mt-2">
									<select id="service_types" v-model="form.service" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
										<option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
									</select>
								</div>
							</div>
							<div class="sm:col-span-2">
								<label for="name" class="block text-sm/6 font-medium text-gray-900">Employee</label>
								<div class="mt-2">
									<select id="service_types" v-model="form.employee" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
										<option v-for="employee in employees" :key="employee.id" :value="employee.id">{{ employee.name }}</option>
									</select>
								</div>
							</div>
						</div>
					</div>

					<!-- Modal footer -->
					<div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b">
						<button @click="submit" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Submit</button>
						<button @click="close" class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100">Cancel</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import store from "@/store";
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
			config: {},
			event: null,

			form: new Form({
				start: null,
				end: null,
				client: null,
				service: null,
				charges: null,
				employee: null,
			}),

			start_time: null,
			end_time: null,
			type: null,

			intervalTime: [],
			serviceTypes: [],
			services: [],
			employees: [],
		};
	},
	watch: {
		event: {
			handler(val) {
				if (val) {
					this.start_time = moment(val.start).format("HH:mm");
					// console.log("start_time:", this.start_time);
					this.end_time = moment(val.end).format("HH:mm");
					// console.log("end_time:", this.end_time);
				}
			},
		},
		start_time: {
			handler(val) {
				if (val) {
					var date = moment(this.event.start);
					date.set({ h: moment(val, "HH:mm").get("h"), m: moment(val, "HH:mm").get("m") });
					this.form.start = date.toISOString(true);
					// console.log(this.form.data());
				}
			},
		},
		end_time: {
			handler(val) {
				if (val) {
					var date = moment(this.event.start);
					date.set({ h: moment(val, "HH:mm").get("h"), m: moment(val, "HH:mm").get("m") });
					this.form.end = date.toISOString(true);
					// console.log(this.form.data());ß
				}
			},
		},
		type: {
			async handler(val) {
				if (val) {
					this.services = await this.getServicesByType(val);
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
	},
	methods: {
		...mapActions("services", ["getServiceTypes", "getServicesByType"]),
		...mapActions("planning", ["getConfig", "loadIntervalTime"]),
		toggle() {
			this.visible = !this.visible;
		},
		close() {
			this.event = null;
			this.start_time = null;
			this.end_time = null;
			this.type = null;
			this.form.reset();
			this.visible = false;
		},
		submit() {},
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
