<template>
  <div class="ai-game-container">
    <WelcomeScreen
      v-if="gameState.phase === 'welcome'"
      @startGame="$emit('startGame')"
    />

    <QuestionScreen
      v-if="gameState.phase === 'playing'"
      :currentQuestion="gameState.currentQuestion"
      :questionNumber="gameState.userAnswers.length + 1"
      :totalQuestions="10"
      @answer="$emit('submitAnswer', $event)"
    />

    <ResultScreen
      v-if="gameState.phase === 'result'"
      :aiGuess="gameState.aiGuess"
      :vocabulary="gameState.vocabulary"
      :userAnswers="gameState.userAnswers"
      @confirmCorrect="handleConfirmCorrect"
      @confirmIncorrect="handleConfirmIncorrect"
      @restart="$emit('restartGame')"
      @exit="$emit('exitGame')"
    />
  </div>
</template>

<script>
import WelcomeScreen from './WelcomeScreen.vue'
import QuestionScreen from './QuestionScreen.vue'
import ResultScreen from './ResultScreen.vue'

export default {
  name: 'AIGameContainer',
  components: {
    WelcomeScreen,
    QuestionScreen,
    ResultScreen
  },
  props: {
    gameState: {
      type: Object,
      required: true
    }
  },
  emits: ['startGame', 'submitAnswer', 'restartGame', 'exitGame'],
  methods: {
    handleConfirmCorrect() {
      console.log('AI guessed correctly!')
    },
    handleConfirmIncorrect() {
      console.log('AI guessed incorrectly!')
    }
  }
}
</script>

<style scoped>
.ai-game-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-lg);
  background: transparent;
  border-radius: var(--border-radius-xl);
  box-shadow: none;
  backdrop-filter: none;
}

@media (max-width: 768px) {
  .ai-game-container {
    margin: var(--spacing-md);
    padding: var(--spacing-md);
  }
}
</style>
