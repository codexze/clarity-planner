<template>
	<div class="relative overflow-x-auto p-4 g-white shadow-md sm:rounded-lg">
		<div class="flex items-center justify-between flex-column flex-wrap md:flex-row space-y-4 md:space-y-0 pb-4 bg-white">
			<div class="relative mb-4"></div>

			<!-- Create New Button -->
			<div class="relative mb-4">
				<button @click="onCreateNew()" class="px-4 py-2 text-white bg-green-600 hover:bg-green-700 rounded-md disabled:opacity-50">New Service</button>
			</div>
		</div>

		<!-- Table -->
		<table class="w-full text-sm text-left rtl:text-right">
			<caption class="p-5 text-lg font-semibold text-left rtl:text-right text-gray-900 bg-white">
				Your Services
				<p class="mt-1 text-sm font-normal text-gray-500">
					Browse a list of all the service your company provides.
					<br />
					Add some more or edit the existing services.
				</p>
			</caption>
			<thead class="uppercase">
				<tr class="">
					<th class="px-4 py-2">
						<div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-indigo-600 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
							<input type="text" name="name_search" id="name_search" v-model="filters.name" @keyup.enter="itemProvider" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="Search by Name" />
						</div>
					</th>
					<th class="px-4 py-2">
						<select v-model="filters.type" @change="itemProvider" class="block p-2 ps-8 pe-8 text-sm border border-indigo-600 rounded-md">
							<option :value="null">All Service Type</option>
							<option v-for="type in serviceTypes" :key="type.id" :value="type.id">
								{{ type.name }}
							</option>
						</select>
					</th>
					<th class="px-4 py-2"></th>
					<th class="px-4 py-2">
						<select v-model="filters.is_active" @change="itemProvider" class="block mt-2 p-2 ps-8 pe-13 text-sm border border-indigo-600 rounded-md">
							<option :value="null">All Statusses</option>
							<option :value="true">Available</option>
							<option :value="false">Unavailable</option>
						</select>
					</th>

					<th class="px-6 py-3"></th>
				</tr>

				<tr class="bg-gray-200">
					<th class="px-4 py-2 text-left" @click="sorting('name')">
						<div class="flex items-center gap-x-2">
							Name
							<ChevronUpDownIcon class="w-4 h-4" :class="sortBy == 'name' ? 'text-gray-800' : 'text-gray-400'" />
						</div>
					</th>
					<th class="px-4 py-2 text-left" @click="sorting('type')">
						<div class="flex items-center gap-x-2">
							Type
							<ChevronUpDownIcon class="w-4 h-4" :class="sortBy == 'type' ? 'text-gray-800' : 'text-gray-400'" />
						</div>
					</th>
					<th class="px-4 py-2 text-left" @click="sorting('price')">
						<div class="flex items-center gap-x-2">
							Price
							<ChevronUpDownIcon class="w-4 h-4" :class="sortBy == 'price' ? 'text-gray-800' : 'text-gray-400'" />
						</div>
					</th>
					<th class="px-4 py-2 text-left" @click="sorting('active')">
						<div class="flex items-center gap-x-2">
							Availability
							<ChevronUpDownIcon class="w-4 h-4" :class="sortBy == 'active' ? 'text-gray-800' : 'text-gray-400'" />
						</div>
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
				<tr v-else-if="!loading && services.length == 0">
					<td colspan="5" class="text-center py-4">
						<div role="status">
							<!-- <ArrowPathIcon class="inline w-8 h-8 text-gray-200 animate-spin fill-blue-600" /> -->
							<span>No records found</span>
						</div>
					</td>
				</tr>
				<tr v-else v-for="service in services" :key="service.id" class="border-b border-b-gray-200 hover:bg-gray-100">
					<td class="px-4 py-2 font-medium text-gray-800 whitespace-nowrap">
						{{ service.name }}
						<br />
						<small class="text-gray-600">{{ service.description }}</small>
					</td>
					<td class="px-4 py-2">
						<span class="bg-gray-100 text-gray-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded-sm border border-gray-500">{{ service.type.name }}</span>
					</td>
					<td class="px-4 py-2">{{ service.price }}</td>
					<td class="px-4 py-2">
						<span v-if="service.is_active" class="">
							<span class="inline-flex items-center bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
								<span class="w-2 h-2 me-1 bg-green-500 rounded-full"></span>
								Available
							</span>
						</span>
						<span v-else class="">
							<span class="inline-flex items-center bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
								<span class="w-2 h-2 me-1 bg-red-500 rounded-full"></span>
								Unavailable
							</span>
						</span>
					</td>
					<!-- Edit Button -->
					<td class="px-6 py-4 text-right">
						<button @click="onEdit(service.id)" class="px-4 py-2 text-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50">Edit</button>
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
			filters: {
				name: null,
				type: null,
				is_active: null,
			},
			sortBy: "name",
			sortOrder: "asc",

			debouncedFilter: null,

			services: [],
		};
	},
	computed: {
		...mapState("services", {
			serviceTypes: (state) => state.types,
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
		...mapActions("services", ["filterServices"]),
		itemProvider() {
			this.loading = true;
			this.filterServices({
				page: this.currentPage,
				page_size: this.pageSize,
				order_by: this.ordering,
				...this.filters,
			})
				.then((response) => {
					this.services = response.results;
					this.totalPages = Math.ceil(response.count / this.pageSize);
					console.log(this.services);
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
		onCreateNew() {
			this.$router.push({ path: "services/new" });
		},
		onEdit(id) {
			this.$router.push({ path: `services/${id}/view` });
		},
	},
	mounted() {
		this.itemProvider();
	},
	created() {
		this.debouncedFilter = debounce(this.itemProvider, 500);
	},
	async beforeRouteEnter(to, from, next) {
		const types = await store.dispatch("services/getServiceTypes");
		return next();
	},
	beforeDestroy() {
		this.debouncedFilter.cancel();
	},
};
</script>
