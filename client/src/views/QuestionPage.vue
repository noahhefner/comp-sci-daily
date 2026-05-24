<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth0 } from "@auth0/auth0-vue";
import { useAuthStore } from "@/stores/auth";
import apiService, { type Question, type Answer } from "@/services/api";
import QuestionCard from "@/components/QuestionCard.vue";
import AnswerSection from "@/components/AnswerSection.vue";

const route = useRoute();
const router = useRouter();
const auth0 = useAuth0();
const authStore = useAuthStore();

// State
const currentQuestion = ref<Question | null>(null);
const currentAnswer = ref<Answer | null>(null);
const selectedChoice = ref<string | null>(null);
const isAnswerRevealed = ref(false);
const isLoading = ref(false);
const error = ref<string | null>(null);

// Computed
const questionId = computed(() => route.params.id as string);
const hasQuestion = computed(() => !!currentQuestion.value);
const isCorrect = computed(() => {
  if (!currentAnswer.value || !selectedChoice.value) return false;
  return selectedChoice.value === currentAnswer.value.answer;
});

// Methods
async function fetchQuestionById(id: string) {
  isLoading.value = true;
  error.value = null;
  selectedChoice.value = null;
  isAnswerRevealed.value = false;

  try {
    currentQuestion.value = await apiService.getQuestionById(id);
    currentAnswer.value = null;
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : "Failed to fetch question";
    currentQuestion.value = null;
  } finally {
    isLoading.value = false;
  }
}

async function revealAnswer() {
  if (!currentQuestion.value) return;

  isLoading.value = true;
  error.value = null;

  try {
    currentAnswer.value = await apiService.getAnswerByQuestionId(
      currentQuestion.value.id,
    );
    isAnswerRevealed.value = true;
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to fetch answer";
  } finally {
    isLoading.value = false;
  }
}

function selectChoice(letter: string) {
  if (!isAnswerRevealed.value) {
    selectedChoice.value = letter;
  }
}

async function handleLogout() {
  await authStore.logout();
}

function goHome() {
  currentQuestion.value = null;
  currentAnswer.value = null;
  selectedChoice.value = null;
  isAnswerRevealed.value = false;
  router.push({ name: "home" });
}

function handleTryNext() {
  currentQuestion.value = null;
  currentAnswer.value = null;
  selectedChoice.value = null;
  isAnswerRevealed.value = false;
  goHome();
}

// Lifecycle
onMounted(async () => {
  if (auth0.isLoading.value) {
    return;
  }

  try {
    await authStore.getAccessToken();
  } catch (error) {
    console.error("Failed to get access token:", error);
  }

  if (questionId.value) {
    await fetchQuestionById(questionId.value);
  }
});
</script>

<template>
  <div class="question-page">
    <header class="header">
      <div class="header-content">
        <button @click="goHome" class="back-btn">← Home</button>
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
      <div v-if="isLoading && !hasQuestion" class="loading">
        <p>Loading question...</p>
      </div>

      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="fetchQuestionById(questionId)" class="retry-btn">
          Retry
        </button>
      </div>

      <template v-else-if="hasQuestion">
        <QuestionCard
          :question="currentQuestion"
          :selected-choice="selectedChoice"
          :is-answer-revealed="isAnswerRevealed"
          :current-answer="currentAnswer"
          :is-correct="isCorrect"
          @select-choice="selectChoice"
        />
        <AnswerSection
          :is-answer-revealed="isAnswerRevealed"
          :current-answer="currentAnswer"
          :is-correct="isCorrect"
          :has-selected="!!selectedChoice"
          :is-loading="isLoading"
          @reveal-answer="revealAnswer"
          @try-next="handleTryNext"
        />
      </template>
    </main>
  </div>
</template>

<style scoped>
.question-page {
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
  gap: 20px;
}

.back-btn {
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.back-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.header h1 {
  margin: 0;
  font-size: 28px;
  flex: 1;
  text-align: center;
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
  white-space: nowrap;
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
