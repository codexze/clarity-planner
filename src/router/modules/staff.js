import DefaultContainer from "@/views/staff/containers/DefaultContainer.vue";
import Staff from "@/views/staff/views/StaffView.vue";
import EmployeeDetailsView from "@/views/staff/views/EmployeeDetailsView.vue";

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
				path: ":employeeId/view",
				component: EmployeeDetailsView,
				meta: { requiresAuth: true },
			},
		],
	},
];

export default routes;
