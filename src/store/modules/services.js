import session from "@/core/utils/Session";

const state = {
	service: null,
	types: [],

	services: [],
};

const getters = {
	getServices: (state) => state.services,
	getService: (state) => state.service,
};

const mutations = {
	SET_SERVICETYPES(state, types) {
		state.types = types;
	},
	SET_SERVICE(state, service) {
		state.service = service;
	},
	SET_SERVICES(state, services) {
		state.services = services;
	},
};

const actions = {
	async getServiceTypes({ commit }) {
		const types = await session.get("api/services/service_types/");
		commit("SET_SERVICETYPES", types.data);
		return types.data;
	},
	async getServicesByType({ commit }, type) {
		const services = await session.get(`api/services/namespace/type/${type}`);
		commit("SET_SERVICES", services.data);
		return services.data;
	},
	async getServices({ commit }) {
		const services = await session.get("api/services/namespace/");
		commit("SET_SERVICES", services.data);
		return services.data;
	},
	async getServiceById({ commit }, id) {
		const service = await session.get(`api/services/namespace/${id}`);
		commit("SET_SERVICE", service.data);
		return service.data;
	},
	async filterServices({ commit }, params) {
		const services = await session.get("api/services/namespace/filter/", { params: params });
		return services.data;
	},
	createService({ commit }, data) {
		return session
			.post(`api/services/namespace/`, data)
			.then((response) => {
				return response.data;
			})
			.finally(() => {});
	},
	updateServiceById({ commit }, data) {
		return session
			.put(`api/services/namespace/${data.id}/`, data)
			.then((response) => {
				commit("SET_SERVICE", response.data);
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
