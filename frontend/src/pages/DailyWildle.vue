<template>
  <div class="daily-wildle-page">
    <img src="/images/epic3-background.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

    <TopNavigation @toggleMobileMenu="toggleMobileMenu" />

    <div class="main-content">
      <DailyWildleContainer
        :gameState="gameState"
        :gameData="gameData"
        @startDaily="handleStartDaily"
        @submitGuess="handleSubmitGuess"
        @playAgain="handlePlayAgain"
        @exit="handleExit"
      />
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import DailyWildleContainer from '../components/daily/DailyWildleContainer.vue'
import TopNavigation from '../components/common/TopNavigation.vue'
import ApiService from '../services/api.js'

export default {
  name: 'DailyWildle',
  components: {
    DailyWildleContainer,
    TopNavigation
  },
  data() {
    return {
      mobileMenuOpen: false,
      gameData: null,
      gameState: {
        phase: 'welcome',
        guesses: [],
        currentAnimal: null,
        gameOver: false,
        won: false,
        attempts: 0,
        maxAttempts: 10
      }
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    async handleStartDaily() {
      try {
        const response = await ApiService.getDailyWildleAnimal()
        this.gameData = response
        this.gameState.phase = 'playing'
        this.gameState.currentAnimal = response
        this.gameState.guesses = []
        this.gameState.gameOver = false
        this.gameState.won = false
        this.gameState.attempts = 0
      } catch (error) {
        console.error('Failed to start daily game:', error)
      }
    },
    async handleSubmitGuess(guess) {
      try {
        const response = await ApiService.submitDailyGuess(guess)

        this.gameState.guesses.push({
          guess: guess,
          feedback: response.feedback,
          isCorrect: response.is_correct
        })

        this.gameState.attempts++

        if (response.is_correct) {
          this.gameState.won = true
          this.gameState.gameOver = true
          this.gameState.phase = 'result'
        } else if (this.gameState.attempts >= this.gameState.maxAttempts) {
          this.gameState.gameOver = true
          this.gameState.phase = 'result'
        }
      } catch (error) {
        console.error('Failed to submit guess:', error)
      }
    },
    handlePlayAgain() {
      this.gameState = {
        phase: 'welcome',
        guesses: [],
        currentAnimal: null,
        gameOver: false,
        won: false,
        attempts: 0,
        maxAttempts: 10
      }
      this.gameData = null
    },
    handleExit() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.daily-wildle-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: var(--font-cartoon);
}

.main-content {
  flex: 1;
  padding: var(--spacing-xl);
  display: flex;
  justify-content: center;
  align-items: center;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

@media (max-width: 768px) {
  .main-content {
    padding: var(--spacing-md);
  }
}
</style>
