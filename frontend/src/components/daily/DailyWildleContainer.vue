<template>
  <div class="daily-wildle-container">
    <WelcomeDaily
      v-if="gameState.phase === 'welcome'"
      @startDaily="$emit('startDaily')"
    />

    <PlayingDaily
      v-if="gameState.phase === 'playing'"
      :guesses="gameState.guesses"
      :feedback="gameState.feedback"
      :showResult="gameState.showResult"
      :isCompleted="gameState.isCompleted"
      :availableAnimals="gameState.availableAnimals"
      @submitGuess="$emit('submitGuess', $event)"
    />

    <CompletedDaily
      v-if="gameState.showResult"
      @playAgain="$emit('playAgain')"
      @exit="$emit('exit')"
    />
  </div>
</template>

<script>
import WelcomeDaily from './WelcomeDaily.vue'
import PlayingDaily from './PlayingDaily.vue'
import CompletedDaily from './CompletedDaily.vue'

export default {
  name: 'DailyWildleContainer',
  components: {
    WelcomeDaily,
    PlayingDaily,
    CompletedDaily
  },
  props: {
    gameState: {
      type: Object,
      required: true
    },
    gameData: {
      type: Object,
      default: null
    }
  },
  emits: ['startDaily', 'submitGuess', 'playAgain', 'exit']
}
</script>

<style scoped>
.daily-wildle-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  background: transparent;
  border-radius: 16px;
  box-shadow: none;
  backdrop-filter: none;
}

@media (max-width: 768px) {
  .daily-wildle-container {
    margin: 16px;
    padding: 16px;
  }
}
</style>
