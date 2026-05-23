import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { useAuth0 } from "@auth0/auth0-vue";
import { useAuthStore } from "@/stores/auth";
import { watch } from "vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomePage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/question/:id",
    name: "question",
    component: () => import("@/views/QuestionPage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/callback",
    name: "auth-callback",
    component: () => import("@/views/CallbackPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const auth0 = useAuth0();
  const authStore = useAuthStore();

  if (auth0.isLoading.value) {
    await new Promise((resolve) => {
      const unwatch = watch(
        () => auth0.isLoading.value,
        (loading) => {
          if (!loading) {
            unwatch();
            resolve(true);
          }
        },
        { immediate: true },
      );
    });
  }

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);

  if (requiresAuth) {
    if (auth0.isAuthenticated.value) {
      try {
        // Get access token for API calls
        await authStore.getAccessToken();
      } catch (error) {
        console.error("Error getting access token:", error);
      }
      next();
    } else {
      // Redirect to Auth0 login
      auth0.loginWithRedirect({
        appState: { target: to.fullPath },
      });
    }
  } else {
    next();
  }
});

export default router;
