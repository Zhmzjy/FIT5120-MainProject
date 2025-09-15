<template>
  <div class="playing-daily">
    <div class="game-header">
      <h2 class="daily-title">Daily Wildle</h2>
      <div class="guess-counter">
        Guess {{ guesses.length }} / {{ maxGuesses }}
      </div>
    </div>

    <div v-if="showResult" class="result-section">
      <div class="animal-card">
        <div class="animal-image-container">
          <img
            :src="currentAnimal.image_url"
            :alt="currentAnimal.common_name"
            class="animal-image"
          />
        </div>
        <div class="animal-info">
          <h3 class="animal-name">{{ currentAnimal.common_name }}</h3>
          <p class="scientific-name">{{ currentAnimal.scientific_name }}</p>
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
          placeholder="Type your guess..."
          class="guess-input"
          :disabled="showResult"
        />
        <button
          @click="submitGuess"
          class="submit-button"
          :disabled="!currentGuess.trim() || showResult"
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
        <div
          v-for="(guess, index) in guesses"
          :key="index"
          class="guess-item"
        >
          <span class="guess-number">{{ index + 1 }}.</span>
          <span class="guess-text">{{ guess }}</span>
          <span class="guess-result" :class="getGuessResultClass(guess)">{{ getGuessResultIcon(guess) }}</span>
        </div>
      </div>
    </div>

    <div v-if="showResult" class="game-actions">
      <button @click="$emit('playAgain')" class="action-button">
        Tomorrow's Challenge
      </button>
      <button @click="$emit('exit')" class="action-button secondary">
        Exit
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayingDaily',
  props: {
    currentAnimal: {
      type: Object,
      required: true
    },
    guesses: {
      type: Array,
      default: () => []
    },
    maxGuesses: {
      type: Number,
      default: 6
    },
    feedback: {
      type: Object,
      default: null
    },
    showResult: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submitGuess', 'playAgain', 'exit'],
  data() {
    return {
      currentGuess: ''
    }
  },
  methods: {
    submitGuess() {
      if (this.currentGuess.trim()) {
        this.$emit('submitGuess', this.currentGuess.trim())
        this.currentGuess = ''
      }
    },
    getGuessResultClass(guess) {
      const isCorrect = guess.toLowerCase().includes('koala')
      return isCorrect ? 'correct' : 'incorrect'
    },
    getGuessResultIcon(guess) {
      const isCorrect = guess.toLowerCase().includes('koala')
      return isCorrect ? '✓' : '❌'
    }
  }
}
</script>

<style scoped>
.playing-daily {
  padding: 32px;
  text-align: center;
}

.game-header {
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.daily-title {
  font-size: 28px;
  color: black;
  margin: 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.guess-counter {
  font-size: 16px;
  color: black;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
}

.result-section {
  margin-bottom: 32px;
}

.animal-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.animal-image-container {
  margin-bottom: 16px;
}

.animal-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
}

.animal-name {
  font-size: 24px;
  color: black;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.scientific-name {
  font-size: 16px;
  color: #666;
  font-style: italic;
  margin: 0;
}

.guess-section {
  margin-bottom: 32px;
}

.guess-prompt {
  font-size: 20px;
  color: black;
  margin-bottom: 24px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.input-section {
  display: flex;
  gap: 12px;
  max-width: 400px;
  margin: 0 auto;
}

.guess-input {
  flex: 1;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;
}

.guess-input:focus {
  border-color: #4CAF50;
}

.submit-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-weight: bold;
}

.submit-button:hover:not(:disabled) {
  background: #45a049;
}

.submit-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.feedback-section {
  margin-bottom: 24px;
}

.feedback-message {
  padding: 16px;
  border-radius: 8px;
  font-weight: bold;
  max-width: 500px;
  margin: 0 auto;
}

.feedback-message.correct {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.feedback-message.incorrect {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.feedback-message.failed {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.guesses-history {
  margin-bottom: 32px;
}

.history-title {
  font-size: 18px;
  color: black;
  margin-bottom: 16px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.guesses-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 400px;
  margin: 0 auto;
}

.guess-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  text-align: left;
}

.guess-number {
  font-weight: bold;
  color: #666;
  min-width: 20px;
}

.guess-text {
  flex: 1;
  color: black;
}

.guess-result {
  font-size: 18px;
}

.game-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.action-button:hover {
  background: #45a049;
}

.action-button.secondary {
  background: #6c757d;
}

.action-button.secondary:hover {
  background: #5a6268;
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

  .game-actions {
    flex-direction: column;
    max-width: 200px;
    margin: 0 auto;
  }
}
</style>
