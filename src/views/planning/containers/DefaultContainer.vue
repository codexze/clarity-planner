<template>
  <div class="min-h-screen flex bg-gradient-to-b from-gray-50 via-gray-100 to-gray-50">
    <Sidebar :current_user="user" :navigation="navigation" :user_navigation="userNavigation" />
    <div class="flex-1 flex flex-col min-h-screen lg:pl-64">
      <Header :label="$route.meta.title || 'Dashboard'" :show-back-button="true" />
      <main class="flex-1 overflow-y-auto">
        <div class="mx-auto max-w-8xl px-4 py-6 sm:px-6 lg:px-8">
          <router-view :key="$route.fullPath"></router-view>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/core/containers/Sidebar.vue';
import Header from '@/core/containers/Header.vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { HomeIcon, CalendarIcon, ClockIcon, UserGroupIcon, WrenchScrewdriverIcon, UsersIcon, UserIcon, Cog6ToothIcon, BuildingOfficeIcon, ArrowRightEndOnRectangleIcon } from '@heroicons/vue/24/outline';

const store = useStore();
const user = store.state.auth.user;
const router = useRouter();

import { computed } from 'vue';

const navigation = computed(() => [
  { name: 'Home', href: '/dashboard', icon: HomeIcon, current: router.currentRoute.value.path === '/dashboard' },
  { name: 'Calendar', href: `/planning/${user?.username}/calendar`, icon: CalendarIcon, current: router.currentRoute.value.path.includes('calendar') },
  { name: 'Appointments', href: `/planning/${user?.username}/appointments`, icon: ClockIcon, current: router.currentRoute.value.path.includes('appointments') },
  { name: 'Companies', href: '/companies', icon: BuildingOfficeIcon, current: false },
  { name: 'Clients', href: '/clients', icon: UserGroupIcon, current: router.currentRoute.value.path.includes('clients') },
  { name: 'Services', href: '/services', icon: WrenchScrewdriverIcon, current: router.currentRoute.value.path.includes('services') },
  { name: 'Staff', href: '/staff', icon: UsersIcon, current: router.currentRoute.value.path.includes('staff') },
]);
const userNavigation = [
  { name: 'Account', href: '/account', icon: UserIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
  { name: 'Sign out', href: '/logout', icon: ArrowRightEndOnRectangleIcon },
];
</script>
