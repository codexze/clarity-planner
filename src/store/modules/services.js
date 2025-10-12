import session from '@/core/utils/Session';

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
    const types = await session.get('api/v1/services/service-types/');
    commit('SET_SERVICETYPES', types.data);
    return types.data;
  },
  async getServicesByType({ commit }, type) {
    const services = await session.get(`api/v1/services/services/type/${type}`);
    return services.data;
  },
  async getServices({ commit }) {
    const services = await session.get('api/v1/services/services/');
    commit('SET_SERVICES', services.data);
    return services.data;
  },
  async getServiceById({ commit }, id) {
    const service = await session.get(`api/v1/services/services/${id}`);
    commit('SET_SERVICE', service.data);
    return service.data;
  },
  async filterServices({ commit }, params) {
    const services = await session.get('api/v1/services/services/filter/', { params: params });
    return services.data;
  },
  createService({ commit }, data) {
    return session
      .post(`api/v1/services/services/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateServiceById({ commit }, data) {
    return session
      .put(`api/v1/services/services/${data.id}/`, data)
      .then((response) => {
        commit('SET_SERVICE', response.data);
        return response.data;
      })
      .finally(() => {});
  },
  async getAddonsByType({ commit }, type) {
    const addon = await session.get(`api/v1/services/addons/type/${type}`);
    return addon.data;
  },
  async filterAddons({ commit }, params) {
    const addons = await session.get('api/v1/services/addons/filter/', { params: params });
    return addons.data;
  },
  createAddon({ commit }, data) {
    return session
      .post(`api/v1/services/addons/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateAddonById({ commit }, data) {
    return session
      .put(`api/v1/services/addons/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  async activateAddon({ commit }, data) {
    return session
      .patch(`api/v1/services/addons/${data.id}/activate/`, { consistency_token: data.consistency_token })
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  async deactivateAddon({ commit }, data) {
    return session
      .patch(`api/v1/services/addons/${data.id}/deactivate/`, { consistency_token: data.consistency_token })
      .then((response) => {
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
