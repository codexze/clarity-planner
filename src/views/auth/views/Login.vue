<template>
	<div class="min-h-screen flex items-center justify-center">
		<div class="w-full max-w-md space-y-8 px-2 ">
			<div class="text-center">
				<img class="mx-auto h-12 w-auto" src="@/assets/logo.png" alt="Clarity" />
				<p class="mt-6 text-center text-xl tracking-tight text-gray-900">Sign in to your account
				</p>
			</div>

			<form class="space-y-6" @submit.prevent>
				<div>
					<label for="username" class="block text-sm/6 font-medium text-gray-900">Username</label>
					<div class="mt-2">
						<input type="username" name="username" id="username" autocomplete="username"
							class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-600 sm:text-sm/6"
							v-model="form.username" required />
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
							<input type="text" name="password" id="password" autocomplete="current-password"
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-600 sm:text-sm/6"
								v-model="form.password" required />
							<button type="button" id="show-password" @click="showPassword = !showPassword"
								class="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-gray-700">
								<EyeIcon class="h-6 w-6 text-blue-500 hover:text-blue-600" />
							</button>
						</template>
						<template v-else>
							<input type="password" name="password" id="password" autocomplete="current-password"
								class="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-blue-600 sm:text-sm/6"
								v-model="form.password" required />
							<button type="button" id="show-password" @click="showPassword = !showPassword"
								class="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-gray-700">
								<EyeSlashIcon class="h-6 w-6 text-gray-500 hover:text-gray-700" />
							</button>
						</template>
					</div>
					<p v-if="fieldErrors.password" class="text-red-500 text-sm">
						{{ fieldErrors.password[0] }}
					</p>
				</div>

				<div class="flex items-center justify-between">
					<div class="flex items-center">
						<input id="remember-me" name="remember-me" type="checkbox" v-model="form.rememberMe"
							class="h-4 w-4 rounded border-gray-300 text-blue-500 focus:ring-blue-500 " />
						<label for="remember-me" class="ml-2 block text-sm text-gray-900">Remember me</label>
					</div>
					<div class="text-sm">
						<router-link to="/auth/forgot-password"
							class="font-semibold text-blue-500 hover:text-blue-600">Forgot
							password?</router-link>
					</div>
				</div>

				<div>
					<button @click="onLogin"
						class="flex w-full justify-center rounded-lg bg-blue-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-blue-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">Sign
						in</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { mapActions } from "vuex";
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
				rememberMe: false,
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
