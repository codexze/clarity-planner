import DefaultContainer from '@/views/employees/containers/DefaultContainer.vue';
import Employee from '@/views/employees/views/EmployeesView.vue';
import EmployeeDetailsView from '@/views/employees/views/EmployeeDetailsView.vue';
import NewEmployeeView from '@/views/employees/views/NewEmployeeView.vue';

const routes = [
  {
    path: '/employees',
    component: DefaultContainer,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: Employee,
        meta: {
          title: 'Employee',
          description: 'Manage your employee members',
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
