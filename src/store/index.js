import { createStore } from "vuex";

import auth from "./modules/auth";
import services from "./modules/services";
import clients from "./modules/clients";
import planning from "./modules/planning";
import staff from "./modules/staff";

export default createStore({
	modules: {
		auth,
		services,
		clients,
		planning,
		staff,
	},
});
