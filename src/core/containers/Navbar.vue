<template>
	<Disclosure as="nav" class="bg-gray-800" v-slot="{ open }">
		<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
			<div class="flex h-16 items-center justify-between">
				<div class="flex items-center">
					<div class="shrink-0">
						<!-- <img class="size-8" src="https://tailç≈indui.com/plus/img/logos/mark.svg?color=gray&shade=500" alt="Your Company" /> -->
					</div>
					<div class="hidden md:block">
						<div class="ml-10 flex items-baseline space-x-4">
							<a v-for="item in navigation" :key="item.name" :href="item.href" :class="[item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white', 'rounded-md px-3 py-2 text-sm font-medium']" :aria-current="item.current ? 'page' : undefined">{{ item.name }}</a>
						</div>
					</div>
				</div>

				<div class="hidden md:block">
					<div class="ml-4 flex items-center md:ml-6">
						<!-- Profile dropdown -->
						<Menu as="div" class="relative ml-3">
							<div>
								<MenuButton class="inline-flex w-full justify-center rounded-md py-2 text-sm font-medium text-white not-first:focus:outline-none focus-visible:ring-2 focus-visible:ring-black/75">
									<span class="flex w-2 h-2 me-2 bg-green-500 rounded-full"></span>
									{{ store.state.auth.user?.name }}
								</MenuButton>
							</div>
							<transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
								<MenuItems class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 ring-1 shadow-lg ring-black/5 focus:outline-hidden">
									<MenuItem v-for="item in user_navigation" :key="item.name" v-slot="{ active }">
										<a :href="item.href" :class="[active ? 'bg-gray-100 outline-hidden' : '', 'block px-4 py-2 text-sm text-gray-700']">{{ item.name }}</a>
									</MenuItem>
								</MenuItems>
							</transition>
						</Menu>
					</div>
				</div>

				<div class="-mr-2 flex md:hidden">
					<!-- Mobile menu button -->
					<DisclosureButton class="relative inline-flex items-center justify-center rounded-md bg-gray-800 p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800 focus:outline-hidden">
						<span class="absolute -inset-0.5" />
						<span class="sr-only">Open main menu</span>
						<Bars3Icon v-if="!open" class="block size-6" aria-hidden="true" />
						<XMarkIcon v-else class="block size-6" aria-hidden="true" />
					</DisclosureButton>
				</div>
			</div>
		</div>
		<transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-out" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
			<DisclosurePanel class="md:hidden">
				<div class="space-y-1 px-2 pt-2 pb-3 sm:px-3">
					<DisclosureButton v-for="item in navigation" :key="item.name" as="a" :href="item.href" :class="[item.current ? 'bg-gray-900 text-white' : 'text-gray-300 hover:bg-gray-700 hover:text-white', 'block rounded-md px-3 py-2 text-base font-medium']" :aria-current="item.current ? 'page' : undefined">{{ item.name }}</DisclosureButton>
				</div>
			</DisclosurePanel>
		</transition>
	</Disclosure>
</template>

<script setup>
import { Disclosure, DisclosurePanel, DisclosureButton, Menu, MenuItems, MenuItem, MenuButton } from "@headlessui/vue";
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/solid";
import { useStore } from "vuex";

defineProps({
	navigation: Array,
	user_navigation: Array,
});

const store = useStore();
</script>
