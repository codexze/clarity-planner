import session from "@/core/utils/Session";

const state = {
	member: null,
	staff: [],
};

const getters = {
	getStaff: (state) => state.staff,
	getEmployee: (state) => state.employee,
};

const mutations = {
	SET_EMPLOYEE(state, employee) {
		state.employee = employee;
	},
	SET_STAFF(state, staff) {
		state.staff = staff;
	},
};

const actions = {
	async getStaff({ commit }) {
		const staff = await session.get("api/inhouse/staff/");
		commit("SET_STAFF", staff.data);
		return staff.data;
	},
	async getEmployeeByUsername({ commit }, username) {
		const employee = await session.get(`api/inhouse/staff/${username}`);
		commit("SET_EMPLOYEE", employee.data);
		return employee.data;
	},
	async getEmployeesByServiceType({ commit }, type) {
		const services = await session.get(`api/inhouse/staff/service_type/${type}/`);
		return services.data;
	},
	async filterStaff({ commit }, params) {
		const staff = await session.get("api/inhouse/staff/filter/", { params: params });
		return staff.data;
	},
	updateEmployeeByUsername({ commit }, data) {
		return session
			.put(`api/inhouse/staff/${data.username}/`, data)
			.then((response) => {
				commit("SET_EMPLOYEE", response.data);
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
