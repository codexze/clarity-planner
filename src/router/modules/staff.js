import DefaultContainer from "@/views/staff/containers/DefaultContainer.vue";
import Staff from "@/views/staff/views/StaffView.vue";
import StaffMemberDetails from "@/views/staff/views/StaffMemberDetailsView.vue";

const routes = [
	{
		path: "/staff",
		component: DefaultContainer,
		meta: { requiresAuth: true },
		children: [
			{
				path: "",
				component: Staff,
				meta: { requiresAuth: true },
			},
			{
				path: ":memberId/view",
				component: StaffMemberDetails,
				meta: { requiresAuth: true },
			},
		],
	},
];

export default routes;
