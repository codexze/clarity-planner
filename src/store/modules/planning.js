import session from '@/core/utils/Session';
import moment from 'moment';
const state = {
  settings: {
    calendar: {},
    days: [],
    events: [],
  },
  employee: {},
  employees: [],

  appointment: null,
};

const getters = {};

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
  SET_APPOINTMENT(state, appointment) {
    state.appointment = appointment;
  },
};

const actions = {
  loadIntervalTime({ commit }, { start, end, interval }) {
    return new Promise((resolve, reject) => {
      let mStart = moment(start, 'HH:mm');
      let mEnd = moment(end, 'HH:mm');
      const it = [];

      it.push(mStart.format('HH:mm'));
      while (mStart < mEnd) {
        let minutes = mStart.add(interval, 'minutes');
        it.push(moment(minutes).format('HH:mm'));
      }

      resolve(it);
    });
  },
  async getConfig({ state, commit }) {
    const config = await session.get(`api/planning/employees/${state.employee?.username}/config/`);
    commit('SET_SETTINGS', { key: 'calendar', value: config.data });
    return config.data;
  },
  async getEmployeeByUsername({ commit }, username) {
    const employee = await session.get(`api/planning/employees/${username}/`);
    commit('SET_EMPLOYEE', employee.data);
    return employee.data;
  },
  async getEmployees({ commit }) {
    const employees = await session.get(`api/planning/employees/limited/`);
    commit('SET_EMPLOYEES', employees.data);
    return employees.data;
  },
  async filterAppointments({ commit }, params) {
    const appointments = await session.get('api/planning/appointments/filter/', { params: params });
    return appointments.data;
  },
  async getAppointmentById({ commit }, id) {
    const appointment = await session.get(`api/planning/appointments/${id}/`);
    commit('SET_APPOINTMENT', appointment.data);
    return appointment.data;
  },
  async filterReminder({ commit }, params) {
    const reminders = await session.get('api/planning/reminders/filter/', { params: params });
    return reminders.data;
  },
  async getBlockedById({ commit }, id) {
    const blocked = await session.get(`api/planning/blocked/${id}/`);
    return blocked.data;
  },
  async filterReminders({ commit }, params) {
    const reminders = await session.get('api/planning/reminders/filter/', { params: params });
    return reminders.data;
  },
  createAppointment({ commit }, data) {
    return session
      .post(`api/planning/appointments/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  rescheduleAppointment({ commit }, data) {
    return session
      .put(`api/planning/appointments/${data.id}/reschedule/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateAppointment({ commit }, data) {
    return session
      .put(`api/planning/appointments/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  createBlocked({ commit }, data) {
    return session
      .post(`api/planning/blocked/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  rescheduleBlocked({ commit }, data) {
    return session
      .put(`api/planning/blocked/${data.id}/reschedule/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateBlocked({ commit }, data) {
    return session
      .put(`api/planning/blocked/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  createReminder({ commit }, data) {
    return session
      .post(`api/planning/reminders/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateReminder({ commit }, data) {
    return session
      .put(`api/planning/reminders/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  deleteReminder({ commit }, id) {
    return session
      .delete(`api/planning/reminders/${id}/`)
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
