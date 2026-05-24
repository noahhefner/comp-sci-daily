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
      <p>Loading application...</p>
    </div>
    <router-view v-else />
  </div>
</template>

<style>
/* Global CSS Variables - Forest Green Palette */
:root {
  --primary: #2d6a4f; /* Forest Green Primary */
  --primary-dark: #1e4620; /* Dark Forest Green for Headers */
  --primary-light: #d8f3dc; /* Soft Forest Tint for Selections */
  --accent: #52b788; /* Mint Accent for Primary Actions */
  --accent-hover: #74c69d; /* Lighter Mint Hover State */

  --success: #2e7d32;
  --error: #c62828;
  --warning: #ef6c00;
  --info: #17a2b8;

  --bg-slate: #f4f6f5; /* Main background color */
  --text-main: #2d3748; /* Charcoal dark text */
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
  background-color: var(--bg-slate);
  color: var(--text-main);
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

/* Updated Global Loading Container */
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: var(--bg-slate);
  color: #4a5568;
  font-size: 16px;
  font-weight: 500;
}

/* Updated Spinner matching the new theme */
.spinner {
  width: 44px;
  height: 44px;
  border: 3.5px solid #edf2f7;
  border-top: 3.5px solid var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
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
