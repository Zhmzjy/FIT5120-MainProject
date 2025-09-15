<template>
  <div class="result-screen">
    <div class="result-header">
      <div class="ai-avatar">🤖</div>
      <h2 class="result-title">AI's Guess</h2>
    </div>

    <div class="animal-result">
      <div class="animal-card">
        <div class="animal-image-container">
          <img
            :src="aiGuess.image_url"
            :alt="aiGuess.common_name"
            class="animal-image"
            @error="handleImageError"
          />
          <div class="conservation-badge" :class="conservationClass">
            {{ aiGuess.conservation_status }}
          </div>
        </div>

        <div class="animal-info">
          <h3 class="animal-name">{{ aiGuess.common_name }}</h3>
          <p class="scientific-name">{{ aiGuess.scientific_name }}</p>
        </div>
      </div>
    </div>

    <div class="guess-verification">
      <h3 class="verification-title">Was the AI correct?</h3>
      <div class="verification-buttons">
        <button
          @click="$emit('confirmCorrect')"
          class="verify-button correct-button"
        >
          <span class="button-icon">🎉</span>
          <span class="button-text">Yes, correct!</span>
        </button>

        <button
          @click="$emit('confirmIncorrect')"
          class="verify-button incorrect-button"
        >
          <span class="button-icon">🤔</span>
          <span class="button-text">No, wrong</span>
        </button>
      </div>
    </div>

    <div v-if="vocabulary && vocabulary.length > 0" class="vocabulary-section">
      <h3 class="vocabulary-title">Learn New Words</h3>
      <div class="vocabulary-grid">
        <div
          v-for="item in vocabulary"
          :key="item.term"
          class="vocabulary-card"
          @click="toggleDefinition(item.term)"
        >
          <div class="vocabulary-term">{{ item.term }}</div>
          <div
            v-if="showDefinitions.includes(item.term)"
            class="vocabulary-definition"
          >
            {{ item.definition }}
          </div>
        </div>
      </div>
    </div>

    <div class="answer-summary">
      <h3 class="summary-title">Your Answers</h3>
      <div class="answers-list">
        <div
          v-for="(answer, index) in userAnswers"
          :key="index"
          class="answer-item"
        >
          <div class="answer-question">{{ answer.question }}</div>
          <div class="answer-response" :class="answer.answer">
            {{ formatAnswer(answer.answer) }}
          </div>
        </div>
      </div>
    </div>

    <div class="game-actions">
      <button @click="$emit('restart')" class="action-button play-again-button">
        <span class="button-icon">🔄</span>
        <span class="button-text">Play Again</span>
      </button>

      <button @click="$emit('exit')" class="action-button exit-button">
        <span class="button-icon">🏠</span>
        <span class="button-text">Exit</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultScreen',
  props: {
    aiGuess: {
      type: Object,
      required: true
    },
    vocabulary: {
      type: Array,
      default: () => []
    },
    userAnswers: {
      type: Array,
      default: () => []
    }
  },
  emits: ['confirmCorrect', 'confirmIncorrect', 'restart', 'exit'],
  data() {
    return {
      showDefinitions: []
    }
  },
  computed: {
    conservationClass() {
      const status = this.aiGuess.conservation_status?.toLowerCase()
      if (status?.includes('critically')) return 'critically-endangered'
      if (status?.includes('endangered')) return 'endangered'
      if (status?.includes('vulnerable')) return 'vulnerable'
      return 'least-concern'
    }
  },
  methods: {
    handleImageError(event) {
      event.target.src = '/images/koala.png'
    },
    toggleDefinition(term) {
      if (this.showDefinitions.includes(term)) {
        this.showDefinitions = this.showDefinitions.filter(t => t !== term)
      } else {
        this.showDefinitions.push(term)
      }
    },
    formatAnswer(answer) {
      switch(answer) {
        case 'yes': return 'Yes'
        case 'no': return 'No'
        case 'dont_know': return "Don't Know"
        default: return answer
      }
    }
  }
}
</script>

<style scoped>
.result-screen {
  padding: var(--spacing-xl);
  text-align: center;
}

.result-header {
  margin-bottom: var(--spacing-xl);
}

.ai-avatar {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.result-title {
  font-size: var(--font-size-xl);
  color: var(--color-text);
  margin: 0;
  font-family: var(--font-cartoon);
}

.animal-result {
  margin-bottom: var(--spacing-xl);
}

.animal-card {
  background: white;
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-xl);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.animal-image-container {
  position: relative;
  margin-bottom: var(--spacing-lg);
}

.animal-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: var(--border-radius-lg);
  border: 3px solid var(--color-light);
}

.conservation-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-xs);
  font-weight: bold;
  color: white;
}

.critically-endangered { background: #ff4444; }
.endangered { background: #ff8800; }
.vulnerable { background: #ffcc00; color: #333; }
.least-concern { background: #44aa44; }

.animal-info {
  text-align: center;
}

.animal-name {
  font-size: var(--font-size-lg);
  color: var(--color-text);
  margin: 0 0 var(--spacing-sm) 0;
  font-family: var(--font-cartoon);
}

.scientific-name {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
  font-style: italic;
  margin: 0;
}

.guess-verification {
  margin-bottom: var(--spacing-xl);
}

.verification-title {
  font-size: var(--font-size-lg);
  color: var(--color-text);
  margin-bottom: var(--spacing-lg);
  font-family: var(--font-cartoon);
}

.verification-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.verify-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-cartoon);
  font-weight: bold;
}

.correct-button {
  background: var(--color-success);
  color: white;
}

.correct-button:hover {
  background: #28a745;
  transform: translateY(-2px);
}

.incorrect-button {
  background: var(--color-warning);
  color: white;
}

.incorrect-button:hover {
  background: #e0a800;
  transform: translateY(-2px);
}

.vocabulary-section {
  margin-bottom: var(--spacing-xl);
}

.vocabulary-title {
  font-size: var(--font-size-lg);
  color: var(--color-text);
  margin-bottom: var(--spacing-lg);
  font-family: var(--font-cartoon);
}

.vocabulary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  max-width: 600px;
  margin: 0 auto;
}

.vocabulary-card {
  background: var(--color-light);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.vocabulary-card:hover {
  background: white;
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.vocabulary-term {
  font-weight: bold;
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.vocabulary-definition {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.4;
}

.answer-summary {
  margin-bottom: var(--spacing-xl);
}

.summary-title {
  font-size: var(--font-size-lg);
  color: var(--color-text);
  margin-bottom: var(--spacing-lg);
  font-family: var(--font-cartoon);
}

.answers-list {
  max-width: 500px;
  margin: 0 auto;
  text-align: left;
}

.answer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-xs);
  background: var(--color-light);
  border-radius: var(--border-radius-md);
}

.answer-question {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  flex: 1;
}

.answer-response {
  font-weight: bold;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
}

.answer-response.yes {
  background: var(--color-success);
  color: white;
}

.answer-response.no {
  background: var(--color-error);
  color: white;
}

.answer-response.dont_know {
  background: var(--color-warning);
  color: white;
}

.game-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.action-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-cartoon);
  font-weight: bold;
}

.play-again-button {
  background: var(--color-primary);
  color: white;
}

.play-again-button:hover {
  background: var(--color-secondary);
  transform: translateY(-2px);
}

.exit-button {
  background: var(--color-text-secondary);
  color: white;
}

.exit-button:hover {
  background: var(--color-text);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .result-screen {
    padding: var(--spacing-lg);
  }

  .animal-image {
    width: 150px;
    height: 150px;
  }

  .verification-buttons {
    flex-direction: column;
    max-width: 200px;
    margin: 0 auto;
  }

  .game-actions {
    flex-direction: column;
    max-width: 200px;
    margin: 0 auto;
  }

  .vocabulary-grid {
    grid-template-columns: 1fr;
  }

  .answer-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}
</style>

