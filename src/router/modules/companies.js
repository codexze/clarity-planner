import DefaultContainer from '@/views/companies/containers/DefaultContainer.vue';
import Companies from '@/views/companies/views/CompaniesView.vue';
import CompanyDetails from '@/views/companies/views/CompanyDetailsView.vue';
import NewCompanyView from '@/views/companies/views/NewCompanyView.vue';

const routes = [
  {
    path: '/companies',
    component: DefaultContainer,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        component: Companies,
        meta: {
          title: 'Companies',
          description: 'Manage your companies',
          requiresAuth: true,
        },
      },
      {
        path: ':companyId/view',
        component: CompanyDetails,
        meta: {
          title: 'Company Details',
          description: 'View and edit company details',
          requiresAuth: true,
        },
      },
      {
        path: 'new',
        component: NewCompanyView,
        meta: {
          title: 'New Company',
          description: 'Create a new company',
          requiresAuth: true,
        },
      },
    ],
  },
];

export default routes;
