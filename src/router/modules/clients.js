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
				meta: {
					title: "Clients",
					requiresAuth: true,
				},
			},
			{
				path: ":clientId/view",
				component: ClientDetails,
				meta: {
					title: "Client Details",
					requiresAuth: true,
				},
			},
			{
				path: "new",
				component: NewClientView,
				meta: {
					title: "New Client",
					requiresAuth: true,
				},
			},
		],
	},
];

export default routes;
