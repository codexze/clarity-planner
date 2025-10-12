import session from '@/core/utils/Session';

const state = {
  settings: {
    calendar: {},
    days: [],
    events: [],
  },
  employee: null,
  employees: [],
};

const getters = {
  getEmployees: (state) => state.employees,
  getEmployee: (state) => state.employee,
};

const mutations = {
  SET_SETTINGS(state, obj) {
    state.settings[obj.key] = obj.value;
  },
  SET_EMPLOYEE(state, employee) {
    state.employee = employee;
  },
  SET_EMPLOYEES(state, employees) {
    state.employees = employees;
  },
};

const actions = {
  async getConfig({ state, commit }) {
    const config = await session.get(`api/v1/employees/employees/${state.employee?.username}/config/`);
    commit('SET_SETTINGS', { key: 'calendar', value: config.data });
    return config.data;
  },
  async getEmployees({ commit }) {
    const employee = await session.get('api/v1/employees/employees/');
    commit('SET_EMPLOYEES', employee.data);
    return employee.data;
  },
  async getEmployeeByUsername({ commit }, username) {
    const employee = await session.get(`api/v1/employees/employees/${username}`);
    commit('SET_EMPLOYEE', employee.data);
    return employee.data;
  },
  async getEmployeesByServiceType({ commit }, type) {
    const services = await session.get(`api/v1/employees/employees/service_type/${type}/`);
    return services.data;
  },
  async filterEmployees({ commit }, params) {
    const employee = await session.get('api/v1/employees/employees/filter/', { params: params });
    return employee.data;
  },
  updateEmployeeByUsername({ commit }, data) {
    return session
      .put(`api/v1/employees/employees/${data.username}/`, data)
      .then((response) => {
        commit('SET_EMPLOYEE', response.data);
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
