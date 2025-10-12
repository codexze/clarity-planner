import session from '@/core/utils/Session';

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
  SET_COMPANIES(state, companies) {
    state.companies = companies;
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
    const genders = await session.get('api/v1/clients/genders/');
    commit('SET_GENDERS', genders.data);
    return genders.data;
  },
  async filterKnownAddresses({ commit }, params) {
    const addresses = await session.get('api/v1/clients/known-addresses/filter/', { params: params });
    return addresses.data;
  },
  async getClientReminders({ commit }, id) {
    const reminders = await session.get(`api/v1/clients/clients/${id}/reminders/`);
    return reminders.data;
  },
  async getClients({ commit }) {
    const clients = await session.get('api/v1/clients/clients/');
    commit('SET_CLIENTS', clients.data);
    return clients.data;
  },
  async getClientById({ commit }, id) {
    const client = await session.get(`api/v1/clients/clients/${id}`);
    commit('SET_CLIENT', client.data);
    return client.data;
  },
  async filterClients({ commit }, params) {
    const clients = await session.get('api/v1/clients/clients/filter/', { params: params });
    return clients.data;
  },
  createClient({ commit }, data) {
    return session
      .post(`api/v1/clients/clients/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateClientById({ commit }, data) {
    return session
      .put(`api/v1/clients/clients/${data.id}/`, data)
      .then((response) => {
        commit('SET_CLIENT', response.data);
        return response.data;
      })
      .finally(() => {});
  },
  async filterClientAppointments({ commit }, params) {
    const appointments = await session.get(`api/v1/clients/clients/${params.client_id}/appointments/`, { params: params });
    return appointments.data;
  },
  updateKnownAddress({ commit }, data) {
    return session
      .patch(`api/v1/clients/known-addresses/${data.id}/set_active/`, data)
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
