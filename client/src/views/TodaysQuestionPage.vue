<script setup lang="ts">
import { watchEffect, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthenticatedUser } from "../composables/useAuthenticatedUser";
import { useAuth0 } from "@auth0/auth0-vue";

const { user, accessToken } = useAuthenticatedUser();

const auth0 = useAuth0();
const router = useRouter();

const question = ref<any>(null);
const isQuestionLoading = ref(true);

const answer = ref<any>(null);
const isAnswerLoading = ref(false);

const error = ref<string | null>(null);

const selectedChoice = ref<string | null>(null);

const hasSubmitted = ref(false);
const isCorrect = ref<boolean | null>(null);

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
    question.value = await response.json();
  } catch (err) {
    console.error("API request failed:", err);
    error.value = err instanceof Error ? err.message : "An unknown error occurred";
  } finally {
    isQuestionLoading.value = false;
  }
};

const getTodaysAnswer = async () => {
  if (!accessToken.value) {
    error.value = "No access token available.";
    return;
  }

  try {
    isAnswerLoading.value = true;
    const baseURL: string = import.meta.env.VITE_API_URL;
    const response = await fetch(`${baseURL}/answers/${question.value.id}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken.value}`,
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    answer.value = await response.json();
  } catch (err) {
    console.error("API request failed:", err);
    error.value = err instanceof Error ? err.message : "An unknown error occurred";
  } finally {
    isAnswerLoading.value = false;
  }
};

const handleChoiceSelect = (letter: string) => {
  if (hasSubmitted.value) return;

  if (selectedChoice.value === letter) {
    selectedChoice.value = null;
    return;
  }
  selectedChoice.value = letter;
};

const handleSubmit = async () => {
  if (!selectedChoice.value) return;

  await getTodaysAnswer();

  if (answer.value) {
    console.log(selectedChoice.value);
    console.log(answer.value.correct_choice);
    isCorrect.value = selectedChoice.value === answer.value.answer;
    hasSubmitted.value = true;
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
            <button
    @click="router.push('/create')"
    class="create-btn"
  >
    Create Question
  </button>
          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div v-if="error" class="error-message">
        <p>Error: {{ error }}</p>
      </div>

      <div v-else-if="isQuestionLoading" class="loading">
        <div class="spinner"></div>
        <p>Loading today's question...</p>
      </div>

      <template v-else-if="question !== null">
        <div class="question-card">
          <div class="question-header">
            <span :class="['difficulty', question.difficulty?.toLowerCase()]">
              {{ question.difficulty || "Trivia" }}
            </span>
            <span class="date">
              {{
                question.date
                  ? new Date(question.date).toLocaleDateString()
                  : "Today"
              }}
            </span>
          </div>

          <h2 class="question-text">{{ question.question }}</h2>

<div class="choices">
  <button
    v-for="(choice, index) in question.choices"
    :key="choice.id || index"
    @click="handleChoiceSelect(String.fromCharCode(65 + index))"
    :class="[
      'choice-btn',
      {
        selected:
          selectedChoice === String.fromCharCode(65 + index),

        correct:
          hasSubmitted &&
          String.fromCharCode(65 + index) ===
            answer?.correct_choice,

        incorrect:
          hasSubmitted &&
          selectedChoice ===
            String.fromCharCode(65 + index) &&
          selectedChoice !== answer?.correct_choice
      }
    ]"
  >
    <span class="letter">
      {{ String.fromCharCode(65 + index) }}
    </span>

    <span class="text">
      {{
        typeof choice === "string"
          ? choice
          : choice.choice_text
      }}
    </span>
  </button>
</div>

          <div class="question-footer">
            <button 
              class="submit-btn" 
              :disabled="selectedChoice === null || hasSubmitted"
              @click="handleSubmit"
            >
              Submit
            </button>
          </div>

          <div v-if="hasSubmitted" class="answer-feedback">
            <p v-if="isCorrect" class="correct-text">
              ✅ Correct!
            </p>
            <p v-else class="incorrect-text">
              ❌ Incorrect. The correct answer is {{ answer?.correct_choice }}.
            </p>

            <p v-if="answer?.explanation" class="explanation">
              {{ answer.explanation }}
            </p>
          </div>
        </div>
      </template>
    </main>
  </div>
</template><style scoped>
.home-page {
  min-height: 100vh;
  background-color: var(--bg-slate);
  color: var(--text-main);
  font-family:
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    sans-serif;
}

/* Header Styles */
.header {
  background-color: var(--primary-dark);
  color: #ffffff;
  padding: 16px 0;
  box-shadow: 0 4px 12px rgba(30, 70, 32, 0.15);
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  font-size: 14px;
  opacity: 0.9;
  font-weight: 500;
}

/* Buttons */
.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: var(--primary-dark);
  color: #ffffff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}

.submit-btn:hover {
  background-color: var(--accent-hover);
  transform: translateY(-1px);
}

.submit-btn:disabled {
  color: var(--accent);
  background-color: var(--primary-light);
  cursor: not-allowed;
}

.logout-btn {
  padding: 8px 16px;
  background-color: transparent;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}

/* Main Content Wrapper */
.main-content {
  max-width: 720px;
  margin: 40px auto;
  padding: 0 24px;
}

/* Question Card Structure */
.question-card {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 32px;
  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.question-footer {
  margin-top: 24px;
}

/* Badges */
.difficulty {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background-color: #e2e8f0;
  color: #4a5568;
}

.difficulty.easy {
  background-color: #e8f5e9;
  color: var(--success);
}
.difficulty.medium {
  background-color: #fff3e0;
  color: var(--warning);
}
.difficulty.hard {
  background-color: #ffebee;
  color: var(--error);
}

.date {
  color: #718096;
  font-size: 13px;
  font-weight: 500;
}

.question-text {
  font-size: 22px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 28px 0;
  line-height: 1.5;
}

/* Choice Buttons Block */
.choices {
  display: grid;
  gap: 14px;
}

.choice-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background-color: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  font-size: 15px;
  color: var(--text-main);
  font-weight: 500;
}

.choice-btn:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

/* Selected State */
.choice-btn.selected {
  background-color: var(--primary-light);
  border-color: var(--primary);
}

.letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background-color: #edf2f7;
  color: #4a5568;
  border-radius: 6px;
  font-weight: 700;
  flex-shrink: 0;
  font-size: 13px;
  transition: all 0.2s ease;
}

.choice-btn.selected .letter {
  background-color: var(--primary);
  color: #ffffff;
}

.text {
  line-height: 1.4;
}

/* Loading State UI */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.loading p {
  font-size: 15px;
  color: #4a5568;
  margin: 16px 0 0 0;
  font-weight: 500;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #edf2f7;
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Error UI */
.error-message {
  background-color: #ffebee;
  border: 1px solid #ffcdd2;
  padding: 16px;
  border-radius: 10px;
  text-align: center;
  color: var(--error);
  font-weight: 500;
}
</style>
