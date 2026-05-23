<script setup lang="ts">
import { computed } from "vue";
import { useTriviaStore } from "@/stores/trivia";

const triviaStore = useTriviaStore();

const isAnswerRevealed = computed(() => triviaStore.isAnswerRevealed);
const currentAnswer = computed(() => triviaStore.currentAnswer);
const isCorrect = computed(() => triviaStore.isCorrect);
const hasSelected = computed(() => !!triviaStore.selectedChoice);

const handleRevealAnswer = async () => {
  if (hasSelected.value && !isAnswerRevealed.value) {
    await triviaStore.revealAnswer();
  }
};

const handleTryNext = () => {
  triviaStore.reset();
  triviaStore.fetchTodayQuestion();
};
</script>

<template>
  <div class="answer-section">
    <div v-if="!isAnswerRevealed" class="controls">
      <button
        @click="handleRevealAnswer"
        :disabled="!hasSelected"
        class="reveal-btn"
      >
        {{ hasSelected ? "Reveal Answer" : "Select an option first" }}
      </button>
    </div>

    <div v-else class="answer-display">
      <div :class="['result', isCorrect ? 'correct' : 'incorrect']">
        <h3>{{ isCorrect ? "✓ Correct!" : "✗ Incorrect" }}</h3>
      </div>

      <div v-if="currentAnswer" class="answer-content">
        <div class="answer-header">
          <h4>
            The answer is: <strong>{{ currentAnswer.answer }}</strong>
          </h4>
        </div>

        <div class="explanation">
          <h4>Explanation:</h4>
          <p>{{ currentAnswer.explanation }}</p>
        </div>

        <button @click="handleTryNext" class="next-btn">
          Try Next Question
        </button>
      </div>

      <div v-else-if="triviaStore.isLoading" class="loading">
        <p>Loading answer...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.answer-section {
  background-color: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.controls {
  display: flex;
  justify-content: center;
}

.reveal-btn {
  padding: 12px 32px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reveal-btn:hover:not(:disabled) {
  background-color: #764ba2;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.reveal-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.answer-display {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result {
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.result.correct {
  background-color: #d4edda;
  border: 2px solid #28a745;
  color: #155724;
}

.result.incorrect {
  background-color: #f8d7da;
  border: 2px solid #dc3545;
  color: #721c24;
}

.result h3 {
  margin: 0;
  font-size: 24px;
}

.answer-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.answer-header {
  padding: 15px;
  background-color: #f0f5ff;
  border-left: 4px solid #667eea;
  border-radius: 4px;
}

.answer-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.answer-header strong {
  color: #667eea;
  font-size: 18px;
}

.explanation {
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.explanation h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.explanation p {
  margin: 0;
  color: #666;
  line-height: 1.6;
  font-size: 15px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #667eea;
  font-size: 16px;
}

.next-btn {
  padding: 12px 32px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: center;
}

.next-btn:hover {
  background-color: #764ba2;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
