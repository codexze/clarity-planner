<template>
	<div>
		<!-- Mobile sidebar backdrop -->
		<div v-show="isMobileOpen" class="fixed inset-0 bg-gray-800/50 backdrop-blur-sm z-40 lg:hidden"
			@click="isMobileOpen = false"></div>

		<!-- Sidebar -->
		<aside
			:class="['fixed inset-y-0 left-0 z-50 w-64 bg-blue-500 flex flex-col transition-transform duration-300 ease-in-out', 'lg:translate-x-0', isMobileOpen ? 'translate-x-0' : '-translate-x-full']">
			<!-- Logo area -->
			<div class="h-24 flex items-center px-6 border-b border-blue-400">
				<div class="shrink-0">
					<img class="h-auto w-53" src="@/assets/logo-light.png" alt="Clarity Logo" />
				</div>
				<!-- <h1 class="ml-3 text-xl font-semibold text-white">Clarity</h1> -->
			</div>

			<!-- Navigation -->
			<nav class="flex-1 overflow-y-auto mt-4 px-4 space-y-1">
				<router-link v-for="item in navigation" :key="item.name" :to="item.href"
					:class="[item.current ? 'bg-blue-700 text-white' : 'text-gray-50 hover:bg-blue-600 hover:text-white', 'flex items-center rounded-md px-4 py-2 text-sm font-medium w-full']"
					:aria-current="item.current ? 'page' : undefined">
					<component :is="item.icon" class="h-5 w-5 mr-3 flex-shrink-0" aria-hidden="true" />
					{{ item.name }}
				</router-link>
			</nav>

			<!-- User profile -->
			<div class="shrink-0 p-4 border-t border-blue-400">
				<Menu as="div" class="w-full relative">
					<MenuButton
						class="flex items-center w-full px-4 py-2 text-sm font-medium text-white rounded-md hover:bg-blue-600">
						<span>{{ store.state.auth.user?.name }}</span>
					</MenuButton>
					<transition enter-active-class="transition ease-out duration-100"
						enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
						leave-active-class="transition ease-in duration-75"
						leave-from-class="transform opacity-100 scale-100"
						leave-to-class="transform opacity-0 scale-95">
						<MenuItems
							class="absolute bottom-full mb-2 w-56 rounded-md bg-blue-400 py-1 shadow-lg ring-1 ring-black/5">
							<MenuItem v-for="item in user_navigation" :key="item.name" v-slot="{ active }">
							<router-link :to="item.href"
								:class="[active ? 'bg-blue-500' : '', 'flex items-center px-4 py-2 text-sm text-gray-50 hover:bg-blue-500']">
								<component :is="item.icon" class="h-5 w-5 mr-3 flex-shrink-0" aria-hidden="true" />
								{{ item.name }}
							</router-link>
							</MenuItem>
						</MenuItems>
					</transition>
				</Menu>
			</div>
		</aside>

		<!-- Mobile toggle button -->
		<div class="fixed top-4 right-4 z-50 lg:hidden">
			<button @click="isMobileOpen = !isMobileOpen"
				class="inline-flex items-center justify-center rounded-md bg-blue-600 p-2 text-gray-50 hover:bg-blue-500 hover:text-white focus:ring-2 focus:ring-white">
				<span class="sr-only">Open sidebar</span>
				<Bars3Icon v-if="!isMobileOpen" class="block size-6" aria-hidden="true" />
				<XMarkIcon v-else class="block size-6" aria-hidden="true" />
			</button>
		</div>
	</div>
</template>

<script setup>
import { Menu, MenuItems, MenuItem, MenuButton } from "@headlessui/vue";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/solid";
import { useStore } from "vuex";
import { ref } from "vue";

const props = defineProps({
	navigation: {
		type: Array,
		required: true,
		default: () => [],
	},
	user_navigation: {
		type: Array,
		required: true,
		default: () => [],
	},
});

const store = useStore();
const isMobileOpen = ref(false);
</script>
