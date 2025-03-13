import session from "@/core/utils/Session";

const state = {
	member: null,
	staff: [],
};

const getters = {
	getStaff: (state) => state.staff,
	getMember: (state) => state.client,
};

const mutations = {
	SET_MEMBER(state, client) {
		state.client = client;
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
	async getMemberById({ commit }, id) {
		const client = await session.get(`api/inhouse/staff/${id}`);
		commit("SET_MEMBER", client.data);
		return client.data;
	},
	async filterStaff({ commit }, params) {
		const staff = await session.get("api/inhouse/staff/filter/", { params: params });
		return staff.data;
	},
	updateMemberById({ commit }, data) {
		return session
			.put(`api/inhouse/staff/${data.id}/`, data)
			.then((response) => {
				commit("SET_MEMBER", response.data);
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
