import axios from "axios";
import store from "@/store";
import router from "@/router";

const instance = axios.create({
	paramsSerializer: {
		indexes: null, // array indexes format (null - no brackets, false (default) - empty brackets, true - brackets with indexes)
	},
});

instance.defaults.baseURL = "http://localhost:8080/";

instance.interceptors.request.use(
	(config) => {
		const token = store.state.auth.accessToken; // Access Vuex state
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error) => Promise.reject(error)
);

instance.interceptors.response.use(
	(response) => {
		return response;
	}, // Directly return successful responses.
	async (error) => {
		if (error.response) {
			const { status } = error.response;

			// Handle 401 Unauthorized error
			if (router.currentRoute.value.path !== "/login" && status === 401) {
				const originalRequest = error.config;

				// Prevent infinite loops - only attempt refresh once
				if (!originalRequest._retry) {
					originalRequest._retry = true;

					try {
						// Try to refresh the token
						const refreshToken = store.state.auth.refreshToken;

						if (!refreshToken) {
							// No refresh token available, force logout
							router.push({ path: "/logout", replace: true });
							return Promise.reject(error);
						}

						// Make a request to refresh the token
						const response = await store.dispatch("auth/refresh_token", refreshToken);

						// If token refresh was successful
						if (response.data.accessToken) {
							// Update the token in the store
							await store.dispatch("auth/refresh_token", response.data.accessToken);

							//o Refresh the page instead of retrying the request
							window.location.reload();
							return new Promise(() => {});
						}
					} catch (refreshError) {
						// Token refresh failed, force logout
						router.push({ path: "/logout", replace: true });
						return Promise.reject(refreshError);
					}
				}
			}
		}
		return Promise.reject(error); // For all other errors, return the error as is.
	}
);
export default instance;
