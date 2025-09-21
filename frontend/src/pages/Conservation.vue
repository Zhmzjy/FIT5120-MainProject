<template>
  <div class="conservation-page">
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
      <ConservationContainer />
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import ConservationContainer from '../components/conservation/ConservationContainer.vue'
export default {
  name: 'Conservation',
  components: {
    ConservationContainer
  },
  data() {
    return {
      mobileMenuOpen: false
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
    goToAIChallenge() {
      this.$router.push('/ai-challenge')
    },
    goToDailyWildle() {
      this.$router.push('/daily-wildle')
    },
    goToConservation() {
      this.$router.push('/conservation')
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    }
  }
}
</script>

<style scoped>
.conservation-page {
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
