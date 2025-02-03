import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import store from "./store";

import "./assets/css/main.css";

import { Socket } from "./core/utils/Socket";
import EventBus from "./core/utils/EventBus";

import mixins from "./core/mixins";

const app = createApp(App);

axios.defaults.baseURL = "http://127.0.0.1:8000/api/";

app.use(store);
app.use(router);

app.use(Socket);
app.config.globalProperties.$eventBus = EventBus; // Attach event bus globally

app.mixin(mixins);

app.mount("#app");
