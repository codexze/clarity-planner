<template>
	<div class="relative overflow-x-auto p-4 g-white shadow-md sm:rounded-lg">
		<div class="pb-12">
			<h2 class="text-base/7 font-semibold text-gray-900">Service Details</h2>
			<p class="mt-1 text-sm/6 text-gray-600">Change the important details about your services here.</p>

			<div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 py-4">

				<div class="sm:col-span-2">
					<label for="name" class="block text-sm/6 font-medium text-gray-900">Name</label>
					<div class="mt-2">
						<div
							class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-blue-300">
							<input type="text" name="name" id="name" v-model="form.name"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="e.g. Hair & Makeup" />
						</div>
					</div>
				</div>

				<div class="sm:col-span-2">
					<label for="type" class="block text-sm/6 font-medium text-gray-900">Service Type</label>
					<div class="mt-2">
						<select id="type" v-model="form.type_id"
							class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
							<option :value="null">Select a service type</option>
							<option v-for="type in serviceTypes" :key="type.id" :value="type.id">
								{{ type.name }}
							</option>
						</select>
					</div>
				</div>

				<div class="col-span-full">
					<label for="description" class="block text-sm/6 font-medium text-gray-900">Description</label>
					<div class="mt-2">
						<textarea name="description" id="description" rows="3" v-model="form.description"
							class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus-within:-outline-offset-2 focus-within:outline-blue-300 sm:text-sm/6"></textarea>
					</div>
					<p class="mt-3 text-sm/6 text-gray-600">Write a few sentences about this service.</p>
				</div>

				<div class="sm:col-span-2">
					<label for="duration" class="block text-sm/6 font-medium text-gray-900">Duration</label>
					<div class="mt-2">
						<div class="flex items-center rounded-md bg-white">
							<VueDatePicker v-model="form.duration" auto-apply :teleport="true" text-input time-picker
								:start-time="startTime" :enable-seconds="false" :minute-increment="15" no-hours-overlay
								:format="'HH:mm'" placeholder="Select duration"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 rounded-md outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-blue-300" />
						</div>
					</div>
				</div>

				<div class="sm:col-span-2">
					<label for="price" class="block text-sm/6 font-medium text-gray-900">Price</label>
					<div class="mt-2">
						<div
							class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-blue-300">
							<div class="shrink-0 text-base text-gray-500 select-none sm:text-sm/6">$</div>
							<input type="text" name="price" id="price" v-model="form.price"
								class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
								placeholder="0.00" />
						</div>
					</div>
				</div>

				<div class="sm:col-span-2">
					<div class="flex items-start mt-8">
						<div class="flex items-center h-5">
							<input id="available" type="checkbox" v-model="form.is_active"
								class="w-4 h-4 border border-gray-300 rounded-sm bg-gray-50 focus:ring-3 focus:ring-blue-300"
								required />
						</div>
						<label for="available" class="ms-2 text-sm font-medium text-gray-900">Available?</label>
					</div>
				</div>
			</div>

			<div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b">
				<button @click="handleSubmit"
					class="text-white bg-blue-500 hover:bg-blue-600 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">Submit</button>
				<button @click="cancel"
					class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none  rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-600 focus:z-10 focus:ring-4 focus:ring-gray-100">Cancel</button>
			</div>
		</div>
	</div>
</template>

<script>
import store from "@/store";
import Form from "@/core/utils/Form";

import VueDatePicker from "@vuepic/vue-datepicker";
import { ChevronDownIcon } from "@heroicons/vue/24/solid";

import { mapState, mapGetters, mapActions } from "vuex";
export default {
	components: {
		VueDatePicker,
		ChevronDownIcon,
	},
	data() {
		return {
			startTime: { hours: 0, minutes: 0 },
			form: new Form({
				id: null,
				consistency_token: null,
				type_id: null,
				name: null,
				description: null,
				duration: null,
				price: null,
				is_active: true,
			}),
		};
	},
	computed: {
		...mapState("services", {
			service: (state) => state.service,
			serviceTypes: (state) => state.types,
		}),
	},
	watch: {
		service: {
			immediate: true,
			handler(val) {
				this.form.populate(val);
				this.form.type_id = val.type?.id;
			},
		},
	},
	methods: {
		...mapActions("services", ["updateServiceById"]),
		handleSubmit() {
			this.updateServiceById(this.form.formData()).then((response) => {
				store.commit("services/SET_SERVICE", response);
				this.toastSuccess(`Service, ${this.service.name}, was updated successfully!`);
				// console.log(response);
			});
			// console.log(this.form.formData());
		},
		cancel() {
			this.$router.go(-1);
		},
	},
	async beforeRouteEnter(to, from, next) {
		const service = await store.dispatch("services/getServiceById", to.params.serviceId);
		const types = await store.dispatch("services/getServiceTypes");
		to.meta.label = `${service.name}`;
		return next();
	},
	beforeDestroy() {
		store.commit("services/SET_SERVICE", null);
	},
};
</script>
