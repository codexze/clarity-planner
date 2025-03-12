<template>
	<div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-sm">
			<!-- <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/plus/img/logos/mark.svg?color=gray&shade=600" alt="Your Company" /> -->
			<h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Sign in to your account</h2>
		</div>

		<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
			<form class="space-y-6" @submit.prevent>
				<div>
					<label for="username" class="block text-sm/6 font-medium text-gray-900">Username</label>
					<div class="mt-2">
						<input type="username" name="username" id="username" autocomplete="username" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6" v-model="form.username" required />
					</div>
					<p v-if="fieldErrors.username" class="text-red-500 text-sm">
						{{ fieldErrors.username[0] }}
					</p>
				</div>

				<div>
					<div class="flex items-center justify-between">
						<label for="password" class="block text-sm/6 font-medium text-gray-900">Password</label>
					</div>
					<div class="mt-2 relative w-full">
						<template v-if="showPassword">
							<input type="text" name="password" id="password" autocomplete="current-password" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6" v-model="form.password" required />
							<button type="button" id="show-password" @click="showPassword = !showPassword" class="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-gray-700">
								<EyeIcon class="h-6 w-6text-gray-600" />
							</button>
						</template>
						<template v-else>
							<input type="password" name="password" id="password" autocomplete="current-password" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-gray-600 sm:text-sm/6" v-model="form.password" required />
							<button type="button" id="show-password" @click="showPassword = !showPassword" class="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-gray-700">
								<EyeSlashIcon class="h-6 w-6 text-gray-600" />
							</button>
						</template>
					</div>
					<p v-if="fieldErrors.password" class="text-red-500 text-sm">
						{{ fieldErrors.password[0] }}
					</p>
				</div>

				<div>
					<button @click="onLogin" class="flex w-full justify-center rounded-md bg-gray-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-gray-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-600">Sign in</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { mapActions } from "vuex";
import { useToast } from "vue-toastification";
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/solid";

import Form from "@/core/utils/Form";

export default {
	components: {
		EyeIcon,
		EyeSlashIcon,
	},
	data() {
		return {
			form: new Form({
				username: "",
				password: "",
			}),
			showPassword: false,
			fieldErrors: {},
		};
	},
	methods: {
		...mapActions("auth", ["login"]), // Calling login from the auth module

		async onLogin() {
			await this.login(this.form.formData())
				.then((response) => {
					this.toastSuccess("Welcome, you have successfully logged into Clarity!");
					this.$router.push("/dashboard"); // Redirect on success
				})
				.catch((errors) => {
					this.fieldErrors = this.formatErrors(errors.response.data);
				});
		},
	},
};
</script>
