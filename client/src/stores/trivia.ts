import { ref, computed } from "vue";
import { defineStore } from "pinia";
import apiService, { type Question, type Answer } from "@/services/api";

export const useTriviaStore = defineStore("trivia", () => {
  const currentQuestion = ref<Question | null>(null);
  const currentAnswer = ref<Answer | null>(null);
  const selectedChoice = ref<string | null>(null);
  const isAnswerRevealed = ref(false);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const isCorrect = computed(() => {
    if (!currentAnswer.value || !selectedChoice.value) return false;
    return selectedChoice.value === currentAnswer.value.answer;
  });

  async function fetchTodayQuestion() {
    isLoading.value = true;
    error.value = null;
    selectedChoice.value = null;
    isAnswerRevealed.value = false;

    try {
      currentQuestion.value = await apiService.getTodayQuestion();
      currentAnswer.value = null;
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : "Failed to fetch question";
      currentQuestion.value = null;
    } finally {
      isLoading.value = false;
    }
  }

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
      error.value =
        err instanceof Error ? err.message : "Failed to fetch answer";
    } finally {
      isLoading.value = false;
    }
  }

  function selectChoice(letter: string) {
    selectedChoice.value = letter;
  }

  function reset() {
    currentQuestion.value = null;
    currentAnswer.value = null;
    selectedChoice.value = null;
    isAnswerRevealed.value = false;
    error.value = null;
  }

  return {
    currentQuestion,
    currentAnswer,
    selectedChoice,
    isAnswerRevealed,
    isLoading,
    error,
    isCorrect,
    fetchTodayQuestion,
    fetchQuestionById,
    revealAnswer,
    selectChoice,
    reset,
  };
});
