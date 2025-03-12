import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import store from "./store";

import { library } from "@fortawesome/fontawesome-svg-core";

// Import All Free FontAwesome Icons
import { fas } from "@fortawesome/free-solid-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { mask } from "vue-the-mask";
import Toast from "vue-toastification";

import "./assets/css/main.css";

import { Socket } from "./core/utils/Socket";
import EventBus from "./core/utils/EventBus";

import mixins from "./core/mixins";

const toast_options = {
	transition: "Vue-Toastification__bounce",
	maxToasts: 20,
	newestOnTop: true,
};

const app = createApp(App);

axios.defaults.baseURL = "http://127.0.0.1:8000/api/";

app.use(store);
app.use(router);

library.add(fas, far, fab);
app.component("font-awesome-icon", FontAwesomeIcon);
app.directive("mask", mask);
app.use(Toast, toast_options);

app.use(Socket);
app.config.globalProperties.$eventBus = EventBus; // Attach event bus globally

app.mixin(mixins);

app.mount("#app");
