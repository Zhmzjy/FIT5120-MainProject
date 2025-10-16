<template>
  <div class="ai-challenge-page">
    <img src="/images/epic3-background.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

    <TopNavigation @toggleMobileMenu="toggleMobileMenu" />

    <div class="main-content">
      <AIGameContainer
        :gameState="gameState"
        @startGame="handleStartGame"
        @submitAnswer="handleSubmitAnswer"
        @restartGame="handleRestartGame"
        @exitGame="handleExitGame"
      />
    </div>

    <Footer />

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import TopNavigation from '../components/common/TopNavigation.vue'
import AIGameContainer from '../components/ai/AIGameContainer.vue'
import Footer from '../components/common/Footer.vue'
import ApiService from '../services/api.js'

export default {
  name: 'AIChallenge',
  components: {
    TopNavigation,
    AIGameContainer,
    Footer
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
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
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
        const response = await ApiService.submitAnswer(
          this.sessionId,
          this.gameState.currentQuestion?.id || 'unknown',
          answer
        )

        this.gameState.userAnswers.push({
          question: this.gameState.currentQuestion?.text || this.gameState.currentQuestion,
          answer: answer
        })

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
  position: relative;
  font-family: var(--font-cartoon);
  padding-bottom: 20px;
}

.main-content {
  min-height: calc(100vh - 80px);
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
