import DefaultContainer from "@/views/clients/containers/DefaultContainer.vue";
import Clients from "@/views/clients/views/ClientsView.vue";
import ClientDetails from "@/views/clients/views/ClientDetailsView.vue";
import NewClientView from "@/views/clients/views/NewClientView.vue";

const routes = [
	{
		path: "/clients",
		component: DefaultContainer,
		meta: { requiresAuth: true },
		children: [
			{
				path: "",
				component: Clients,
				meta: { requiresAuth: true },
			},
			{
				path: ":clientId/view",
				component: ClientDetails,
				meta: { requiresAuth: true },
			},
			{
				path: "new",
				component: NewClientView,
				meta: { requiresAuth: true },
			},
		],
	},
];

export default routes;
