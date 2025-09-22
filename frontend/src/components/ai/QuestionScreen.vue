<template>
  <div class="question-screen">
    <div class="question-header">
      <h2 class="question-title">Think of an Australian Animal</h2>
      <p class="question-subtitle">Answer the questions to help me guess!</p>
      <div class="progress">Question {{ questionNumber || 1 }}</div>
    </div>

    <div class="question-content">
      <div class="question-box">
        <h3 class="question-text">{{ currentQuestion?.text || 'Loading question...' }}</h3>
      </div>

      <div class="answer-options">
        <Button
          class="answer-button yes-button"
          @click="submitAnswer('yes')"
          :disabled="!currentQuestion || isSubmitting"
          type="primary"
          size="medium"
        >
          Yes
        </Button>
        <Button
          class="answer-button no-button"
          @click="submitAnswer('no')"
          :disabled="!currentQuestion || isSubmitting"
          type="secondary"
          size="medium"
        >
          No
        </Button>
        <Button
          class="answer-button dont-know-button"
          @click="submitAnswer('dont_know')"
          :disabled="!currentQuestion || isSubmitting"
          type="secondary"
          size="large"
        >
          Don't Know
        </Button>
      </div>
    </div>

    <div class="thinking-indicator">
      <div class="thinking-dots">
        <span class="thinking-text">AI is thinking</span>
        <div class="dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'QuestionScreen',
  components: {
    Button
  },
  props: {
    currentQuestion: {
      type: [String, Object],
      default: null
    },
    questionNumber: {
      type: Number,
      default: 1
    },
    totalQuestions: {
      type: Number,
      default: 10
    }
  },
  emits: ['submitAnswer'],
  data() {
    return {
      isSubmitting: false,
      lastSubmittedQuestion: null
    }
  },
  methods: {
    submitAnswer(answer) {
      if (this.isSubmitting || !this.currentQuestion) {
        return
      }

      if (this.lastSubmittedQuestion === this.currentQuestion?.id) {
        return
      }

      this.isSubmitting = true
      this.lastSubmittedQuestion = this.currentQuestion?.id
      this.$emit('submitAnswer', answer)

      setTimeout(() => {
        this.isSubmitting = false
      }, 1000)
    }
  },
  watch: {
    currentQuestion(newQuestion) {
      if (newQuestion && newQuestion.id !== this.lastSubmittedQuestion) {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
.question-screen {
  padding: var(--spacing-xl);
  text-align: center;
}

.question-header {
  margin-bottom: var(--spacing-xl);
}

.progress-container {
  max-width: 400px;
  margin: 0 auto;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: var(--border-radius-sm);
  overflow: hidden;
  margin-bottom: var(--spacing-sm);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  transition: width 0.3s ease;
  border-radius: var(--border-radius-sm);
}

.progress-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
}

.question-content {
  margin-bottom: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
}

.ai-avatar {
  font-size: 3rem;
  animation: bounce 2s infinite;
}

.question-bubble {
  background: white;
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-xl);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 3px solid var(--color-primary);
  position: relative;
  max-width: 500px;
}

.question-bubble::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  border-bottom: 15px solid var(--color-primary);
}

.question-text {
  font-size: var(--font-size-xl);
  color: var(--color-text);
  margin: 0;
  font-family: var(--font-cartoon);
  line-height: 1.4;
}

.answer-section {
  margin-bottom: var(--spacing-xl);
}

.answer-prompt {
  font-size: var(--font-size-lg);
  color: var(--color-text);
  margin-bottom: var(--spacing-lg);
  font-family: var(--font-cartoon);
}

.answer-options {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: center;
  align-items: center;
}

.answer-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.answer-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-cartoon);
  font-weight: bold;
  min-width: 60px;
  color: white;
  font-size: var(--font-size-sm);
  text-align: center;
}

.yes-button {
  background: #4CAF50;
}

.yes-button:hover {
  background: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.no-button {
  background: #f44336;
}

.no-button:hover {
  background: #da190b;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.dont-know-button {
  background: #ff9800;
}

.dont-know-button:hover {
  background: #e68900;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.button-icon {
  font-size: var(--font-size-xl);
}

.button-text {
  font-size: var(--font-size-md);
}

.thinking-indicator {
  opacity: 0.7;
}

.thinking-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.thinking-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.dots {
  display: flex;
  gap: 4px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-text-secondary);
  animation: pulse 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -8px, 0);
  }
  70% {
    transform: translate3d(0, -4px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
}

@keyframes pulse {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .question-screen {
    padding: var(--spacing-lg);
  }

  .answer-buttons {
    flex-direction: column;
    max-width: 200px;
    margin: 0 auto;
  }

  .answer-button {
    min-width: auto;
    width: 100%;
  }

  .question-text {
    font-size: var(--font-size-lg);
  }
}
</style>
