import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { authGuard } from "@auth0/auth0-vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "welcome",
    component: () => import("@/views/WelcomePage.vue"),
  },
  {
    path: "/today",
    name: "home",
    component: () => import("@/views/TodaysQuestionPage.vue"),
    beforeEnter: authGuard,
  },
  {
    path: "/create",
    name: "create-question",
    component: () => import("@/views/CreateQuestionPage.vue"),
    beforeEnter: authGuard,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
