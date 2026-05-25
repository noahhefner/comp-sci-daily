<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth0 } from "@auth0/auth0-vue";
import { useAuthenticatedUser } from "../composables/useAuthenticatedUser";

const { user, accessToken } = useAuthenticatedUser();

const auth0 = useAuth0();
const router = useRouter();

const question = ref("");
const date = ref(new Date().toISOString().split("T")[0]);

const choices = ref<string[]>(["", ""]);
const answerIndex = ref<number | null>(null);

const explanation = ref("");

const isSubmitting = ref(false);

const successMessage = ref<string | null>(null);
const error = ref<string | null>(null);

const addChoice = () => {
  choices.value.push("");
};

const removeChoice = (index: number) => {
  if (choices.value.length <= 2) return;

  choices.value.splice(index, 1);

  if (answerIndex.value === index) {
    answerIndex.value = null;
  } else if (answerIndex.value !== null && answerIndex.value > index) {
    answerIndex.value--;
  }
};

const handleSubmit = async () => {
  error.value = null;
  successMessage.value = null;

  if (!accessToken.value) {
    error.value = "No access token available.";
    return;
  }

  if (answerIndex.value === null) {
    error.value = "Please select the correct answer.";
    return;
  }

  try {
    isSubmitting.value = true;

    const baseURL: string = import.meta.env.VITE_API_URL;

    const response = await fetch(`${baseURL}/questions/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken.value}`,
      },
      body: JSON.stringify({
        question: question.value,
        date: date.value,
        choices: choices.value,
        answer_index: answerIndex.value,
        explanation: explanation.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to create question.");
    }

    successMessage.value = "Question created successfully.";

    question.value = "";
    choices.value = ["", ""];
    answerIndex.value = null;
    explanation.value = "";
  } catch (err) {
    console.error(err);

    error.value =
      err instanceof Error ? err.message : "An unknown error occurred";
  } finally {
    isSubmitting.value = false;
  }
};

const handleLogout = async () => {
  await auth0.logout({
    logoutParams: {
      returnTo: window.location.origin,
    },
  });
};
</script>

<template>
  <div class="home-page">
    <header class="header">
      <div class="header-content">
        <h1>Create Trivia Question</h1>

        <div class="user-info">
          <span v-if="user" class="user-name">
            {{ user.name }}
          </span>

          <button @click="handleLogout" class="logout-btn">Logout</button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div class="question-card">
        <div class="form-group">
          <label>Question</label>

          <textarea
            v-model="question"
            class="input textarea"
            placeholder="Enter question..."
          />
        </div>

        <div class="form-group">
          <label>Date</label>

          <input v-model="date" type="date" class="input" />
        </div>

        <div class="form-group">
          <div class="choices-header">
            <label>Choices</label>

            <button type="button" class="add-choice-btn" @click="addChoice">
              + Add Choice
            </button>
          </div>

          <div class="choices-list">
            <div
              v-for="(choice, index) in choices"
              :key="index"
              class="choice-row"
            >
              <button
                type="button"
                :class="[
                  'answer-select-btn',
                  {
                    selected: answerIndex === index,
                  },
                ]"
                @click="answerIndex = index"
              >
                {{ String.fromCharCode(65 + index) }}
              </button>

              <input
                v-model="choices[index]"
                type="text"
                class="input"
                :placeholder="`Choice ${String.fromCharCode(65 + index)}`"
              />

              <button
                type="button"
                class="remove-btn"
                @click="removeChoice(index)"
                :disabled="choices.length <= 2"
              >
                ✕
              </button>
            </div>
          </div>

          <p class="helper-text">
            Click a letter button to mark the correct answer.
          </p>
        </div>

        <div class="form-group">
          <label>Explanation</label>

          <textarea
            v-model="explanation"
            class="input textarea"
            placeholder="Explain why the answer is correct..."
          />
        </div>

        <button
          class="submit-btn"
          :disabled="isSubmitting"
          @click="handleSubmit"
        >
          {{ isSubmitting ? "Creating Question..." : "Create Question" }}
        </button>
      </div>
    </main>
  </div>
</template>

<style scoped>
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

/* Header */

.header {
  background-color: var(--primary-dark);
  color: white;
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
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-name {
  font-size: 14px;
  opacity: 0.9;
}

/* Main */

.main-content {
  max-width: 720px;
  margin: 40px auto;
  padding: 0 24px;
}

/* Card */

.question-card {
  background: white;
  border-radius: 16px;
  padding: 32px;

  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.02);
}

/* Form */

.form-group {
  margin-bottom: 28px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;

  font-weight: 600;
  color: #2d3748;
}

.input {
  width: 100%;
  padding: 14px;

  border: 1.5px solid #e2e8f0;
  border-radius: 10px;

  font-size: 15px;

  transition: all 0.2s ease;
  box-sizing: border-box;
}

.input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
}

.textarea {
  min-height: 120px;
  resize: vertical;
}

/* Choices */

.choices-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 14px;
}

.choices-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.choice-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.answer-select-btn {
  width: 42px;
  height: 42px;

  border: none;
  border-radius: 10px;

  cursor: pointer;

  background: #edf2f7;
  color: #4a5568;

  font-weight: 700;

  transition: all 0.2s ease;

  flex-shrink: 0;
}

.answer-select-btn.selected {
  background: var(--primary);
  color: white;
}

.answer-select-btn:hover {
  transform: translateY(-1px);
}

.add-choice-btn {
  border: none;
  background: transparent;

  color: var(--primary);
  font-weight: 600;

  cursor: pointer;
}

.remove-btn {
  width: 40px;
  height: 40px;

  border: none;
  border-radius: 8px;

  background: #fed7d7;
  color: #c53030;

  cursor: pointer;
  flex-shrink: 0;
}

.remove-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.helper-text {
  margin-top: 10px;

  font-size: 13px;
  color: #718096;
}

/* Buttons */

.submit-btn {
  width: 100%;
  padding: 16px;

  border: none;
  border-radius: 10px;

  background-color: var(--primary-dark);
  color: white;

  cursor: pointer;

  font-weight: 600;
  font-size: 15px;

  transition: all 0.2s ease;
}

.submit-btn:hover {
  background-color: var(--accent-hover);
  transform: translateY(-1px);
}

.submit-btn:disabled {
  background-color: var(--primary-light);
  cursor: not-allowed;
}

.logout-btn {
  padding: 8px 16px;

  background-color: transparent;
  color: white;

  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;

  cursor: pointer;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Messages */

.error-message {
  background-color: #ffebee;
  border: 1px solid #ffcdd2;

  padding: 16px;
  margin-bottom: 20px;

  border-radius: 10px;

  color: var(--error);
  font-weight: 500;
}

.success-message {
  background-color: #e8f5e9;
  border: 1px solid #c8e6c9;

  padding: 16px;
  margin-bottom: 20px;

  border-radius: 10px;

  color: #2e7d32;
  font-weight: 500;
}
</style>
