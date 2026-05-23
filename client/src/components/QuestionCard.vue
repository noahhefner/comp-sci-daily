<script setup lang="ts">
import { computed } from "vue";
import { useTriviaStore } from "@/stores/trivia";

const triviaStore = useTriviaStore();

const question = computed(() => triviaStore.currentQuestion);
const selectedChoice = computed(() => triviaStore.selectedChoice);

const handleChoiceSelect = (letter: string) => {
  if (!triviaStore.isAnswerRevealed) {
    triviaStore.selectChoice(letter);
  }
};
</script>

<template>
  <div v-if="question" class="question-card">
    <div class="question-header">
      <span class="difficulty" :class="question.difficulty?.toLowerCase()">
        {{ question.difficulty }}
      </span>
      <span class="date">{{
        new Date(question.date).toLocaleDateString()
      }}</span>
    </div>

    <h2 class="question-text">{{ question.question }}</h2>

    <div class="choices">
      <button
        v-for="choice in question.choices"
        :key="choice.letter"
        @click="handleChoiceSelect(choice.letter)"
        :class="[
          'choice-btn',
          { selected: selectedChoice === choice.letter },
          { disabled: triviaStore.isAnswerRevealed },
          {
            correct:
              triviaStore.isAnswerRevealed &&
              triviaStore.isCorrect &&
              selectedChoice === choice.letter,
          },
          {
            incorrect:
              triviaStore.isAnswerRevealed &&
              !triviaStore.isCorrect &&
              selectedChoice === choice.letter,
          },
          {
            answer:
              triviaStore.isAnswerRevealed &&
              triviaStore.currentAnswer?.answer === choice.letter,
          },
        ]"
      >
        <span class="letter">{{ choice.letter }}</span>
        <span class="text">{{ choice.text }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.question-card {
  background-color: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.difficulty {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.difficulty.easy {
  background-color: #d4edda;
  color: #155724;
}

.difficulty.medium {
  background-color: #fff3cd;
  color: #856404;
}

.difficulty.hard {
  background-color: #f8d7da;
  color: #721c24;
}

.date {
  color: #999;
  font-size: 14px;
}

.question-text {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 30px 0;
  line-height: 1.4;
}

.choices {
  display: grid;
  gap: 12px;
}

.choice-btn {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 16px;
  background-color: #f9f9f9;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  font-size: 16px;
}

.choice-btn:hover:not(.disabled) {
  background-color: #f0f5ff;
  border-color: #667eea;
}

.choice-btn.selected {
  background-color: #f0f5ff;
  border-color: #667eea;
  border-width: 2px;
}

.choice-btn.disabled {
  cursor: not-allowed;
  opacity: 0.8;
}

.choice-btn.correct {
  background-color: #d4edda;
  border-color: #28a745;
}

.choice-btn.incorrect {
  background-color: #f8d7da;
  border-color: #dc3545;
}

.choice-btn.answer {
  background-color: #cfe2ff;
  border-color: #0d6efd;
}

.letter {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: #667eea;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  flex-shrink: 0;
  font-size: 14px;
}

.choice-btn.correct .letter {
  background-color: #28a745;
}

.choice-btn.incorrect .letter {
  background-color: #dc3545;
}

.choice-btn.answer .letter {
  background-color: #0d6efd;
}

.text {
  display: flex;
  align-items: center;
}
</style>
