import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState('auth', {
      user: (state) => state.current,
    }),
    userRoles() {
      return this.user ? this.user.roles : [];
    },
    isManager() {
      return this.userRoles.some((role) => role.name === 'manager');
    },
    isEmployee() {
      return this.userRoles.some((role) => role.name === 'employee');
    },
  },
  methods: {
    formatErrors(errorResponse) {
      if (errorResponse?.detail) {
        this.toastError(errorResponse.detail);
        return {};
      } else {
        return errorResponse;
      }
    },
    checkUserPermission(codename, user_permission) {
      if (this.user?.is_staff) return true; // override permissions for employee user

      const permissionExists = this.userRoles
        .flatMap((role) => role.permissions.filter((permission) => permission.codename)) // Filter out empty permissions
        .some((permission) => permission.codename === `${user_permission}_${codename}`);

      return permissionExists;
    },
  },
};
