import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { authGuard } from "@auth0/auth0-vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/welcome",
  },

  {
    path: "/welcome",
    name: "welcome",
    component: () => import("@/views/WelcomePage.vue"),
  },

  {
    path: "/today",
    name: "today",
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

export default createRouter({
  history: createWebHistory(),
  routes,
});
