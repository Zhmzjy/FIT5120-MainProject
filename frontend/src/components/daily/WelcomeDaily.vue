<template>
  <div class="welcome-daily">
    <div class="welcome-header">
      <h1 class="game-title">Daily Wildle</h1>
      <p class="game-subtitle">Guess today's Australian animal!</p>
    </div>

    <div class="game-instructions">
      <h2>How to Play</h2>
      <div class="instruction-steps">
        <div class="instruction-step">
          <div class="step-text">You have 6 guesses to find today's animal</div>
        </div>
        <div class="instruction-step">
          <div class="step-text">Get hints with each wrong guess</div>
        </div>
        <div class="instruction-step">
          <div class="step-text">Learn about Australian wildlife!</div>
        </div>
      </div>
    </div>

    <div class="welcome-actions">
      <button @click="$emit('startDaily')" class="start-button">
        Start Today's Challenge
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WelcomeDaily',
  emits: ['startDaily']
}
</script>

<style scoped>
.welcome-daily {
  text-align: center;
  padding: 32px;
}

.welcome-header {
  margin-bottom: 32px;
}

.game-title {
  font-size: 48px;
  color: #4CAF50;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.game-subtitle {
  font-size: 20px;
  color: black;
  margin: 0;
  font-weight: 500;
}

.game-instructions {
  margin-bottom: 32px;
}

.game-instructions h2 {
  font-size: 24px;
  color: black;
  margin-bottom: 24px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.instruction-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 400px;
  margin: 0 auto;
}

.instruction-step {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.step-text {
  font-size: 16px;
  color: black;
  font-weight: 500;
}

.welcome-actions {
  margin-bottom: 32px;
}

.start-button {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border: none;
  padding: 16px 32px;
  font-size: 18px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 auto;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .welcome-daily {
    padding: 24px;
  }

  .game-title {
    font-size: 36px;
  }

  .instruction-steps {
    max-width: 100%;
  }
}
</style>
