import session from "@/core/utils/Session";

const state = {
	user: localStorage.getItem("userdata") ? JSON.parse(localStorage.getItem("userdata")) : null,
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
		localStorage.setItem("userdata", JSON.stringify(user));
	},
	SET_ACCESS_TOKEN(state, token) {
		state.accessToken = token;
		localStorage.setItem("access_token", token);
	},
	SET_REFRESH_TOKEN(state, token) {
		state.refreshToken = token;
		localStorage.setItem("refresh_token", token);
	},
};

const actions = {
	login({ commit, dispatch }, credentials) {
		return session
			.post("api/authorize/token/", credentials)
			.then(async (response) => {
				commit("SET_ACCESS_TOKEN", response.data.access);
				commit("SET_REFRESH_TOKEN", response.data.refresh);

				await dispatch("current");
				return response.data;
			})
			.finally(() => {});
	},
	refresh_token({ commit }) {
		return session
			.post("api/authorize/token/refresh/", { refresh: state.refreshToken })
			.then((response) => {
				commit("SET_ACCESS_TOKEN", response.data.access);
				commit("SET_REFRESH_TOKEN", response.data.refresh);
				return response.data;
			})
			.finally(() => {});
	},
	async current({ commit }) {
		const response = await session.get("api/authorize/current/");
		commit("SET_USER", response.data); // Store user data in Vuex
		return response.data;
	},
	async logout({ commit }) {
		// const response = await session.post("api/authorize/logout/", { token: state.refreshToken });
		commit("SET_ACCESS_TOKEN", "");
		commit("SET_REFRESH_TOKEN", "");
		commit("SET_USER", null); // Store user data in Vuex
	},
};

export default {
	namespaced: true,
	state,
	getters,
	mutations,
	actions,
};
