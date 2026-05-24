<script setup lang="ts">
import { watchEffect, ref } from "vue";
import { useRouter } from "vue-router";
import QuestionCard from "@/components/QuestionCard.vue";
import AnswerSection from "@/components/AnswerSection.vue";
import { useAuthenticatedUser } from "../composables/useAuthenticatedUser";
import { useAuth0 } from "@auth0/auth0-vue";

const { user, accessToken, isLoading } = useAuthenticatedUser();

const auth0 = useAuth0();
const router = useRouter();
const apiResponse = ref(null);
const isQuestionLoading = ref(true);
const error = ref<string | null>(null);

const getTodaysQuestion = async () => {
  if (!accessToken.value) {
    error.value = "No access token available.";
    return;
  }

  try {
    isQuestionLoading.value = true;
    const baseURL: string = import.meta.env.VITE_API_URL;
    const response = await fetch(`${baseURL}/questions/today`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken.value}`,
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    apiResponse.value = await response.json();
  } catch (err) {
    console.error("API request failed:", err);
    // Handle type-unsafe catch blocks cleanly
    if (err instanceof Error) {
      error.value = err.message;
    } else {
      error.value = "An unknown error occurred";
    }
  } finally {
    isQuestionLoading.value = false;
  }
};

const handleLogout = async () => {
  await auth0.logout({
    logoutParams: {
      returnTo: window.location.origin,
    },
  });
};

watchEffect(() => {
  if (accessToken.value) {
    getTodaysQuestion();
  }
});
</script>

<template>
  <div class="home-page">
    <header class="header">
      <div class="header-content">
        <h1>Computer Science Daily Trivia</h1>
        <div class="user-info">
          <span v-if="user" class="user-name">{{ user.name }}</span>
          <button @click="router.push('/create')" class="create-btn">
            Create Question
          </button>
          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div v-if="isQuestionLoading" class="loading">
        <p>Loading today's question...</p>
      </div>

      <template v-else-if="apiResponse !== null">
        <QuestionCard />
        <AnswerSection />
      </template>
    </main>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  background-color: rgba(0, 0, 0, 0.2);
  color: white;
  padding: 20px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  font-size: 28px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-name {
  font-size: 16px;
}

.logout-btn {
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.create-btn {
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.9);
  color: #667eea;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.create-btn:hover {
  background-color: white;
  transform: scale(1.05);
}

.main-content {
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px;
}

.loading,
.error {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.loading p {
  font-size: 18px;
  color: #667eea;
  margin: 0;
}

.error {
  background-color: #fee;
}

.error p {
  color: #c33;
  margin: 0 0 20px 0;
  font-size: 16px;
}

.retry-btn {
  padding: 10px 20px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.retry-btn:hover {
  background-color: #764ba2;
}
</style>
