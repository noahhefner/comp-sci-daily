<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useTriviaStore } from "@/stores/trivia";
import { useAuthStore } from "@/stores/auth";
import QuestionCard from "@/components/QuestionCard.vue";
import AnswerSection from "@/components/AnswerSection.vue";

const triviaStore = useTriviaStore();
const authStore = useAuthStore();

const hasQuestion = computed(() => !!triviaStore.currentQuestion);

onMounted(async () => {
  if (!hasQuestion.value) {
    await triviaStore.fetchTodayQuestion();
  }
});

const handleLogout = async () => {
  await authStore.logout();
};
</script>

<template>
  <div class="home-page">
    <header class="header">
      <div class="header-content">
        <h1>Computer Science Daily Trivia</h1>
        <div class="user-info">
          <span v-if="authStore.user" class="user-name">{{
            authStore.user.name
          }}</span>
          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div v-if="triviaStore.isLoading && !hasQuestion" class="loading">
        <p>Loading today's question...</p>
      </div>

      <div v-else-if="triviaStore.error" class="error">
        <p>{{ triviaStore.error }}</p>
        <button @click="triviaStore.fetchTodayQuestion()" class="retry-btn">
          Retry
        </button>
      </div>

      <template v-else-if="hasQuestion">
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
