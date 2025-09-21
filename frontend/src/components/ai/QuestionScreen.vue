<template>
  <div class="question-screen">
    <div class="question-header">
      <div class="progress-container">
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
        <div class="progress-text">
          Question {{ questionNumber }} of {{ totalQuestions }}
        </div>
      </div>
    </div>

    <div class="question-content">
      <div class="question-bubble">
        <h2 class="question-text">{{ questionText }}</h2>
      </div>
    </div>

    <div class="answer-section">
      <h3 class="answer-prompt">Your Answer:</h3>
      <div class="answer-buttons">
        <button
          @click="submitAnswer('yes')"
          class="answer-button yes-button">
          <span class="button-text">Yes</span>
        </button>

        <button
          @click="submitAnswer('no')"
          class="answer-button no-button"
        >
          <span class="button-text">No</span>
        </button>

        <button
          @click="submitAnswer('dont_know')"
          class="answer-button maybe-button"
        >
          <span class="button-text">Don't Know</span>
        </button>
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
export default {
  name: 'QuestionScreen',
  props: {
    currentQuestion: {
      type: [String, Object],
      required: true
    },
    questionNumber: {
      type: Number,
      required: true
    },
    totalQuestions: {
      type: Number,
      default: 20
    }
  },
  emits: ['submitAnswer'],
  computed: {
    progressPercentage() {
      return (this.questionNumber / this.totalQuestions) * 100
    },
    questionText() {
      if (typeof this.currentQuestion === 'string') {
        return this.currentQuestion
      }
      return this.currentQuestion?.text || 'Loading question...'
    }
  },
  methods: {
    submitAnswer(answer) {
      this.$emit('submitAnswer', answer)
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
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-cartoon);
  font-weight: bold;
  min-width: 120px;
  color: black;
  border: 3px solid transparent;
}

.yes-button {
  background: var(--color-success);
}

.yes-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.no-button {
  background: var(--color-error);
}

.no-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.maybe-button {
  background: var(--color-warning);
}

.maybe-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
