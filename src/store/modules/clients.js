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
  async getReminderReasons({ commit }) {
    const reasons = await session.get('api/clients/reminder-reason/');
    return reasons.data;
  },
  async getGenders({ commit }) {
    const genders = await session.get('api/clients/genders/');
    commit('SET_GENDERS', genders.data);
    return genders.data;
  },
  async filterKnownAddresses({ commit }, params) {
    const addresses = await session.get('api/clients/known-addresses/filter/', { params: params });
    return addresses.data;
  },
  async getReminders({ commit }, id) {
    const reminders = await session.get(`api/clients/base/${id}/reminders/`);
    return reminders.data;
  },
  async getClients({ commit }) {
    const clients = await session.get('api/clients/base/');
    commit('SET_CLIENTS', clients.data);
    return clients.data;
  },
  async getClientById({ commit }, id) {
    const client = await session.get(`api/clients/base/${id}`);
    commit('SET_CLIENT', client.data);
    return client.data;
  },
  async filterClients({ commit }, params) {
    const clients = await session.get('api/clients/base/filter/', { params: params });
    return clients.data;
  },
  createClient({ commit }, data) {
    return session
      .post(`api/clients/base/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateClientById({ commit }, data) {
    return session
      .put(`api/clients/base/${data.id}/`, data)
      .then((response) => {
        commit('SET_CLIENT', response.data);
        return response.data;
      })
      .finally(() => {});
  },
  async filterClientAppointments({ commit }, params) {
    const appointments = await session.get(`api/clients/base/${params.client_id}/appointments/`, { params: params });
    return appointments.data;
  },
  updateKnownAddress({ commit }, data) {
    return session
      .patch(`api/clients/known-addresses/${data.id}/set_active/`, data)
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
