<template>
  <div class="game-summary">
    <div class="summary-card">
      <div class="summary-header">
        <h2>Game Complete!</h2>
        <div class="final-score">
          <span class="score-number">{{ correctAnswers }}/{{ totalRounds }}</span>
          <span class="score-label">Correct</span>
        </div>
      </div>

      <div class="performance-message">
        <div class="performance-icon">
          <img v-if="correctAnswers === 0" src="/images/shredder.png" alt="shredder" class="performance-image" />
          <img v-else-if="correctAnswers === 1" src="/images/e6(4).png" alt="e6-4" class="performance-image" />
          <img v-else-if="correctAnswers === 2" src="/images/e6(3).png" alt="e6-3" class="performance-image" />
          <img v-else-if="correctAnswers === 3" src="/images/e6(2).png" alt="e6-2" class="performance-image" />
          <img v-else-if="correctAnswers === 4" src="/images/e6(1).png" alt="e6-1" class="performance-image" />
          <img v-else-if="correctAnswers === totalRounds" src="/images/splinter.png" alt="splinter" class="performance-image" />
          <span v-else>{{ performanceIcon }}</span>
        </div>
        <p class="performance-text">{{ performanceMessage }}</p>
      </div>

      <div class="results-breakdown">
        <h3>Round Results</h3>
        <div class="results-list">
          <div
            v-for="result in results"
            :key="result.round"
            class="result-item"
            :class="{ correct: result.isCorrect, incorrect: !result.isCorrect }"
          >
            <div class="round-number">{{ result.round }}</div>
            <div class="animal-info">
              <img :src="result.animal.imageUrl" :alt="result.animal.commonName" />
              <span class="animal-name">{{ result.animal.commonName }}</span>
            </div>
            <div class="result-status">
              {{ result.isCorrect ? '✓' : '✗' }}
            </div>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <Button @click="$emit('play-again')" type="primary" size="large">
          Play Again
        </Button>
        <Button @click="$emit('go-home')" type="secondary" size="medium">
          Back to Home
        </Button>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'GameSummary',
  components: {
    Button
  },
  props: {
    totalRounds: {
      type: Number,
      required: true
    },
    correctAnswers: {
      type: Number,
      required: true
    },
    results: {
      type: Array,
      required: true
    }
  },
  emits: ['play-again', 'go-home'],
  computed: {
    scorePercentage() {
      return Math.round((this.correctAnswers / this.totalRounds) * 100)
    },
    performanceIcon() {
      const percentage = this.scorePercentage
      if (percentage >= 80) return '🏆'
      if (percentage >= 60) return '🎉'
      if (percentage >= 40) return '👍'
      return ''
    },
    performanceMessage() {
      if (this.correctAnswers === 0) return 'Keep trying! Every attempt helps you learn more about animals!'
      if (this.correctAnswers === 1) return 'Good start! You recognized one animal sound!'
      if (this.correctAnswers === 2) return 'Nice work! You are getting better at this!'
      if (this.correctAnswers === 3) return 'Great job! You have good listening skills!'
      if (this.correctAnswers === 4) return 'Excellent! You almost got them all!'
      if (this.correctAnswers === this.totalRounds) return 'Perfect! You are an animal sound expert!'

      const percentage = this.scorePercentage
      if (percentage === 100) return 'Perfect! You know your Australian animals very well!'
      if (percentage >= 80) return 'Excellent! You have great knowledge of animal sounds!'
      if (percentage >= 60) return 'Good job! You\'re learning to recognize animal sounds!'
      if (percentage >= 40) return 'Not bad! Keep practicing to improve your skills!'
      return 'Keep trying! Every attempt helps you learn more about animals!'
    }
  }
}
</script>

<style scoped>
.game-summary {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.summary-header {
  margin-bottom: 24px;
}

.summary-header h2 {
  color: #2d3748;
  font-size: 2rem;
  margin-bottom: 16px;
}

.final-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #ebf8ff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.score-number {
  font-size: 3rem;
  font-weight: bold;
  color: #2b6cb0;
  line-height: 1;
}

.score-label {
  color: #4a5568;
  font-size: 1.1rem;
  margin-top: 4px;
}

.performance-message {
  margin-bottom: 28px;
  padding: 20px;
  background: #f7fafc;
  border-radius: 12px;
}

.performance-icon {
  font-size: 3rem;
  margin-bottom: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.performance-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.performance-text {
  color: #4a5568;
  font-size: 1.1rem;
  line-height: 1.5;
  margin: 0;
}

.results-breakdown {
  margin-bottom: 28px;
}

.results-breakdown h3 {
  color: #2d3748;
  font-size: 1.3rem;
  margin-bottom: 16px;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.result-item.correct {
  background: #f0fff4;
  border-left: 4px solid #38a169;
}

.result-item.incorrect {
  background: #fed7d7;
  border-left: 4px solid #e53e3e;
}

.round-number {
  width: 40px;
  height: 40px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #4a5568;
  margin-right: 12px;
  flex-shrink: 0;
}

.animal-info {
  display: flex;
  align-items: center;
  flex: 1;
  gap: 12px;
}

.animal-info img {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  object-fit: cover;
}

.animal-name {
  color: #2d3748;
  font-weight: 500;
}

.result-status {
  font-size: 1.2rem;
  font-weight: bold;
  margin-left: 12px;
}

.result-item.correct .result-status {
  color: #38a169;
}

.result-item.incorrect .result-status {
  color: #e53e3e;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .summary-card {
    padding: 24px 16px;
    margin: 16px;
  }

  .summary-header h2 {
    font-size: 1.6rem;
  }

  .score-number {
    font-size: 2.5rem;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .result-item {
    padding: 8px;
  }

  .animal-info {
    gap: 8px;
  }

  .animal-info img {
    width: 32px;
    height: 32px;
  }
}
</style>
