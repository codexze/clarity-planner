import DefaultContainer from '@/views/planning/containers/DefaultContainer.vue';
import AppointmentsView from '@/views/planning/views/AppointmentsView.vue';
import AppointmentDetailsView from '@/views/planning/views/AppointmentDetailsView.vue';
import CalendarView from '@/views/planning/views/CalendarView.vue';

const routes = [
  {
    path: '/planning/',
    component: DefaultContainer,
    meta: { requiresAuth: true },
    children: [
      {
        path: ':username/calendar',
        component: CalendarView,
        meta: {
          title: 'Calendar',
          description: 'View and manage your schedule using the calendar interface.',
          requiresAuth: true,
        },
      },
      {
        path: ':username/appointments',
        component: AppointmentsView,
        meta: {
          title: 'Appointments',
          description: 'Manage your appointments.',
          requiresAuth: true,
        },
      },
      {
        path: ':username/appointments/:appointmentId/view',
        name: 'AppointmentDetails',
        component: AppointmentDetailsView,
        meta: {
          title: 'Appointment Details',
          description: 'Review and modify the appointment information below.',
          requiresAuth: true,
        },
      },
      {
        path: ':username/appointments/new',
        meta: {
          title: 'New Appointment',
          requiresAuth: true,
        },
      },
    ],
  },
];

export default routes;
