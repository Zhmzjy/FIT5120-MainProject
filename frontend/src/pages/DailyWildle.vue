<template>
  <div class="daily-wildle-page">
    <img src="/images/epic3-background.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

    <header class="top-nav">
      <div class="nav-content">
        <div class="logo">
          <button @click="goHome" class="logo-button">Wildlife Academy</button>
        </div>
        <nav class="nav-links">
          <button @click="goHome" class="nav-link">Home</button>
          <button @click="goToWildlife" class="nav-link">Learn Wildlife</button>
          <button @click="goToSeasonal" class="nav-link">Seasonal Activities</button>
          <button @click="goToAIChallenge" class="nav-link">AI Challenge</button>
          <button @click="goToDailyWildle" class="nav-link">Daily Wildle</button>
          <button @click="goToConservation" class="nav-link">Conservation</button>
        </nav>
        <button @click="toggleMobileMenu" class="mobile-toggle">🍔</button>
      </div>
    </header>

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
import ApiService from '../services/api.js'

export default {
  name: 'DailyWildle',
  components: {
    DailyWildleContainer
  },
  data() {
    return {
      mobileMenuOpen: false,
      gameData: null,
      gameState: {
        phase: 'welcome',
        guesses: [],
        isCompleted: false,
        showResult: false,
        feedback: null,
        availableAnimals: []
      }
    }
  },
  async mounted() {
    await this.loadGameData()
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    goToWildlife() {
      this.$router.push('/learn-wildlife')
    },
    goToSeasonal() {
      this.$router.push('/seasonal')
    },
    goToAIChallenge() {
      this.$router.push('/ai-challenge')
    },
    goToDailyWildle() {
      this.$router.push('/daily-wildle')
    },
    goToConservation() {
      this.$router.push('/conservation')
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    async loadGameData() {
      try {
        const response = await ApiService.getDailyWildleToday()
        this.gameData = response
        this.gameState.availableAnimals = response.vocab.animals
      } catch (error) {
        console.error('Failed to load game data:', error)
      }
    },
    handleStartDaily() {
      this.gameState.phase = 'playing'
      this.gameState.guesses = []
      this.gameState.feedback = null
      this.gameState.isCompleted = false
      this.gameState.showResult = false
    },
    async handleSubmitGuess(guess) {
      const currentGuessCount = this.gameState.guesses.length + 1

      try {
        const response = await ApiService.submitDailyWildleGuess(guess, currentGuessCount)

        this.gameState.guesses.push({
          guessName: guess,
          isCorrect: response.solved,
          isValidAnimal: true,
          guess: response.guess,
          feedback: response.feedback,
          solved: response.solved
        })

        if (response.solved) {
          this.gameState.feedback = {
            type: 'correct',
            message: 'Correct! Well done!'
          }
          this.gameState.isCompleted = true
          this.gameState.showResult = true
        } else if (response.game_over) {
          this.gameState.feedback = {
            type: 'failed',
            message: response.message || `Game over! The correct answer was: ${response.correct_answer}`
          }
          this.gameState.isCompleted = true
          this.gameState.showResult = true
          if (response.correct_answer && response.correct_answer !== guess) {
            this.gameState.guesses.push({
              guessName: response.correct_answer,
              isCorrect: true,
              isValidAnimal: true,
              guess: { CommonName: response.correct_answer },
              feedback: response.feedback || null,
              solved: true
            })
          }
        } else if (currentGuessCount >= 10) {
          this.gameState.feedback = {
            type: 'failed',
            message: `Game over! The correct answer was: ${response.guess?.CommonName || 'Unknown'}`
          }
          this.gameState.isCompleted = true
          this.gameState.showResult = true
        } else {
          this.gameState.feedback = {
            type: 'partial',
            message: 'Not quite right. Check the feedback for clues!'
          }
        }
      } catch (error) {
        this.gameState.guesses.push({
          guessName: guess,
          isCorrect: false,
          isValidAnimal: false,
          guess: { CommonName: guess },
          feedback: null,
          solved: false
        })

        if (currentGuessCount >= 10) {
          this.gameState.feedback = {
            type: 'failed',
            message: `Game over! The correct answer was: ${this.gameData?.target?.CommonName || 'Unknown'}`
          }
          this.gameState.showResult = true
          this.gameState.isCompleted = true
          if (this.gameData?.target?.CommonName) {
            this.gameState.guesses.push({
              guessName: this.gameData.target.CommonName,
              isCorrect: true,
              isValidAnimal: true,
              guess: this.gameData.target,
              feedback: null,
              solved: true
            })
          }
        } else {
          let hintMessage = "That animal is not in our database. "
          if (currentGuessCount >= 2 && this.gameData?.target) {
            const targetClass = this.gameData.target.taxon_class_ET
            if (targetClass) {
              hintMessage += `Hint: Today's animal is a ${targetClass.toLowerCase()}.`
            } else {
              hintMessage += "Try selecting from the autocomplete list."
            }
          } else {
            hintMessage += "Try selecting from the autocomplete list."
          }

          this.gameState.feedback = {
            type: 'error',
            message: hintMessage
          }
        }
      }
    },
    handlePlayAgain() {
      this.gameState.phase = 'welcome'
      this.gameState.isCompleted = false
      this.gameState.showResult = false
      this.gameState.guesses = []
      this.gameState.feedback = null
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
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.top-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: transparent;
  backdrop-filter: none;
  border-bottom: none;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-button {
  background: none;
  border: none;
  font-size: 24px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  background: none;
  border: none;
  font-size: 16px;
  color: white;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background-color 0.3s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: white;
}

.main-content {
  flex: 1;
  padding: 32px;
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
  .nav-links {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }

  .main-content {
    padding: 16px;
  }
}
</style>
