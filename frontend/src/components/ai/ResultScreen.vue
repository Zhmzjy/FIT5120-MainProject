<template>
  <div class="result-screen">
    <div class="result-header">
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
      <div v-if="!userFeedback" class="verification-buttons">
        <Button
          class="verify-button correct-button"
          @click="handleCorrectGuess"
          type="primary"
          size="large"
        >
          Yes, correct!
        </Button>
        <Button
          class="verify-button incorrect-button"
          @click="handleIncorrectGuess"
          type="secondary"
          size="large"
        >
          No, wrong
        </Button>
      </div>
      <div v-if="userFeedback" class="feedback-message" :class="userFeedback.type">
        {{ userFeedback.message }}
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
      <Button @click="$emit('restart')" class="action-button play-again-button" type="primary" size="large">
        Play Again
      </Button>
      <Button @click="$emit('exit')" class="action-button exit-button" type="secondary" size="large">
        Exit Game
      </Button>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'ResultScreen',
  components: {
    Button
  },
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
      showDefinitions: [],
      userFeedback: null
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
    },
    handleCorrectGuess() {
      this.userFeedback = {
        message: 'Great! You and AI matched the same animal 🐨✨',
        type: 'success'
      }
      this.$emit('confirmCorrect')
    },
    handleIncorrectGuess() {
      this.userFeedback = {
        message: 'Nice try, AI! But I am smarter today 😎',
        type: 'error'
      }
      this.$emit('confirmIncorrect')
    }
  }
}
</script>

<style scoped>
.result-screen {
  padding: 32px;
  text-align: center;
}

.result-header {
  margin-bottom: 32px;
}

.result-title {
  font-size: 24px;
  color: black;
  margin: 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.animal-result {
  margin-bottom: 32px;
}

.animal-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.animal-image-container {
  position: relative;
  margin-bottom: 24px;
}

.animal-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  border: 3px solid #f0f0f0;
}

.conservation-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
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
  font-size: 20px;
  color: black;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.scientific-name {
  font-size: 16px;
  color: black;
  font-style: italic;
  margin: 0;
}

.guess-verification {
  margin-bottom: 32px;
}

.verification-title {
  font-size: 20px;
  color: black;
  margin-bottom: 24px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.verification-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.verify-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.correct-button {
  background: #4CAF50;
  color: black;
}

.correct-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.incorrect-button {
  background: #FFC107;
  color: black;
}

.incorrect-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.feedback-message {
  margin-top: 16px;
  padding: 16px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: bold;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.feedback-message.success {
  background: #d4edda;
  color: #155724;
  border: 2px solid #c3e6cb;
}

.feedback-message.error {
  background: #f8d7da;
  color: #721c24;
  border: 2px solid #f5c6cb;
}

.vocabulary-section {
  margin-bottom: 32px;
}

.vocabulary-title {
  font-size: 20px;
  color: black;
  margin-bottom: 24px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.vocabulary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  max-width: 600px;
  margin: 0 auto;
}

.vocabulary-card {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.vocabulary-card:hover {
  background: white;
  border-color: #3498db;
  transform: translateY(-2px);
}

.vocabulary-term {
  font-weight: bold;
  color: black;
  margin-bottom: 8px;
}

.vocabulary-definition {
  font-size: 14px;
  color: black;
  line-height: 1.4;
}

.answer-summary {
  margin-bottom: 32px;
}

.summary-title {
  font-size: 20px;
  color: black;
  margin-bottom: 24px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
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
  padding: 8px 16px;
  margin-bottom: 4px;
  background: #f5f5f5;
  border-radius: 8px;
}

.answer-question {
  font-size: 14px;
  color: black;
  flex: 1;
}

.answer-response {
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 14px;
}

.answer-response.yes {
  background: #4CAF50;
  color: black;
}

.answer-response.no {
  background: #f44336;
  color: black;
}

.answer-response.dont_know {
  background: #FFC107;
  color: black;
}

.game-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.play-again-button {
  background: #3498db;
  color: black;
}

.play-again-button:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.exit-button {
  background: #95a5a6;
  color: black;
}

.exit-button:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .result-screen {
    padding: 24px;
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
    gap: 4px;
  }
}
</style>
