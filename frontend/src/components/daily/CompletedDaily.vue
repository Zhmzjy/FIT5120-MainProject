<template>
  <div class="completed-daily">
    <div class="completion-header">
      <h1 class="completion-title">Daily Wildle Complete!</h1>
      <p class="completion-subtitle">Come back tomorrow for a new animal challenge</p>
    </div>

    <div class="completion-message">
      <div class="message-card">
        <h3>Well Done!</h3>
        <p>You've completed today's Daily Wildle challenge.</p>
        <p>New challenges are available every day at midnight!</p>
      </div>
    </div>

    <div class="completion-actions">
      <button @click="$emit('exit')" class="action-button">
        Back to Home
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CompletedDaily',
  props: {
    hasPlayedToday: {
      type: Boolean,
      default: false
    }
  },
  emits: ['playAgain', 'exit']
}
</script>

<style scoped>
.completed-daily {
  text-align: center;
  padding: 32px;
}

.completion-header {
  margin-bottom: 32px;
}

.completion-title {
  font-size: 36px;
  color: #4CAF50;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.completion-subtitle {
  font-size: 18px;
  color: black;
  margin: 0;
  font-weight: 500;
}

.completion-message {
  margin-bottom: 32px;
}

.message-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.success-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.message-card h3 {
  font-size: 24px;
  color: black;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.message-card p {
  font-size: 16px;
  color: #666;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.completion-actions {
  display: flex;
  justify-content: center;
}

.action-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 16px 32px;
  font-size: 18px;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .completed-daily {
    padding: 24px;
  }

  .completion-title {
    font-size: 28px;
  }

  .message-card {
    padding: 24px;
  }
}
</style>
