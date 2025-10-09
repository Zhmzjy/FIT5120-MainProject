<template>
  <header class="top-nav">
    <div class="nav-content">
      <div class="logo">
        <Button @click="goHome" class="logo-button">Wildlife Academy</Button>
      </div>
      <nav class="nav-links">
        <Button @click="goHome" class="nav-link">Home</Button>
        <Button @click="goToWildlife" class="nav-link">Learn Wildlife</Button>
        <Button @click="goToSeasonal" class="nav-link">Seasonal Activities</Button>
        <Button @click="goToAIChallenge" class="nav-link">AI Challenge</Button>
        <Button @click="goToDailyWildle" class="nav-link">Daily Wildle</Button>
        <Button @click="goToConservation" class="nav-link">Conservation</Button>
        <Button @click="goToAudioGame" class="nav-link">Audio Game</Button>
        <Button @click="goToYearlyAnalysis" class="nav-link">Yearly Analysis</Button>
      </nav>
      <Button @click="toggleMobileMenu" class="mobile-toggle">🍔</Button>
    </div>
  </header>
</template>

<script>
import Button from './Button.vue'

export default {
  name: 'TopNavigation',
  components: {
    Button
  },
  emits: ['toggleMobileMenu'],
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
    goToAudioGame() {
      this.$router.push('/audio-game')
    },
    goToYearlyAnalysis() {
      this.$router.push('/yearly-analysis')
    },
    toggleMobileMenu() {
      this.$emit('toggleMobileMenu')
    }
  }
}
</script>

<style scoped>
.top-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: transparent;
  backdrop-filter: none;
  border-bottom: none;
  padding: 0 var(--spacing-lg);
  flex-shrink: 0;
  overflow: hidden;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  position: relative;
  z-index: 2;
}

.logo-button {
  margin: 0;
  color: var(--text-white);
  font-size: var(--font-size-xl);
  font-family: var(--font-family-heading);
  font-weight: bold;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8), 1px 1px 2px rgba(0, 0, 0, 0.9);
  animation: logoFloat 2s ease-in-out infinite;
  background: #1e293b;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-lg);
  transition: all var(--transition-bounce);
  border: none;
  cursor: pointer;
}

.logo-button:hover {
  background: #334155;
  transform: scale(1.02);
  text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.9), 2px 2px 4px rgba(0, 0, 0, 1);
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}

.nav-links {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.nav-link {
  background: #1e293b;
  color: #ffffff;
  border: 2px solid #1e293b;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-pill);
  font-family: var(--font-family-primary);
  font-weight: bold;
  cursor: pointer;
  transition: all var(--transition-bounce);
  font-size: var(--font-size-sm);
  text-shadow: none;
}

.nav-link:hover {
  background: #334155;
  color: #ffffff;
  border-color: #334155;
  transform: translateY(-2px) scale(1.05);
}

.mobile-toggle {
  display: none;
  background: #1e293b;
  color: #ffffff;
  border: 2px solid #1e293b;
  padding: var(--spacing-sm);
  border-radius: 50%;
  font-size: var(--font-size-lg);
  cursor: pointer;
  transition: all var(--transition-bounce);
  width: 50px;
  height: 50px;
  align-items: center;
  justify-content: center;
  text-shadow: none;
}

.mobile-toggle:hover {
  background: #334155;
  border-color: #334155;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }
}
</style>
