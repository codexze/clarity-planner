import DefaultContainer from "@/views/services/containers/DefaultContainer.vue";
import Services from "@/views/services/views/ServicesView.vue";
import ServiceDetails from "@/views/services/views/ServiceDetailsView.vue";
import NewServiceView from "@/views/services/views/NewServiceView.vue";

const routes = [
	{
		path: "/services",
		component: DefaultContainer,
		meta: { requiresAuth: true },
		children: [
			{
				path: "",
				component: Services,
				meta: {
					title: "Services",
					requiresAuth: true,
				},
			},
			{
				path: ":serviceId/view",
				component: ServiceDetails,
				meta: {
					title: "Service Details",
					requiresAuth: true,
				},
			},
			{
				path: "new",
				component: NewServiceView,
				meta: {
					title: "New Service",
					requiresAuth: true,
				},
			},
		],
	},
];

export default routes;
