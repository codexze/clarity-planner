import DefaultContainer from "@/views/planning/containers/DefaultContainer.vue";
import CalendarView from "@/views/planning/views/CalendarView.vue";

const routes = [
	{
		path: "/planning/",
		component: DefaultContainer,
		meta: { requiresAuth: true },
		children: [
			{
				path: ":username",
				component: CalendarView,
				meta: { requiresAuth: true },
			},
		],
	},
];

export default routes;
