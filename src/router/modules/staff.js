import DefaultContainer from '@/views/staff/containers/DefaultContainer.vue';
import Staff from '@/views/staff/views/StaffView.vue';
import EmployeeDetailsView from '@/views/staff/views/EmployeeDetailsView.vue';
import NewEmployeeView from '@/views/staff/views/NewEmployeeView.vue';

const routes = [
  {
    path: '/staff',
    component: DefaultContainer,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: Staff,
        meta: {
          title: 'Staff',
          description: 'Manage your staff members',
          requiresAuth: true,
        },
      },
      {
        path: ':employeeId/view',
        component: EmployeeDetailsView,
        meta: {
          title: 'Employee Details',
          description: 'View and edit employee details',
          requiresAuth: true,
        },
      },
      {
        path: 'new',
        component: NewEmployeeView,
        meta: {
          title: 'New Employee',
          description: 'Create a new employee record',
          requiresAuth: true,
        },
      },
    ],
  },
];

export default routes;
