import session from "@/core/utils/Session";

const state = {
	user: null,
	accessToken: localStorage.getItem("access_token") || "",
	refreshToken: localStorage.getItem("refresh_token") || "",
};

const getters = {
	isAuthenticated: (state) => !!state.accessToken,
	getAccessToken: (state) => state.accessToken,
	getRefreshToken: (state) => state.refreshToken,
	getUser: (state) => state.user,
};

const mutations = {
	SET_USER(state, user) {
		state.user = user;
	},
	SET_ACCESS_TOKEN(state, token) {
		state.accessToken = token;
		localStorage.setItem("access_token", token);
	},
	SET_REFRESH_TOKEN(state, token) {
		state.refreshToken = token;
		localStorage.setItem("refresh_token", token);
	},
	LOGOUT(state) {
		state.user = null;
		state.accessToken = "";
		state.refreshToken = "";
		localStorage.removeItem("access_token");
		localStorage.removeItem("refresh_token");
	},
};

const actions = {
	login({ commit }, credentials) {
		return session
			.post("api/authorize/token/", credentials)
			.then((response) => {
				commit("SET_ACCESS_TOKEN", response.data.access);
				commit("SET_REFRESH_TOKEN", response.data.refresh);
				return response.data;
			})
			.finally(() => {});
	},
	refresh_token({ commit }, token) {
		return session
			.post("api/authorize/token/refresh/", { token: state.refreshToken })
			.then((response) => {
				commit("SET_ACCESS_TOKEN", response.data.access);
				commit("SET_REFRESH_TOKEN", response.data.refresh);
				return response.data;
			})
			.finally(() => {});
	},
	logout({ commit }) {
		return session
			.post("api/authorize/logout/", { token: state.refreshToken })
			.then((response) => {
				commit("LOGOUT");
				return response.data;
			})
			.finally(() => {});
	},
};

export default {
	namespaced: true,
	state,
	getters,
	mutations,
	actions,
};
