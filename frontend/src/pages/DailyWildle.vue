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
          <button @click="goToSeasonal" class="nav-link">Seasonal Wildlife</button>
          <button @click="goToAIChallenge" class="nav-link">AI Challenge</button>
        </nav>
        <button @click="toggleMobileMenu" class="mobile-toggle">🍔</button>
      </div>
    </header>

    <div class="main-content">
      <DailyWildleContainer
        :gameState="gameState"
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

export default {
  name: 'DailyWildle',
  components: {
    DailyWildleContainer
  },
  data() {
    return {
      mobileMenuOpen: false,
      gameState: {
        phase: 'welcome',
        currentAnimal: null,
        guesses: [],
        maxGuesses: 6,
        isCompleted: false,
        hasPlayedToday: false,
        feedback: null,
        showResult: false
      }
    }
  },
  mounted() {

  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    goToWildlife() {
      this.$router.push('/wildlife')
    },
    goToSeasonal() {
      this.$router.push('/seasonal')
    },
    goToAIChallenge() {
      this.$router.push('/ai-challenge')
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    checkDailyStatus() {
      // Remove daily restriction - always allow new game
      this.gameState.hasPlayedToday = false
      this.gameState.phase = 'welcome'
    },
    handleStartDaily() {
      this.gameState.phase = 'playing'
      this.gameState.currentAnimal = {
        common_name: "Koala",
        scientific_name: "Phascolarctos cinereus",
        image_url: "/images/koala.png",
        hints: [
          "This animal lives in trees",
          "This animal eats eucalyptus leaves",
          "This animal is a marsupial",
          "This animal sleeps most of the day",
          "This animal is found in eastern Australia"
        ]
      }
      this.gameState.guesses = []
      this.gameState.feedback = null
    },
    handleSubmitGuess(guess) {
      this.gameState.guesses.push(guess)

      const correct = guess.toLowerCase().includes('koala')

      if (correct) {
        this.gameState.feedback = {
          type: 'correct',
          message: 'Correct! Well done!'
        }
        this.gameState.isCompleted = true
        this.gameState.showResult = true
        this.saveProgress()
      } else if (this.gameState.guesses.length >= this.gameState.maxGuesses) {
        this.gameState.feedback = {
          type: 'failed',
          message: 'Out of guesses! The answer was Koala.'
        }
        this.gameState.isCompleted = true
        this.gameState.showResult = true
        this.saveProgress()
      } else {
        const hintIndex = Math.min(this.gameState.guesses.length - 1, this.gameState.currentAnimal.hints.length - 1)
        this.gameState.feedback = {
          type: 'incorrect',
          message: 'Incorrect. Hint: ' + this.gameState.currentAnimal.hints[hintIndex]
        }
      }
    },
    handlePlayAgain() {
      // Always allow restart - no daily check
      this.gameState.phase = 'welcome'
      this.gameState.isCompleted = false
      this.gameState.showResult = false
      this.gameState.hasPlayedToday = false
      this.gameState.guesses = []
      this.gameState.feedback = null
    },
    handleExit() {
      this.$router.push('/')
    },
    saveProgress() {
      // Remove localStorage save - no daily tracking needed
      this.gameState.hasPlayedToday = false
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
