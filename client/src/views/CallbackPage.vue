<script setup lang="ts">
import { onMounted } from "vue";
import { useAuth0 } from "@auth0/auth0-vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const { isLoading, error } = useAuth0();
const router = useRouter();
const authStore = useAuthStore();

onMounted(async () => {
  // Wait for Auth0 to finish processing the callback
  if (!isLoading.value) {
    // Get access token
    try {
      await authStore.getAccessToken();
      // Redirect to home page
      router.push({ name: "home" });
    } catch (err) {
      console.error("Error in callback:", err);
      router.push({ name: "home" });
    }
  }
});
</script>

<template>
  <div class="callback-page">
    <div class="loading-container">
      <h1>Loading...</h1>
      <p>Processing authentication...</p>
      <div v-if="error" class="error">
        <p>{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.callback-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.loading-container {
  text-align: center;
  color: white;
}

.loading-container h1 {
  font-size: 32px;
  margin-bottom: 10px;
}

.loading-container p {
  font-size: 18px;
  margin-bottom: 20px;
}

.error {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
}

.error p {
  color: #ffcccc;
  margin: 0;
}
</style>
