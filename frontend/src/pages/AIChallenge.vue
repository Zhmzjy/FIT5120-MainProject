<template>
  <div class="ai-challenge-page">
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
      <AIGameContainer
        :gameState="gameState"
        @startGame="handleStartGame"
        @submitAnswer="handleSubmitAnswer"
        @restartGame="handleRestartGame"
        @exitGame="handleExitGame"
      />
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import AIGameContainer from '../components/ai/AIGameContainer.vue'
import ApiService from '../services/api.js'

export default {
  name: 'AIChallenge',
  components: {
    AIGameContainer
  },
  data() {
    return {
      mobileMenuOpen: false,
      sessionId: null,
      gameState: {
        phase: 'welcome',
        currentQuestion: null,
        questionHistory: [],
        userAnswers: [],
        candidateAnimals: [],
        aiGuess: null,
        isCorrectGuess: null,
        gameResult: null,
        vocabulary: []
      }
    }
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
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
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
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    async handleStartGame() {
      try {
        const response = await ApiService.createAISession()
        this.sessionId = response.session_id
        this.gameState.phase = 'playing'
        this.gameState.questionHistory = []
        this.gameState.userAnswers = []
        this.gameState.candidateAnimals = []
        await this.loadNextQuestion()
      } catch (error) {
        console.error('Failed to start game:', error)
        this.gameState.currentQuestion = "Error loading question. Please try again."
      }
    },
    async loadNextQuestion() {
      try {
        const response = await ApiService.getNextQuestion(this.sessionId)
        if (response.decision) {
          this.gameState.phase = 'result'
          this.gameState.aiGuess = {
            common_name: response.decision.common_name,
            scientific_name: response.decision.scientific_name,
            confidence: response.decision.confidence,
            questions_asked: response.decision.questions_asked
          }
          this.gameState.vocabulary = []
        } else if (response.question) {
          this.gameState.currentQuestion = response.question
        }
      } catch (error) {
        console.error('Failed to load question:', error)
        this.gameState.currentQuestion = "Error loading question. Please try again."
      }
    },
    async handleSubmitAnswer(answer) {
      try {
        this.gameState.userAnswers.push({
          question: this.gameState.currentQuestion?.text || this.gameState.currentQuestion,
          answer: answer
        })

        const response = await ApiService.submitAnswer(
          this.sessionId,
          this.gameState.currentQuestion?.id || 'unknown',
          answer
        )

        if (response.decision) {
          this.gameState.phase = 'result'
          this.gameState.aiGuess = {
            common_name: response.decision.common_name,
            scientific_name: response.decision.scientific_name,
            confidence: response.decision.confidence,
            questions_asked: response.decision.questions_asked
          }
          this.gameState.vocabulary = []
        } else if (response.next_question) {
          this.gameState.currentQuestion = response.next_question
        }
      } catch (error) {
        console.error('Failed to submit answer:', error)
        await this.loadNextQuestion()
      }
    },
    async handleRestartGame() {
      try {
        if (this.sessionId) {
          await ApiService.resetAISession(this.sessionId)
        }
        this.gameState = {
          phase: 'welcome',
          currentQuestion: null,
          questionHistory: [],
          userAnswers: [],
          candidateAnimals: [],
          aiGuess: null,
          isCorrectGuess: null,
          gameResult: null,
          vocabulary: []
        }
        this.sessionId = null
      } catch (error) {
        console.error('Failed to restart game:', error)
        this.gameState.phase = 'welcome'
      }
    },
    handleExitGame() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.ai-challenge-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: var(--font-cartoon);
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
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-button {
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  font-weight: bold;
  color: white;
  cursor: pointer;
  font-family: var(--font-cartoon);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.nav-links {
  display: flex;
  gap: var(--spacing-lg);
}

.nav-link {
  background: none;
  border: none;
  font-size: var(--font-size-md);
  color: white;
  cursor: pointer;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  transition: background-color 0.3s;
  font-family: var(--font-cartoon);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: var(--font-size-lg);
  cursor: pointer;
  color: white;
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
  .nav-links {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }

  .main-content {
    padding: var(--spacing-md);
  }
}
</style>
