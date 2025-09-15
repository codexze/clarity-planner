<template>
	<div class="relative overflow-y-auto p-2">
		<div
			class="flex items-center justify-between flex-column flex-wrap md:flex-row space-y-4 md:space-y-0 pb-4  rounded-t-lg">
			<table class="w-full text-sm mt-6 text-left rtl:text-right">
				<thead>
					<tr class="">
						<th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
							Appointment Date</th>
						<th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
							Employee</th>
						<th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
							Service</th>
						<th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
							Addons</th>
						<th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
							Payment Amount</th>
					</tr>
				</thead>
				<tbody>
					<tr v-if="loading">
						<td colspan="5" class="text-center py-4">
							<div role="status">
								<ArrowPathIcon class="inline w-8 h-8 text-gray-200 animate-spin fill-blue-600" />
								<span class="sr-only">Loading...</span>
							</div>
						</td>
					</tr>
					<tr v-else-if="!loading && appointments.length == 0">
						<td colspan="5" class="text-center py-4">
							<div role="status">

								<span class="text-xs font-medium text-gray-500 uppercase tracking-wider">No
									records found</span>
							</div>
						</td>
					</tr>
					<tr v-else v-for="appointment in appointments" :key="appointment.id"
						class="border-b border-b-gray-200 hover:bg-gray-100">
						<td class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-900">
							<small class="text-gray-600">{{ appointment.id }}</small>
							{{ appointment.appointment_date ? toLocaleDate(appointment.appointment_date) : "n/a" }}

							<small>from {{ appointment.start_time }} to {{ appointment.end_time }}</small>
							<span v-if="appointment.is_past"
								class="inline-block ml-2 px-2 py-0.5 text-xs font-semibold rounded bg-red-100 text-red-800">Past</span>
							<span v-else-if="appointment.is_future"
								class="inline-block ml-2 px-2 py-0.5 text-xs font-semibold rounded bg-green-100 text-green-800">Future</span>
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center  text-sm text-gray-900">{{
							appointment.employee_name }}
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center  text-sm text-gray-900"> {{
							appointment.service_name }}
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center"
							:class="appointment.addons.length ? 'text-gray-900 text-sm' : 'text-gray-300 text-xs'">{{
								appointment.addons.length ? appointment.addons.join(", ") : "n/a" }}
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-center  text-sm text-gray-900"> ${{
							appointment.payment_amount }}
						</td>
					</tr>
				</tbody>
			</table>

		</div>
		<!-- Pagination -->
		<div class="mt-4 flex justify-between items-center">
			<button @click="previousPage" :disabled="isFirstPage"
				class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Previous</button>
			<span v-if="appointments.length > 0" class="text-md font-medium text-gray-500 uppercase tracking-wider">Page
				{{ currentPage }} of {{
					totalPages }}</span>
			<button @click="nextPage" :disabled="isLastPage"
				class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Next</button>
		</div>
	</div>
</template>

<script>
import { mapActions } from "vuex";

export default {
	props: {
		client: {
			type: Object,
			required: null,
		},
	},
	data() {
		return {
			loading: false,

			count: null,
			currentPage: 1,
			pageSize: 5,
			totalPages: 1,
			sortBy: "start",
			sortOrder: "desc",

			appointments: [],

			filters: {},
		};
	},
	computed: {
		sorting() {
			return this.sortOrder === "asc" ? this.sortBy : `-${this.sortBy}`; // DRF ordering syntax
		},
		isFirstPage() {
			return this.currentPage === 1;
		},
		isLastPage() {
			return this.currentPage === this.totalPages;
		},
	},
	methods: {
		...mapActions("clients", ["filterClientAppointments"]),
		itemProvider() {
			this.loading = true;
			this.filterClientAppointments({
				client_id: this.client.id,
				page: this.currentPage,
				page_size: this.pageSize,
				sorting: this.sorting,
				gender: this.selectedType,
				...this.filters,
			})
				.then((response) => {
					console.log(response);
					this.appointments = response.results;
					this.totalPages = Math.ceil(response.count / this.pageSize);
					// console.log(this.clients);
				})
				.catch((errors) => {
					this.formatErrors(errors.response);
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
				this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc"; // Toggle order
			} else {
				this.sortBy = column;
				this.sortOrder = "asc";
			}
			this.itemProvider();
		},
	},
	mounted() {
		this.itemProvider();
	},
	async beforeRouteEnter(to, from, next) {
		return next();
	},
};
</script>
