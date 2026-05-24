import { computed } from "vue";
import { defineStore } from "pinia";
import { useAuth0 } from "@auth0/auth0-vue";
import apiService from "@/services/api";

export const useAuthStore = defineStore("auth", () => {
  const auth0 = useAuth0();

  const isAuthenticated = computed(() => auth0.isAuthenticated.value);
  const user = computed(() => auth0.user.value);
  const isLoading = computed(() => auth0.isLoading.value);

  async function logout() {
    apiService.clearAuthToken();
    await auth0.logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    });
  }

  async function getAccessToken() {
    try {
      const token = await auth0.getAccessTokenSilently();
      apiService.setAuthToken(token);
      return token;
    } catch (error) {
      console.error("Failed to get access token:", error);
      throw error;
    }
  }

  return {
    isAuthenticated,
    user,
    isLoading,
    logout,
    getAccessToken,
  };
});
