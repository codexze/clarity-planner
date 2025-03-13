<template>
	<div class="h-full">
		<Navbar :current_user="user" :navigation="navigation" :user_navigation="userNavigation" />
		<Header label="Dashboard"></Header>
		<main>
			<div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
				<router-view :key="$route.fullPath"></router-view>
			</div>
		</main>
	</div>
</template>

<script setup>
import Navbar from "@/core/containers/Navbar.vue";
import Header from "@/core/containers/Header.vue";
import { useStore } from "vuex";

const store = useStore();

const user = store.state.auth.user;

const navigation = [
	{ name: "Home", href: "/dashboard", current: true },
	{ name: "Planning", href: `/planning/${user?.username}`, current: false },
	{ name: "Clients", href: "/clients", current: false },
	{ name: "Services", href: "/services", current: false },
	{ name: "Staff", href: "/staff", current: false },
];
const userNavigation = [
	{ name: "Account", href: "/account" },
	{ name: "Settings", href: "/settings" },
	{ name: "Sign out", href: "/logout" },
];
</script>
