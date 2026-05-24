<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth0 } from "@auth0/auth0-vue";
import { useAuthStore } from "@/stores/auth";
import apiService from "@/services/api";

const router = useRouter();
const auth0 = useAuth0();
const authStore = useAuthStore();

const isLoading = ref(false);
const error = ref<string | null>(null);
const successMessage = ref<string | null>(null);

const form = ref({
  question: "",
  difficulty: "easy",
  choices: ["", "", "", ""],
  answer_letter: "A",
  explanation: "",
  date: new Date().toISOString().split("T")[0],
});

const difficultyOptions = ["easy", "medium", "hard"];
const answerLetters = ["A", "B", "C", "D", "E", "F"];

const updateChoice = (index: number, value: string) => {
  form.value.choices[index] = value;
};

const addChoice = () => {
  if (form.value.choices.length < 6) {
    form.value.choices.push("");
  }
};

const removeChoice = (index: number) => {
  if (form.value.choices.length > 2) {
    form.value.choices.splice(index, 1);
  }
};

const handleSubmit = async () => {
  error.value = null;
  successMessage.value = null;

  // Validation
  if (!form.value.question.trim()) {
    error.value = "Question text is required";
    return;
  }

  if (!form.value.explanation.trim()) {
    error.value = "Explanation is required";
    return;
  }

  const filledChoices = form.value.choices.filter((c) => c.trim());
  if (filledChoices.length < 2) {
    error.value = "At least 2 choices are required";
    return;
  }

  isLoading.value = true;

  try {
    const payload = {
      question: form.value.question,
      difficulty: form.value.difficulty,
      choices: filledChoices,
      answer_letter: form.value.answer_letter,
      explanation: form.value.explanation,
      date: form.value.date,
    };

    const result = await apiService.createQuestion(payload);

    successMessage.value = "Question created successfully!";

    // Reset form
    form.value = {
      question: "",
      difficulty: "easy",
      choices: ["", "", "", ""],
      answer_letter: "A",
      explanation: "",
      date: new Date().toISOString().split("T")[0],
    };

    // Redirect to home after 2 seconds
    setTimeout(() => {
      router.push("/home");
    }, 2000);
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : "Failed to create question";
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = async () => {
  await authStore.logout();
};

onMounted(async () => {
  if (auth0.isLoading.value) {
    return;
  }

  try {
    await authStore.getAccessToken();
  } catch (error) {
    console.error("Failed to get access token:", error);
  }
});
</script>

<template>
  <div class="create-question-page">
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
      <div class="form-container">
        <h2>Create a New Question</h2>

        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <form @submit.prevent="handleSubmit">
          <!-- Question Text -->
          <div class="form-group">
            <label for="question">Question *</label>
            <textarea
              id="question"
              v-model="form.question"
              placeholder="Enter your question here..."
              rows="3"
              required
            ></textarea>
          </div>

          <!-- Difficulty -->
          <div class="form-group">
            <label for="difficulty">Difficulty *</label>
            <select id="difficulty" v-model="form.difficulty" required>
              <option
                v-for="diff in difficultyOptions"
                :key="diff"
                :value="diff"
              >
                {{ diff.charAt(0).toUpperCase() + diff.slice(1) }}
              </option>
            </select>
          </div>

          <!-- Choices -->
          <div class="form-group">
            <label>Answer Choices *</label>
            <div class="choices-container">
              <div
                v-for="(choice, index) in form.choices"
                :key="index"
                class="choice-input-group"
              >
                <span class="choice-letter">{{
                  String.fromCharCode(65 + index)
                }}</span>
                <input
                  v-model="form.choices[index]"
                  type="text"
                  :placeholder="`Choice ${String.fromCharCode(65 + index)}`"
                  @input="updateChoice(index, $event.target.value)"
                />
                <button
                  v-if="form.choices.length > 2"
                  type="button"
                  @click="removeChoice(index)"
                  class="remove-choice-btn"
                >
                  ✕
                </button>
              </div>
            </div>
            <button
              v-if="form.choices.length < 6"
              type="button"
              @click="addChoice"
              class="add-choice-btn"
            >
              + Add Choice
            </button>
          </div>

          <!-- Correct Answer -->
          <div class="form-group">
            <label for="answer">Correct Answer *</label>
            <select id="answer" v-model="form.answer_letter" required>
              <option
                v-for="(letter, index) in answerLetters.slice(
                  0,
                  form.choices.length,
                )"
                :key="letter"
                :value="letter"
              >
                {{ letter }} - {{ form.choices[index] || "Empty" }}
              </option>
            </select>
          </div>

          <!-- Explanation -->
          <div class="form-group">
            <label for="explanation">Explanation *</label>
            <textarea
              id="explanation"
              v-model="form.explanation"
              placeholder="Explain why this is the correct answer..."
              rows="4"
              required
            ></textarea>
          </div>

          <!-- Date -->
          <div class="form-group">
            <label for="date">Date *</label>
            <input id="date" v-model="form.date" type="date" required />
          </div>

          <!-- Buttons -->
          <div class="form-actions">
            <button type="submit" :disabled="isLoading" class="submit-btn">
              {{ isLoading ? "Creating..." : "Create Question" }}
            </button>
            <button
              type="button"
              @click="router.push('/home')"
              class="cancel-btn"
              :disabled="isLoading"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<style scoped>
.create-question-page {
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
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.form-container {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.form-container h2 {
  margin-top: 0;
  color: #333;
  font-size: 24px;
  margin-bottom: 30px;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-left: 4px solid #c33;
}

.success-message {
  background-color: #efe;
  color: #3c3;
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-left: 4px solid #3c3;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="date"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input[type="text"]:focus,
.form-group input[type="date"]:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
}

.choices-container {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 4px;
  margin-bottom: 12px;
}

.choice-input-group {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.choice-input-group:last-child {
  margin-bottom: 0;
}

.choice-letter {
  font-weight: 600;
  color: #667eea;
  min-width: 24px;
  text-align: center;
}

.choice-input-group input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.choice-input-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.remove-choice-btn {
  padding: 6px 10px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.remove-choice-btn:hover {
  background-color: #ee5a5a;
}

.add-choice-btn {
  width: 100%;
  padding: 10px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.add-choice-btn:hover {
  background-color: #764ba2;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.submit-btn,
.cancel-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn {
  background-color: #667eea;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #764ba2;
  transform: scale(1.02);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #e0e0e0;
  color: #333;
}

.cancel-btn:hover:not(:disabled) {
  background-color: #d0d0d0;
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
