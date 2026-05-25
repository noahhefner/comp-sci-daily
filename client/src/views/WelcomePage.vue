<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";

const { loginWithRedirect } = useAuth0();

const handleSignIn = async () => {
  await loginWithRedirect({
    appState: {
      target: "/today",
    },
  });
};
</script>

<template>
  <div class="welcome-container">
    <div class="welcome-card">
      <div class="logo-icon">
        <span></span>
      </div>

      <h1>Welcome to Computer Science Daily</h1>
      <p class="welcome-message">
        Challenge yourself every day with curated trivia questions and track
        your learning progress.
      </p>

      <button class="sign-in-btn" @click="handleSignIn">
        Sign In to Get Started
      </button>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--bg-slate);
  padding: 24px;
}

.welcome-card {
  background-color: #ffffff;
  text-align: center;
  padding: 48px 40px;
  max-width: 480px;
  width: 100%;
  border-radius: 16px;
  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* Accent logo geometric element */
.logo-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 56px;
  height: 56px;
  background-color: var(--primary-light);
  border-radius: 12px;
  margin: 0 auto 24px auto;
}

.logo-icon span {
  width: 20px;
  height: 20px;
  border: 3px solid var(--primary);
  border-radius: 4px;
  transform: rotate(45deg);
}

h1 {
  color: var(--text-main);
  font-size: 28px;
  margin: 0 0 14px 0;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1.3;
}

.welcome-message {
  color: #718096;
  font-size: 15px;
  margin: 0 0 32px 0;
  line-height: 1.6;
  font-weight: 400;
}

.sign-in-btn {
  width: 100%;
  background-color: var(--accent);
  color: #ffffff;
  border: none;
  padding: 14px 28px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(82, 183, 136, 0.2);
}

.sign-in-btn:hover {
  background-color: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(82, 183, 136, 0.3);
}

.sign-in-btn:active {
  transform: translateY(0);
}
</style>
