import session from '@/core/utils/Session';
import moment from 'moment';
const state = {
  appointment: null,
};

const getters = {};

const mutations = {
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
  async filterAppointments({ commit }, params) {
    const appointments = await session.get('api/v1/planning/appointments/filter/', { params: params });
    return appointments.data;
  },
  async getAppointmentsByEmployee({ commit }, username) {
    const appointments = await session.get(`api/v1/planning/appointments/employee/${username}/`);
    return appointments.data;
  },
  async getAppointmentById({ commit }, id) {
    const appointment = await session.get(`api/v1/planning/appointments/${id}/`);
    commit('SET_APPOINTMENT', appointment.data);
    return appointment.data;
  },
  async getBlockedTimeByEmployee({ commit }, username) {
    const blocked = await session.get(`api/v1/planning/blocked/employee/${username}/`);
    return blocked.data;
  },
  async getBlockedTimeById({ commit }, id) {
    const blocked = await session.get(`api/v1/planning/blocked/${id}/`);
    return blocked.data;
  },
  async getReminderReasons({ commit }) {
    const reasons = await session.get('api/v1/planning/reminders/reasons/');
    return reasons.data;
  },
  async getRemindersByEmployee({ commit }, username) {
    const reminders = await session.get(`api/v1/planning/reminders/employee/${username}/`);
    return reminders.data;
  },
  async getReminderById({ commit }, id) {
    const reminder = await session.get(`api/v1/planning/reminders/${id}/`);
    return reminder.data;
  },
  async filterReminders({ commit }, params) {
    const reminders = await session.get('api/v1/planning/reminders/filter/', { params: params });
    return reminders.data;
  },
  createAppointment({ commit }, data) {
    return session
      .post(`api/v1/planning/appointments/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  rescheduleAppointment({ commit }, data) {
    return session
      .put(`api/v1/planning/appointments/${data.id}/reschedule/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateAppointment({ commit }, data) {
    return session
      .put(`api/v1/planning/appointments/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  createBlockedTime({ commit }, data) {
    return session
      .post(`api/v1/planning/blocked/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  rescheduleBlockedTime({ commit }, data) {
    return session
      .put(`api/v1/planning/blocked/${data.id}/reschedule/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateBlockedTime({ commit }, data) {
    return session
      .put(`api/v1/planning/blocked/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  createReminder({ commit }, data) {
    return session
      .post(`api/v1/planning/reminders/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  updateReminder({ commit }, data) {
    return session
      .put(`api/v1/planning/reminders/${data.id}/`, data)
      .then((response) => {
        return response.data;
      })
      .finally(() => {});
  },
  deleteReminder({ commit }, id) {
    return session
      .delete(`api/v1/planning/reminders/${id}/`)
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
