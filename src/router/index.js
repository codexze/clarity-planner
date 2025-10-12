import { createRouter, createWebHistory } from 'vue-router';
import { useStore } from 'vuex';

import Login from '@/views/auth/views/Login.vue';

import DefaultContainer from '@/views/auth/containers/DefaultContainer.vue';
import Dashboard from '@/views/auth/views/Dashboard.vue';

import serviceRoutes from './modules/services';
import companyRoutes from './modules/companies';
import clientRoutes from './modules/clients';
import planningRoutes from './modules/planning';
import employeesRoutes from './modules/employees';

const redirectLogout = (to, from, next) => {
  const store = useStore();
  store.dispatch('auth/logout').then(() => {
    next({ path: '/login', replace: true, query: { redirect: from.fullPath } });
  });
};

// prettier-ignore
const baseRoutes = [
	{
		path: "/",
		redirect: "/dashboard", // Redirect root path to dashboard or another existing route
	},
	{
		path: "/login",
		name: "login",
		component: Login,
		meta: { anonymous: true },
	},
	{
		path: "/dashboard",
		component: DefaultContainer,
		meta: { requiresAuth: true },
		children: [
			{
				path: "",
				component: Dashboard,
				meta: { requiresAuth: true },
			},
		],
	},
	{ 
		path: "/logout", 
		name: "logout", 
		beforeEnter: redirectLogout 
	},
	
];

const routes = baseRoutes.concat(serviceRoutes, companyRoutes, clientRoutes, planningRoutes, employeesRoutes);

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Route guard for authentication
router.beforeEach(async (to, from, next) => {
  const store = useStore();

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  const isAuthenticated = store.getters['auth/isAuthenticated'];
  const token = store.getters['auth/getRefreshToken'];

  if (requiresAuth) {
    if (!isAuthenticated) {
      // Redirect to login page if authentication is required but no token exists
      next('/login');
    } else {
      // Optional: Check if token is expired
      const payload = JSON.parse(atob(token.split('.')[1]));
      const isExpired = Date.now() >= payload.exp * 1000;

      if (isExpired) {
        // Token is expired, clear it
        next('/logout');
      } else {
        next();
      }
    }
  } else if (to.path === '/login' && isAuthenticated) {
    // Redirect to home/dashboard if user is already logged in
    next('/dashboard');
  } else {
    // Proceed as normal
    next();
  }
});

export default router;
