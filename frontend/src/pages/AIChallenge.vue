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

export default {
  name: 'AIChallenge',
  components: {
    AIGameContainer
  },
  data() {
    return {
      mobileMenuOpen: false,
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
    handleStartGame() {
      this.gameState.phase = 'playing'
      this.gameState.questionHistory = []
      this.gameState.userAnswers = []
      this.gameState.candidateAnimals = []
      this.gameState.currentQuestion = "Does your animal live in water?"
    },
    handleSubmitAnswer(answer) {
      this.gameState.userAnswers.push({
        question: this.gameState.currentQuestion,
        answer: answer
      })

      if (this.gameState.userAnswers.length >= 10) {
        this.gameState.phase = 'result'
        this.gameState.aiGuess = {
          common_name: "Koala",
          scientific_name: "Phascolarctos cinereus",
          conservation_status: "Vulnerable",
          image_url: "/images/koala.png"
        }
        this.gameState.vocabulary = [
          { term: "Marsupial", definition: "An animal that carries its baby in a pouch" },
          { term: "Eucalyptus", definition: "A type of tree that koalas love to eat" },
          { term: "Vulnerable", definition: "A species that might become endangered" }
        ]
      } else {
        this.gameState.currentQuestion = this.getNextQuestion()
      }
    },
    getNextQuestion() {
      const questions = [
        "Does your animal live in water?",
        "Is your animal a mammal?",
        "Does your animal have fur?",
        "Is your animal larger than a cat?",
        "Does your animal live in trees?",
        "Is your animal active during the day?",
        "Does your animal eat plants?",
        "Does your animal have a pouch?",
        "Is your animal found in Australia?",
        "Does your animal make sounds?"
      ]
      return questions[this.gameState.userAnswers.length] || "Final question..."
    },
    handleRestartGame() {
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
