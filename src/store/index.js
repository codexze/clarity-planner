import { createStore } from 'vuex';

import auth from './modules/auth';
import services from './modules/services';
import clients from './modules/clients';
import companies from './modules/companies';
import planning from './modules/planning';
import employees from './modules/employees';

export default createStore({
  modules: {
    auth,
    services,
    clients,
    companies,
    planning,
    employees,
  },
});
