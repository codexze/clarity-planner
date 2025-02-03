import { createRouter, createWebHistory } from "vue-router";
import { useStore } from "vuex";

import Login from "@/views/Login.vue";
import Services from "@/views/Services.vue";

const redirectLogout = (to, from, next) => {
	const store = useStore();
	store.dispatch("auth/logout").then(() => next({ path: "/login", replace: true, query: { redirect: from.fullPath } }));
};

// prettier-ignore
const baseRoutes = [{ path: "/" }, 
	{ path: "/login", name: "login", component: Login }, 
	{ path: "/logout", name:"logout", beforeEnter: redirectLogout }, 
	{ path: "/services", component: Services, meta: { requiresAuth: true } }];

const routes = baseRoutes;

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
});

// Route guard for authentication
router.beforeEach((to, from, next) => {
	const store = useStore();

	if (to.meta.requiresAuth && !store.getters["auth/isAuthenticated"]) {
		next("/");
	} else {
		next();
	}
});

export default router;
