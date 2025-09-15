<template>
  <div class="welcome-screen">
    <div class="welcome-header">
      <h1 class="game-title">AI Animal Challenge</h1>
      <p class="game-subtitle">Can you outsmart the AI?</p>
    </div>

    <div class="game-instructions">
      <h2>How to Play</h2>
      <div class="instruction-steps">
        <div class="instruction-step">
          <div class="step-text">Think of an Australian animal</div>
        </div>
        <div class="instruction-step">
          <div class="step-text">Answer Yes/No/Don't Know questions</div>
        </div>
        <div class="instruction-step">
          <div class="step-text">See if the AI can guess your animal!</div>
        </div>
      </div>
    </div>

    <div class="welcome-actions">
      <button @click="$emit('startGame')" class="start-button">
        Start Challenge
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WelcomeScreen',
  emits: ['startGame']
}
</script>

<style scoped>
.welcome-screen {
  text-align: center;
  padding: var(--spacing-xl);
}

.welcome-header {
  margin-bottom: var(--spacing-xl);
}

.game-title {
  font-size: var(--font-size-xxl);
  color: var(--color-primary);
  margin: 0 0 var(--spacing-sm) 0;
  font-family: var(--font-cartoon);
  font-weight: bold;
}

.game-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.game-instructions {
  margin-bottom: var(--spacing-xl);
}

.game-instructions h2 {
  font-size: var(--font-size-xl);
  color: var(--color-text);
  margin-bottom: var(--spacing-lg);
  font-family: var(--font-cartoon);
}

.instruction-steps {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  max-width: 400px;
  margin: 0 auto;
}

.instruction-step {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-light);
  border-radius: var(--border-radius-lg);
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-text {
  font-size: var(--font-size-md);
  color: var(--color-text);
}

.welcome-actions {
  margin-bottom: var(--spacing-xl);
}

.start-button {
  background: linear-gradient(135deg, #333333, #000000);
  color: white;
  border: none;
  padding: var(--spacing-lg) var(--spacing-xl);
  font-size: var(--font-size-lg);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-family: var(--font-cartoon);
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: 0 auto;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}

.game-features {
  display: flex;
  justify-content: center;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.feature {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(255, 255, 255, 0.7);
  border-radius: var(--border-radius-md);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.feature-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
}

@media (max-width: 768px) {
  .welcome-screen {
    padding: var(--spacing-lg);
  }

  .game-title {
    font-size: var(--font-size-xl);
  }

  .instruction-steps {
    max-width: 100%;
  }

  .game-features {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
}
</style>
