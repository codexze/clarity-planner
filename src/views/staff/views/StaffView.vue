<template>
	<div class="relative overflow-x-auto p-4 g-white shadow-md sm:rounded-lg">
		<div class="flex items-center justify-between flex-column flex-wrap md:flex-row space-y-4 md:space-y-0 pb-4 bg-white">
			<!-- Search Bar -->
			<div class="relative mb-4">
				<div class="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
					<MagnifyingGlassIcon class="w-4 h-4 text-gray-500" />
				</div>
				<input type="text" v-model="searchQuery" @input="debouncedFilter" placeholder="Search employees..." class="block p-2 ps-10 border border-gray-300 rounded-md" />
			</div>

			<div class="relative mb-4">
				<!-- Type Dropdown -->
				<!-- <select v-model="selectedType" @input="debouncedFilter" class="block p-2 ps-8 pe-8 text-sm border border-gray-300 rounded-md">
					<option value="">All Genders</option>
					<option v-for="gender in genders" :key="gender.value" :value="gender.value">
						{{ gender.label }}
					</option>
				</select> -->
			</div>

			<!-- Create New Button -->
			<div class="relative mb-4">
				<!-- <button @click="onCreateNew()" class="px-4 py-2 text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50">New Client</button> -->
			</div>
		</div>

		<!-- Table -->
		<table class="w-full text-sm text-left rtl:text-right">
			<caption class="p-5 text-lg font-semibold text-left rtl:text-right text-gray-900 bg-white">
				Your Staff
				<p class="mt-1 text-sm font-normal text-gray-500">
					Browse a list of all the employees.
					<br />
					Add some more or edit the existing employees.
				</p>
			</caption>
			<thead class="uppercase">
				<tr class="bg-gray-200">
					<th class="px-4 py-2 text-left" @click="sorting('surname')">
						<div class="flex items-center gap-x-2">
							Name
							<ChevronUpDownIcon class="w-4 h-4" :class="sortBy == 'surname' ? 'text-gray-800' : 'text-gray-400'" />
						</div>
					</th>
					<th class="px-4 py-2 text-left">
						<div class="flex items-center gap-x-2">
							Date of Birth
							<!-- <ChevronUpDownIcon class="w-4 h-4" :class="sortBy == 'type' ? 'text-gray-800' : 'text-gray-400'" /> -->
						</div>
					</th>
					<th class="px-4 py-2 text-left" @click="sorting('gender')">
						<div class="flex items-center gap-x-2">Emailaddress</div>
					</th>
					<th class="px-4 py-2 text-left">
						<div class="flex items-center gap-x-2">Phone Number</div>
					</th>
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
				<tr v-else-if="!loading && staff.length == 0">
					<td colspan="5" class="text-center py-4">
						<div role="status">
							<!-- <ArrowPathIcon class="inline w-8 h-8 text-gray-200 animate-spin fill-blue-600" /> -->
							<span>No records found</span>
						</div>
					</td>
				</tr>
				<tr v-else v-for="client in staff" :key="client.id" class="border-b border-b-gray-200 hover:bg-gray-100">
					<td class="px-4 py-2 font-medium text-gray-800 whitespace-nowrap">
						<small class="text-gray-600">{{ client.id }}</small>
						{{ client.display }}

						<template v-if="client.gender == 'MALE'">
							<small class="text-gray-600">
								<font-awesome-icon :icon="['fas', 'mars']" />
							</small>
						</template>
						<template v-else-if="client.gender == 'FEMALE'">
							<small class="text-gray-600">
								<font-awesome-icon :icon="['fas', 'venus']" />
							</small>
						</template>
						<template v-else>
							<small class="text-gray-600">
								<font-awesome-icon :icon="['fas', 'venus-mars']" />
							</small>
						</template>
					</td>
					<td class="px-4 py-2 font-medium text-gray-900 whitespace-nowrap">
						{{ toLocaleDate(client.date_of_birth) }}
					</td>
					<td class="px-4 py-2 font-medium whitespace-nowrap" :class="client.emailaddress ? 'text-gray-900' : 'text-xs text-gray-400'">
						{{ client.emailaddress ? client.emailaddress : "n/a" }}
					</td>
					<td class="px-4 py-2 whitespace-nowrap" :class="client.mobile ? 'text-gray-900' : 'text-xs text-gray-400'">
						{{ client.mobile ? client.mobile : "n/a" }}
					</td>

					<!-- Edit Button -->
					<td class="px-6 py-4 text-right">
						<button @click="onEdit(client.id)" class="px-4 py-2 text-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50">Edit</button>
					</td>
				</tr>
			</tbody>
		</table>

		<!-- Pagination -->
		<div class="mt-4 flex justify-between items-center">
			<button @click="previousPage" :disabled="isFirstPage" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Previous</button>
			<span>Page {{ currentPage }} of {{ totalPages }}</span>
			<button @click="nextPage" :disabled="isLastPage" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md disabled:opacity-50">Next</button>
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
			sortBy: "surname",
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
		ordering() {
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
				order_by: this.ordering,
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
		sorting(column) {
			if (this.sortBy === column) {
				this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc"; // Toggle order
			} else {
				this.sortBy = column;
				this.sortOrder = "asc";
			}
			this.itemProvider();
		},
		onEdit(id) {
			this.$router.push({ path: `staff/${id}/view` });
		},
	},
	mounted() {
		this.itemProvider();
	},
	created() {
		this.debouncedFilter = debounce(this.itemProvider, 500);
	},
	async beforeRouteEnter(to, from, next) {
		// const genders = await store.dispatch("staff/getGenders");
		return next();
	},
	beforeDestroy() {
		this.debouncedFilter.cancel();
	},
};
</script>
