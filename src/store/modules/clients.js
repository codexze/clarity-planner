import session from "@/core/utils/Session";

const state = {
	client: null,
	genders: [],

	clients: [],
};

const getters = {
	getClients: (state) => state.clients,
	getClient: (state) => state.client,
};

const mutations = {
	SET_GENDERS(state, genders) {
		state.genders = genders;
	},
	SET_CLIENT(state, client) {
		state.client = client;
	},
	SET_CLIENTS(state, clients) {
		state.clients = clients;
	},
};

const actions = {
	async getGenders({ commit }) {
		const genders = await session.get("api/clients/genders/");
		commit("SET_GENDERS", genders.data);
		return genders.data;
	},
	async getClients({ commit }) {
		const clients = await session.get("api/clients/namespace/");
		commit("SET_CLIENTS", clients.data);
		return clients.data;
	},
	async getClientById({ commit }, id) {
		const client = await session.get(`api/clients/namespace/${id}`);
		commit("SET_CLIENT", client.data);
		return client.data;
	},
	async filterClients({ commit }, params) {
		const clients = await session.get("api/clients/namespace/filter/", { params: params });
		return clients.data;
	},
	createClient({ commit }, data) {
		return session
			.post(`api/clients/namespace/`, data)
			.then((response) => {
				return response.data;
			})
			.finally(() => {});
	},
	updateClientById({ commit }, data) {
		return session
			.put(`api/clients/namespace/${data.id}/`, data)
			.then((response) => {
				commit("SET_CLIENT", response.data);
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
