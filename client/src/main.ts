import { createApp } from "vue";
import { createPinia } from "pinia";
import { createAuth0 } from "@auth0/auth0-vue";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(
  createAuth0({
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
    authorizationParams: {
      redirect_uri: "http://localhost:5173/today",
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    },
  }),
);

app.use(createPinia());
app.use(router);

app.mount("#app");
