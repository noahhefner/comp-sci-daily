<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
import { useAuthStore } from "@/stores/auth";

const { isLoading } = useAuth0();
const authStore = useAuthStore();
</script>

<template>
  <div id="app">
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading...</p>
    </div>
    <router-view v-else />
  </div>
</template>

<style>
:root {
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #28a745;
  --error: #dc3545;
  --warning: #ffc107;
  --info: #17a2b8;
  --light: #f8f9fa;
  --dark: #343a40;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu,
    Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  display: flex;
  flex-direction: column;
}

.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

button {
  font-family: inherit;
}
</style>
