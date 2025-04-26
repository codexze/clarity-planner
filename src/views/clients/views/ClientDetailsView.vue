<template>
	<div class="relative overflow-x-auto p-4 g-white shadow-md sm:rounded-lg">
		<div class="border-b border-gray-900/10 pb-12">
			<h2 class="text-base/7 font-semibold text-gray-900">Client Details</h2>
			<p class="mt-1 text-sm/6 text-gray-600">Change the important details about your clients here.</p>

			<div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
				<div class="sm:col-span-2">
					<label for="first_name" class="block text-sm/6 font-medium text-gray-900">First Name</label>
					<div class="mt-2">
						<div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
							<!-- <div class="shrink-0 text-base text-gray-500 select-none sm:text-sm/6">hair&makup</div> -->
							<input type="text" name="first_name" id="first_name" v-model="form.first_name" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="e.g. Hair & Makeup" />
						</div>
					</div>
				</div>
				<div class="sm:col-span-2">
					<label for="surname" class="block text-sm/6 font-medium text-gray-900">Surname</label>
					<div class="mt-2">
						<div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
							<!-- <div class="shrink-0 text-base text-gray-500 select-none sm:text-sm/6">hair&makup</div> -->
							<input type="text" name="surname" id="surname" v-model="form.surname" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="e.g. Hair & Makeup" />
						</div>
					</div>
				</div>

				<div class="sm:col-span-2">
					<label for="name" class="block text-sm/6 font-medium text-gray-900">Gender</label>
					<div class="mt-2">
						<select id="genders" v-model="form.gender" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
							<option v-for="gender in genders" :key="gender.value" :value="gender.value">{{ gender.label }}</option>
						</select>
					</div>
				</div>

				<div class="sm:col-span-2">
					<label for="date_of_birth" class="block text-sm/6 font-medium text-gray-900">Date of Birth</label>
					<div class="">
						<VueDatePicker v-mask="'##-##-####'" :teleport="true" v-model="form.date_of_birth" placeholder="MM-DD-YYYY " format="MM-dd-yyyy" model-type="yyyy-MM-dd" :max-date="new Date()" :hide-navigation="['time']" prevent-min-max-navigation auto-position="top" text-input class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" />
					</div>
				</div>
				<div class="sm:col-span-2 sm:col-start-1">
					<label for="email" class="block text-sm/6 font-medium text-gray-900">Email</label>
					<div class="mt-2">
						<div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
							<!-- <div class="shrink-0 text-base text-gray-500 select-none sm:text-sm/6">billybob@domain.com</div> -->
							<input type="text" name="email" id="email" v-model="form.email" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="e.g. billybob@doamin.com" />
						</div>
					</div>
				</div>
				<div class="sm:col-span-2">
					<label for="mobile" class="block text-sm/6 font-medium text-gray-900">Phone Number</label>
					<div class="mt-2">
						<div class="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
							<div class="shrink-0 text-base text-gray-500 select-none sm:text-sm/6">+</div>
							<input type="text" name="mobile" id="mobile" v-mask="['### ###-####', '## # ####-####', '# (###) ###-####']" v-model="form.mobile" class="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="597 000-0000" />
						</div>
					</div>
				</div>

				<div class="sm:col-span-2">
					<div class="flex items-start mt-8">
						<div class="flex items-center h-5">
							<input id="available" type="checkbox" v-model="form.is_active" class="w-4 h-4 border border-gray-300 rounded-sm bg-gray-50 focus:ring-3 focus:ring-blue-300" required />
						</div>
						<label for="available" class="ms-2 text-sm font-medium text-gray-900">Active?</label>
					</div>
				</div>

				<div>
					<button @click="handleSubmit()" :disabled="!form.dirty()" class="px-2 py-1 mr-2 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded-sm disabled:opacity-50">Update</button>
					<button @click="cancel()" class="px-2 py-1 text-sm text-white bg-gray-500 hover:bg-gray-600 rounded-sm disabled:opacity-50">Cancel</button>
				</div>
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
			form: new Form({
				id: null,
				consistency_token: null,
				first_name: null,
				surname: null,
				date_of_birth: null,
				gender: "UNKNOWN",
				email: null,
				mobile: null,
				is_active: true,
			}),
		};
	},
	computed: {
		...mapState("clients", {
			client: (state) => state.client,
			genders: (state) => state.genders,
		}),
	},
	watch: {
		client: {
			immediate: true,
			handler(val) {
				this.form.withData(val);
			},
		},
	},
	methods: {
		...mapActions("clients", ["updateClientById"]),
		handleSubmit() {
			this.updateClientById(this.form.formData()).then((response) => {
				store.commit("clients/SET_CLIENT", response);
				this.toastSuccess(`Client, ${this.client.name}, was updated successfully!`);
				console.log(response);
			});
			// console.log(this.form.formData());
		},
		cancel() {
			this.$router.push({ path: "/clients" });
		},
	},
	async beforeRouteEnter(to, from, next) {
		const client = await store.dispatch("clients/getClientById", to.params.clientId);
		const genders = await store.dispatch("clients/getGenders");
		// to.meta.label = `${client.name}`;
		return next();
	},
	beforeDestroy() {
		store.commit("clients/SET_CLIENT", null);
	},
};
</script>
