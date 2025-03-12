import session from "@/core/utils/Session";
import moment from "moment";
const state = {
	settings: {
		calendar: {},
		days: [],
		events: [],
	},
	employee: {},
	employees: [],
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
};

const actions = {
	loadIntervalTime({ commit }, { start, end, interval }) {
		return new Promise((resolve, reject) => {
			let mStart = moment(start, "HH:mm");
			let mEnd = moment(end, "HH:mm");
			const it = [];

			it.push(mStart.format("HH:mm"));
			while (mStart < mEnd) {
				let minutes = mStart.add(interval, "minutes");
				it.push(moment(minutes).format("HH:mm"));
			}

			resolve(it);
		});
	},
	async getConfig({ state, commit }) {
		const config = await session.get(`api/planning/employees/${state.employee?.username}/config/`);
		commit("SET_SETTINGS", { key: "calendar", value: config.data });
		return config.data;
	},
	async getEmployeeByUsername({ commit }, username) {
		const employee = await session.get(`api/planning/employees/${username}/`);
		commit("SET_EMPLOYEE", employee.data);
		return employee.data;
	},
	async getEmployees({ commit }) {
		const employees = await session.get(`api/planning/employees/limited/`);
		commit("SET_EMPLOYEES", employees.data);
		return employees.data;
	},
};

export default {
	namespaced: true,
	state,
	getters,
	mutations,
	actions,
};
