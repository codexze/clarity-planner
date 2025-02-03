import axios from "axios";
import store from "@/store";

const instance = axios.create({
	paramsSerializer: {
		indexes: null, // array indexes format (null - no brackets, false (default) - empty brackets, true - brackets with indexes)
	},
});

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
	(response) => response,
	async (error) => {
		const originalRequest = error.config;

		// If token expired and refresh token exists, attempt to refresh
		if (error.response?.status === 401 && !originalRequest._retry) {
			originalRequest._retry = true;

			try {
				const refreshToken = store.state.auth.refreshToken;
				if (!refreshToken) {
					this.$router.push("/logout"); // No refresh token? Redirect to logout
					// store.dispatch("auth/logout"); // No refresh token? Log out user
					return Promise.reject(error);
				}

				// Attempt to refresh token
				// const response = await axios.post(`${API_URL}token/refresh/`, { refresh: refreshToken });
				const response = await store.dispatch("auth/refresh_token");
				store.commit("auth/SET_ACCESS_TOKEN", response.access); // Update token in Vuex

				// Retry the original request with the new token
				axiosInstance.defaults.headers.Authorization = `Bearer ${response.access}`;
				return axiosInstance(originalRequest);
			} catch (refreshError) {
				store.dispatch("auth/logout"); // Failed to refresh? Log out user
				return Promise.reject(refreshError);
			}
		}
		return Promise.reject(error);
	}
);

// Check token expiration periodically
// setInterval(() => {
// 	const token = store.state.auth.accessToken;
// 	if (!token) return;

// 	const tokenPayload = JSON.parse(atob(token.split(".")[1]));
// 	const expirationTime = tokenPayload.exp * 1000;
// 	const timeRemaining = expirationTime - Date.now();

// 	if (timeRemaining < 60000) {
// 		alert("⚠️ Your session is about to expire! Please refresh your token.");
// 	}
// }, 30000);

export default instance;
