<template>
	<div class="relative overflow-x-auto p-4 g-white shadow-md sm:rounded-lg">
		<table class="w-full text-sm text-left rtl:text-right">
			<caption class="p-5 text-lg font-semibold text-left rtl:text-right text-gray-900">
				Your Staff
				<p class="mt-1 text-sm font-normal text-gray-500">
					Browse a list of all the employees.
					<br />
					Add some more or edit the existing employees.
				</p>
			</caption>
			<thead class="uppercase">
				<tr class="">
					<th class="px-4 py-2">
						<div
							class="flex items-center rounded-md pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="name_search" id="name_search" v-model="filters.name"
								@keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Name" />
						</div>
					</th>
					<th class="px-4 py-2">
						<div
							class="flex items-center rounded-md pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="date_of_birth_search" id="date_of_birth_search"
								v-model="filters.date_of_birth" @keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Date of Birth" />
						</div>
					</th>
					<th class="px-4 py-2">
						<div
							class="flex items-center rounded-md pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="email_search" id="email_search" v-model="filters.email"
								@keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Email" />
						</div>
					</th>
					<th class="px-4 py-2">
						<div
							class="flex items-center rounded-md pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-gray-300">
							<input type="text" name="mobile_search" id="mobile_search" v-model="filters.mobile"
								@keyup.enter="itemProvider"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="Search by Phone Number" />
						</div>
					</th>

					<th class="px-6 py-3 text-center">

					</th>
				</tr>
				<tr class="">
					<th class="px-6 py-3 text-center text-md font-medium text-gray-500 uppercase tracking-wider"
						@click="sort('surname')">Name</th>
					<th class="px-6 py-3 text-center text-md font-medium text-gray-500 uppercase tracking-wider"
						@click="sort('date_of_birth')">Date of Birth</th>
					<th class="px-6 py-3 text-center text-md font-medium text-gray-500 uppercase tracking-wider"
						@click="sort('email')">Email</th>
					<th class="px-6 py-3 text-center text-md font-medium text-gray-500 uppercase tracking-wider"
						@click="sort('mobile')">Phone</th>
					<th scope="col"
						class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
						<span class="sr-only">Actions</span>
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
				<tr v-else-if="!loading && staff.length == 0">
					<td colspan="5" class="text-center py-4">
						<div role="status">

							<span class="text-xs font-medium text-gray-500 uppercase tracking-wider">No
								records found</span>
						</div>
					</td>
				</tr>
				<tr v-else v-for="employee in staff" :key="employee.id"
					class="border-b border-b-gray-200 hover:bg-gray-100">
					<td class="px-4 py-2 font-medium text-centertext-gray-800 whitespace-nowrap">
						<small class="text-gray-600">{{ employee.id }}</small>
						{{ employee.display }}
					</td>
					<td class="px-4 py-2 font-medium whitespace-nowrap"
						:class="employee.date_of_birth ? 'text-gray-900' : 'text-xs text-gray-400'">
						{{ employee.date_of_birth ? toLocaleDate(employee.date_of_birth) : "n/a" }}
					</td>
					<td class="px-4 py-2 font-medium whitespace-nowrap"
						:class="employee.email ? 'text-gray-900' : 'text-xs text-gray-400'">
						{{ employee.email ? employee.email : "n/a" }}
					</td>
					<td class="px-4 py-2 whitespace-nowrap"
						:class="employee.mobile ? 'text-gray-900' : 'text-xs text-gray-400'">
						{{ employee.mobile ? `+${employee.mobile}` : "n/a" }}
					</td>

					<!-- Edit Button -->
					<td class="px-6 py-4 text-center">
						<button @click="onEdit(employee.username)"
							class="px-4 py-2 text-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50">Edit</button>
					</td>
				</tr>
			</tbody>
		</table>

		<!-- Pagination -->
		<div class="mt-4 flex justify-between items-center">
			<button @click="previousPage" :disabled="isFirstPage"
				class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Previous</button>
			<span class="text-md font-medium text-gray-500 uppercase tracking-wider">Page {{ currentPage }} of {{
				totalPages }}</span>
			<button @click="nextPage" :disabled="isLastPage"
				class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Next</button>
		</div>
	</div>
</template>

<script>
import store from "@/store";
import { mapState, mapGetters, mapActions } from "vuex";

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

			count: null,
			currentPage: 1,
			pageSize: 5,
			totalPages: 1,
			sortBy: "last_name",
			sortOrder: "asc",
			selectedType: "",
			staff: [],

			debouncedFilter: null,

			searchQuery: "",
			filters: {},
		};
	},
	computed: {
		...mapState("staff", {
			genders: (state) => state.genders,
		}),
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
		...mapActions("staff", ["filterStaff"]),
		itemProvider() {
			this.loading = true;
			this.filterStaff({
				search: this.searchQuery,
				gender: this.selectedType,
				page: this.currentPage,
				page_size: this.pageSize,
				sorting: this.sorting,
				...this.filters,
			})
				.then((response) => {
					this.staff = response.results;
					this.totalPages = Math.ceil(response.count / this.pageSize);
					console.log(this.staff);
				})
				.catch((errors) => {
					this.formatErrors(errors.response);
				})
				.finally(() => {
					setTimeout(() => {
						this.loading = false;
					}, 3000);
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
		onEdit(username) {
			this.$router.push({ path: `staff/${username}/view` });
		},
	},
	mounted() {
		this.itemProvider();
	},
	created() {
		this.debouncedFilter = debounce(this.itemProvider, 500);
	},
	async beforeRouteEnter(to, from, next) {
		return next();
	},
	beforeDestroy() {
		this.debouncedFilter.cancel();
	},
};
</script>
