<template>
  <div class="playing-daily">
    <div class="game-header">
      <h2 class="daily-title">Daily Wildle</h2>
      <div class="guess-counter">
        Guesses: {{ guesses.length }}/10
      </div>
    </div>

    <div v-if="showResult && latestGuess" class="result-section">
      <div class="animal-card">
        <div class="animal-info">
          <h3 class="animal-name">{{ getCorrectAnswerName() }}</h3>
          <div v-if="getCorrectAnswerFeedback()" class="feedback-grid">
            <div v-for="(field, key) in getCorrectAnswerFeedback()" :key="key" class="feedback-item">
              <div class="field-label">{{ getFieldLabel(key) }}</div>
              <div class="field-value" :class="getFieldClass(field.state)">
                {{ formatFieldValue(field, key) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="guess-section">
      <h3 class="guess-prompt">What Australian animal am I?</h3>

      <div class="input-section">
        <input
          v-model="currentGuess"
          @keyup.enter="submitGuess"
          type="text"
          placeholder="Type animal name..."
          class="guess-input"
          :disabled="isCompleted"
          list="animal-suggestions"
        />
        <datalist id="animal-suggestions">
          <option v-for="animal in availableAnimals" :key="animal" :value="animal" />
        </datalist>
        <button
          @click="submitGuess"
          class="submit-button"
          :disabled="!currentGuess.trim() || isCompleted"
        >
          Guess
        </button>
      </div>
    </div>

    <div v-if="feedback" class="feedback-section">
      <div class="feedback-message" :class="feedback.type">
        {{ feedback.message }}
      </div>
    </div>

    <div v-if="guesses.length > 0" class="guesses-history">
      <h4 class="history-title">Your Guesses:</h4>
      <div class="guesses-list">
        <div v-for="(guess, index) in reversedGuesses" :key="index" class="guess-item">
          <div class="guess-header">
            <span class="guess-number">{{ guesses.length - index }}.</span>
            <span class="guess-name">{{ getGuessName(guess) }}</span>
            <span class="guess-result" :class="getGuessResultClass(guess)">
              {{ getGuessResultIcon(guess) }}
            </span>
          </div>
          <div v-if="guess.feedback" class="guess-feedback">
            <div v-for="(field, key) in guess.feedback" :key="key" class="feedback-row">
              <span class="feedback-label">{{ getFieldLabel(key) }}:</span>
              <span class="feedback-value" :class="getFieldClass(field.state)">
                {{ formatFieldValue(field, key) }}
                <span v-if="field.direction" class="direction-hint">
                  {{ field.direction === 'higher' ? '↑' : '↓' }}
                </span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showResult" class="game-actions">
      <button @click="$emit('playAgain')" class="action-button">
        Play Again
      </button>
      <button @click="$emit('exit')" class="action-button secondary">
        Exit
      </button>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'PlayingDaily',
  components: {
    Button
  },
  props: {
    guesses: {
      type: Array,
      default: () => []
    },
    feedback: {
      type: Object,
      default: null
    },
    showResult: {
      type: Boolean,
      default: false
    },
    isCompleted: {
      type: Boolean,
      default: false
    },
    availableAnimals: {
      type: Array,
      default: () => []
    },
    gameData: {
      type: Object,
      default: null
    }
  },
  emits: ['submitGuess'],
  data() {
    return {
      currentGuess: ''
    }
  },
  computed: {
    latestGuess() {
      return this.guesses.length > 0 ? this.guesses[this.guesses.length - 1] : null
    },
    reversedGuesses() {
      return this.guesses.slice().reverse()
    }
  },
  methods: {
    submitGuess() {
      if (this.currentGuess.trim()) {
        this.$emit('submitGuess', this.currentGuess.trim())
        this.currentGuess = ''
      }
    },
    getFieldLabel(key) {
      const labels = {
        'taxon_class_ET': 'Class',
        'EPBCThreatStatus': 'EPBC Status',
        'size_bucket': 'Size',
        'activity_top': 'Activity',
        'habitats': 'Habitats',
        'diet': 'Diet'
      }
      return labels[key] || key
    },
    getFieldClass(state) {
      return {
        'correct': state === 'correct',
        'partial': state === 'partial',
        'incorrect': state === 'incorrect',
        'unknown': state === 'unknown'
      }
    },
    formatFieldValue(field, key) {
      if (Array.isArray(field.guess)) {
        return field.guess.join(', ')
      }
      return field.guess || 'Unknown'
    },
    getGuessName(guess) {
      return guess.guess?.CommonName || guess.animal_name || 'Unknown Animal'
    },
    getGuessResultClass(guess) {
      if (guess.solved) {
        return 'correct'
      } else if (guess.feedback) {
        return 'partial'
      }
      return 'incorrect'
    },
    getGuessResultIcon(guess) {
      return guess.solved ? '✓' : '○'
    },
    getCorrectAnswerName() {
      const correctGuess = this.guesses.find(guess => guess.solved && guess.isCorrect)
      if (correctGuess) {
        return correctGuess.guess?.CommonName || correctGuess.guessName || 'Unknown Animal'
      }
      return this.latestGuess?.guess?.CommonName || 'Unknown Animal'
    },
    getCorrectAnswerFeedback() {
      const correctGuess = this.guesses.find(guess => guess.solved && guess.isCorrect)
      if (correctGuess && correctGuess.feedback) {
        return correctGuess.feedback
      }
      return this.latestGuess?.feedback || null
    }
  }
}
</script>

<style scoped>
.playing-daily {
  padding: 32px;
  text-align: center;
  min-height: 60vh;
}

.game-header {
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.daily-title {
  font-size: 28px;
  color: #2c3e50;
  margin: 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.guess-counter {
  font-size: 16px;
  color: #2c3e50;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  border: 2px solid #3498db;
}

.result-section {
  margin-bottom: 32px;
}

.animal-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
  border: 2px solid #e8f5e8;
}

.animal-name {
  font-size: 24px;
  color: #2c3e50;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.guess-section {
  margin-bottom: 32px;
}

.guess-prompt {
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 24px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.input-section {
  display: flex;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.guess-input {
  flex: 1;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #3498db;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s;
  background: white;
}

.guess-input:focus {
  border-color: #2980b9;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.3);
}

.submit-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.submit-button:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
}

.submit-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
}

.feedback-section {
  margin-bottom: 24px;
}

.feedback-message {
  padding: 16px;
  border-radius: 12px;
  font-weight: bold;
  max-width: 500px;
  margin: 0 auto;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.feedback-message.correct {
  background: #d4edda;
  color: #155724;
  border: 2px solid #27ae60;
}

.feedback-message.incorrect {
  background: #f8d7da;
  color: #721c24;
  border: 2px solid #e74c3c;
}

.feedback-message.failed {
  background: #f8d7da;
  color: #721c24;
  border: 2px solid #e74c3c;
}

.guesses-history {
  margin-bottom: 32px;
}

.history-title {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 16px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.guesses-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 600px;
  margin: 0 auto;
}

.guess-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 16px;
  border: 2px solid #ecf0f1;
  transition: all 0.3s;
}

.guess-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.guess-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.guess-number {
  font-weight: bold;
  color: #7f8c8d;
  min-width: 30px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.guess-name {
  flex: 1;
  color: #2c3e50;
  font-weight: bold;
  text-align: left;
  margin: 0 16px;
}

.guess-result {
  font-size: 20px;
  font-weight: bold;
}

.guess-feedback {
  border-top: 1px solid #ecf0f1;
  padding-top: 8px;
  margin-top: 8px;
}

.feedback-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  align-items: center;
}

.feedback-label {
  font-weight: bold;
  color: #34495e;
  min-width: 100px;
  text-align: left;
}

.feedback-value {
  color: #7f8c8d;
  text-align: right;
  flex: 1;
}

.feedback-value.correct {
  background: #d4edda;
  color: #155724;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
}

.feedback-value.partial {
  background: #fff3cd;
  color: #856404;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
}

.feedback-value.incorrect {
  background: #f8d7da;
  color: #721c24;
  padding: 4px 8px;
  border-radius: 6px;
}

.direction-hint {
  font-size: 14px;
  color: #95a5a6;
  margin-left: 4px;
}

.feedback-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  margin-top: 16px;
}

.feedback-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.field-label {
  font-weight: bold;
  color: #2c3e50;
  min-width: 100px;
}

.field-value {
  color: #34495e;
  text-align: right;
}

.guess-result.correct {
  color: #27ae60;
}

.guess-result.partial {
  color: #f39c12;
}

.guess-result.incorrect {
  color: #e74c3c;
}

.game-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 32px;
}

.action-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 14px 28px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
  min-width: 120px;
}

.action-button:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.action-button.secondary {
  background: #95a5a6;
}

.action-button.secondary:hover {
  background: #7f8c8d;
}

@media (max-width: 768px) {
  .playing-daily {
    padding: 16px;
  }

  .game-header {
    flex-direction: column;
    gap: 16px;
  }

  .input-section {
    flex-direction: column;
    max-width: 100%;
  }

  .feedback-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .feedback-label {
    min-width: unset;
  }

  .feedback-value {
    text-align: left;
  }

  .game-actions {
    flex-direction: column;
    max-width: 200px;
    margin: 32px auto 0;
  }
}
</style>
