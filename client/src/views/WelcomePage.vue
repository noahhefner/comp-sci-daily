<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";

const { loginWithRedirect } = useAuth0();

const handleSignIn = async () => {
  await loginWithRedirect();
};
</script>

<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <h1>Welcome to Computer Scienc Daily!</h1>
      <p class="welcome-message">Sign in to get started.</p>
      <button class="sign-in-btn" @click="handleSignIn">Sign In</button>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.welcome-content {
  text-align: center;
  color: white;
  padding: 40px;
  max-width: 500px;
}

h1 {
  font-size: 48px;
  margin: 0 0 20px 0;
  font-weight: 700;
}

.welcome-message {
  font-size: 18px;
  margin: 0 0 40px 0;
  line-height: 1.6;
  opacity: 0.95;
}

.sign-in-btn {
  background-color: white;
  color: #667eea;
  border: none;
  padding: 12px 40px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.sign-in-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.sign-in-btn:active {
  transform: translateY(0);
}
</style>
