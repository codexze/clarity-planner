<template>
	<div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-sm">
			<!-- <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company" /> -->
			<h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight text-gray-900">Sign in to your account</h2>
		</div>

		<div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
			<form class="space-y-6">
				<div>
					<label for="username" class="block text-sm/6 font-medium text-gray-900">Username</label>
					<div class="mt-2">
						<input type="username" name="username" id="username" autocomplete="username" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" v-model="form.username" required />
					</div>
				</div>

				<div>
					<div class="flex items-center justify-between">
						<label for="password" class="block text-sm/6 font-medium text-gray-900">Password</label>
					</div>
					<div class="mt-2 relative w-full">
						<template v-if="showPassword">
							<input type="text" name="password" id="password" autocomplete="current-password" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" v-model="form.password" required />
							<button type="button" id="show-password" @click="showPassword = !showPassword" class="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-gray-700">
								<EyeIcon class="h-6 w-6text-indigo-600" />
							</button>
						</template>
						<template v-else>
							<input type="password" name="password" id="password" autocomplete="current-password" class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" v-model="form.password" required />
							<button type="button" id="show-password" @click="showPassword = !showPassword" class="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-gray-700">
								<EyeSlashIcon class="h-6 w-6 text-indigo-600" />
							</button>
						</template>
					</div>
				</div>

				<div>
					<button type="button" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600" @click="handleLogin">Sign in</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { mapActions } from "vuex";
import Form from "@/core/utils/Form";

import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/solid";

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
		};
	},
	methods: {
		...mapActions("auth", ["login"]), // Calling login from the auth module

		async handleLogin() {
			await this.login(this.form.formData())
				.then((response) => {
					this.$router.push("/services"); // Redirect on success
				})
				.catch((errors) => {
					console.log(errors);
				});
		},
	},
};
</script>
