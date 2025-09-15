<template>
	<div class="relative overflow-x-auto p-4 g-white shadow-md sm:rounded-lg">
		<div
			class="flex items-center justify-between flex-column flex-wrap md:flex-row space-y-4 md:space-y-0 pb-4 bg-white">
			<div class="relative mb-4"></div>

			<!-- Create New Button -->
			<div class="relative mb-4">
				<!-- <button @click="onCreateNew()" class="px-4 py-2 text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50">New Client</button> -->
			</div>
		</div>

		<!-- Table -->
		<table class="w-full text-sm text-left rtl:text-right">
			<caption class="p-5 text-lg font-semibold text-left rtl:text-right text-gray-900 bg-white">
				Your Appointments
				<p class="mt-1 text-sm font-normal text-gray-500">
					Browse a list of all the appointments.
					<br />
					Add some more or edit the existing appointments.
				</p>
			</caption>
			<thead class="uppercase">
				<tr class="">
					<th class="px-4 py-2">
						<div
							class="grid items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="appointment_date_search" id="appointment_date_search"
								v-model="filters.appointment_date" @keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Appointment Date" />
						</div>
					</th>
					<th class="px-4 py-2">
						<div
							class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="client_search" id="client_search" v-model="filters.client__name"
								@keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Client Name" />
						</div>
					</th>
					<th class="px-4 py-2">
						<div
							class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="service_search" id="service_search" v-model="filters.service__name"
								@keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Service Name" />
						</div>
					</th>
				</tr>
				<tr class="bg-gray-200">
					<th class="px-4 py-2 text-left">
						<div class="flex items-center gap-x-2" @click="sort('start')">
							Appointment Date
							<ChevronUpDownIcon class="w-4 h-4"
								:class="sortBy == 'start' ? 'text-gray-900 font-weight-bold' : 'text-gray-300'" />
						</div>
					</th>
					<th class="px-4 py-2 text-left">
						<div class="flex items-center gap-x-2">Client</div>
					</th>
					<th class="px-4 py-2 text-left">
						<div class="flex items-center gap-x-2">Service</div>
					</th>
					<th class="px-4 py-2 text-left">
						<div class="flex items-center gap-x-2">Assigned to</div>
					</th>
					<th class="py-2 text-center" @click="sort('is_onsite')">Onsite?</th>

					<th scope="col" class="px-6 py-3">
						<span class="sr-only">Edit</span>
					</th>
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
					<td class="px-4 py-2 font-medium whitespace-nowrap"
						:class="appointment.appointment_date ? 'text-gray-900' : 'text-xs text-gray-400'">
						<small class="text-gray-600">{{ appointment.id }}</small>
						{{ appointment.appointment_date ? toLocaleDate(appointment.appointment_date) : "n/a" }}

						<small>from {{ appointment.start_time }} to {{ appointment.end_time }}</small>
						<span v-if="appointment.is_past"
							class="inline-block ml-2 px-2 py-0.5 text-xs font-semibold rounded bg-red-100 text-red-800">Past</span>
						<span v-else-if="appointment.is_future"
							class="inline-block ml-2 px-2 py-0.5 text-xs font-semibold rounded bg-green-100 text-green-800">Future</span>
					</td>
					<td class="px-4 py-2 font-medium text-gray-800 whitespace-nowrap">
						{{ appointment.client_name }}
					</td>
					<td class="px-4 py-2 font-medium text-gray-800 whitespace-nowrap">
						{{ appointment.service_name }}
						<small>{{ appointment.service.time_display }}</small>
					</td>
					<td class="px-4 py-2 font-medium text-gray-800 whitespace-nowrap">
						{{ appointment.employee_name }}
					</td>
					<td class="py-2 text-center font-medium whitespace-nowrap">
						<span v-if="appointment.is_onsite" class="text-emerald-600">Yes</span>
						<span v-else class="text-red-600">No</span>
					</td>
					<td class="px-6 py-4 text-right">
						<button @click="onEdit(appointment.id)"
							class="px-4 py-2 text-medium text-white bg-blue-500 hover:bg-blue-600 rounded-md disabled:opacity-50">Edit</button>
					</td>
				</tr>
			</tbody>
		</table>

		<!-- Pagination -->
		<div class="mt-4 flex justify-between items-center">
			<button @click="previousPage" :disabled="isFirstPage"
				class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Previous</button>
			<span>Page {{ currentPage }} of {{ totalPages }}</span>
			<button @click="nextPage" :disabled="isLastPage"
				class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Next</button>
		</div>
	</div>
</template>

<script>
import { mapState, mapActions } from "vuex";

import debounce from "lodash.debounce";
import { MagnifyingGlassIcon, ArrowPathIcon, ChevronUpDownIcon } from "@heroicons/vue/24/solid";

export default {
	components: {
		MagnifyingGlassIcon,
		ArrowPathIcon,
		ChevronUpDownIcon,
	},
	data() {
		return {
			loading: false,
			username: null,

			count: null,
			currentPage: 1,
			pageSize: 5,
			totalPages: 1,
			sortBy: "start",
			sortOrder: "desc", // asc, desc
			selectedType: "",
			appointments: [],

			debouncedFilter: null,

			filters: {},
		};
	},
	computed: {
		...mapState("planning", {
			settings: (state) => state.settings,
			employee: (state) => state.employee,
			employees: (state) => state.employees,
		}),
		sorting() {
			return this.sortOrder === "asc" ? this.sortBy : `-${this.sortBy}`; // DRF sorting syntax
		},
		isFirstPage() {
			return this.currentPage === 1;
		},
		isLastPage() {
			return this.currentPage === this.totalPages;
		},
	},
	methods: {
		...mapActions("planning", ["filterAppointments"]),
		itemProvider() {
			this.loading = true;
			this.filterAppointments({
				page: this.currentPage,
				page_size: this.pageSize,
				sorting: this.sorting,
				...this.filters,
			})
				.then((response) => {
					this.appointments = response.results;
					this.totalPages = Math.ceil(response.count / this.pageSize);
					console.log(this.appointments);
				})
				.catch((errors) => {
					this.formatErrors(errors.response);
				})
				.finally(() => {
					// setTimeout(() => {
					this.loading = false;
					// }, 3000);
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
		onEdit(id) {
			this.$router.push({ path: `/planning/${this.username}/appointments/${id}/view` });
		},
	},
	mounted() {
		this.itemProvider();
	},
	created() {
		this.debouncedFilter = debounce(this.itemProvider, 500);
	},
	async beforeRouteEnter(to, from, next) {
		return next((vm) => {
			vm.username = to.params.username;
		});
	},
	beforeDestroy() {
		this.debouncedFilter.cancel();
	},
};
</script>
