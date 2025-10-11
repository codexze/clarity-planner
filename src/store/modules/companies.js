import session from '@/core/utils/Session';

const state = {
  company: null,
  companies: [],
};

const getters = {
  getCompanies: (state) => state.companies,
  getCompany: (state) => state.company,
};

const mutations = {
  SET_COMPANY(state, company) {
    state.company = company;
  },
  SET_COMPANIES(state, companies) {
    state.companies = companies;
  },
};

const actions = {
  async getCompanies({ commit }) {
    const companies = await session.get('api/clients/companies/all/');
    commit('SET_COMPANIES', companies.data);
    return companies.data;
  },
  async getCompanyById({ commit }, id) {
    const company = await session.get(`api/clients/companies/${id}/`);
    commit('SET_COMPANY', company.data);
    return company.data;
  },
  async filterCompanies({ commit }, params) {
    const companies = await session.get('api/clients/companies/filter/', { params: params });
    return companies.data;
  },
  createCompany({ commit }, data) {
    return session
      .post(`api/clients/companies/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateCompanyById({ commit }, data) {
    return session
      .put(`api/clients/companies/${data.id}/`, data)
      .then((response) => {
        commit('SET_COMPANY', response.data);
        return response.data;
      })
      .finally(() => {});
  },
  deleteCompanyById({ commit }, id) {
    return session
      .delete(`api/clients/companies/${id}/`)
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
