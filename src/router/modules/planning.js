import DefaultContainer from "@/views/planning/containers/DefaultContainer.vue";
import AppointmentsView from "@/views/planning/views/AppointmentsView.vue";
import AppointmentDetailsView from "@/views/planning/views/AppointmentDetailsView.vue";
import CalendarView from "@/views/planning/views/CalendarView.vue";

const routes = [
	{
		path: "/planning/",
		component: DefaultContainer,
		meta: { requiresAuth: true },
		children: [
			{
				path: ":username/calendar",
				component: CalendarView,
				meta: {
					title: "Calendar",
					requiresAuth: true,
				},
			},
			{
				path: ":username/appointments",
				component: AppointmentsView,
				meta: {
					title: "Appointments",
					requiresAuth: true,
				},
			},
			{
				path: ":username/appointments/:appointmentId/view",
				component: AppointmentDetailsView,
				meta: {
					title: "Appointment Details",
					requiresAuth: true,
				},
			},
			{
				path: ":username/appointments/new",
				// component: NewServiceView,
				meta: {
					title: "New Appointment",
					requiresAuth: true,
				},
			},
		],
	},
];

export default routes;
