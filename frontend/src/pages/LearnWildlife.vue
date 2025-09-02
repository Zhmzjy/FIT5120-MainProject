<template>
  <div class="wildlife-app">
    <img src="/images/backformap.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">
    <header class="top-nav">
      <div class="nav-content">
        <div class="logo">
          <h2>Wildlife Academy</h2>
        </div>
        <nav class="nav-links">
          <button @click="goHome" class="nav-link">Home</button>
          <button @click="showSeasonalWildlife" class="nav-link">Seasonal Wildlife</button>
        </nav>
        <button @click="toggleMobileSidebar" class="mobile-toggle">🍔</button>
      </div>
    </header>

    <div class="main-layout">
      <aside class="left-sidebar" :class="{ 'mobile-open': mobileMenuOpen }">
        <LeftFilters />
      </aside>

      <main class="center-content">
        <MapView />
      </main>

      <RightDrawer />
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileSidebar"></div>
  </div>
</template>

<script>
import LeftFilters from '../components/wildlife/LeftFilters.vue'
import MapView from '../components/wildlife/MapView.vue'
import RightDrawer from '../components/wildlife/RightDrawer.vue'

export default {
  name: 'LearnWildlife',
  components: {
    LeftFilters,
    MapView,
    RightDrawer
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
    showSeasonalWildlife() {
      console.log('Showing seasonal wildlife')
    },
    toggleMobileSidebar() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileSidebar() {
      this.mobileMenuOpen = false
    }
  }
}
</script>

<style scoped>
.wildlife-app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  gap: 0;
  border: none;
  margin: 0;
  padding: 0;
}

.top-nav {
  background: url('/images/backformap.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  filter: brightness(0.8) contrast(1.1);
  padding: 0 var(--spacing-lg);
  flex-shrink: 0;
  z-index: 100;
  position: relative;
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

.logo h2 {
  margin: 0;
  color: var(--text-white);
  font-size: var(--font-size-xl);
  font-family: var(--font-family-heading);
  font-weight: bold;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8), 1px 1px 2px rgba(0, 0, 0, 0.9);
  animation: logoFloat 2s ease-in-out infinite;
  background: transparent;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-lg);
  transition: all var(--transition-bounce);
}

.logo h2:hover {
  background: transparent;
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
  background: transparent;
  color: var(--text-white);
  border: 2px solid rgba(255, 255, 255, 0.7);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-pill);
  font-family: var(--font-family-primary);
  font-weight: bold;
  cursor: pointer;
  transition: all var(--transition-bounce);
  font-size: var(--font-size-sm);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-white);
  border-color: rgba(255, 255, 255, 1);
  transform: translateY(-2px) scale(1.05);
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9);
}

.mobile-toggle {
  display: none;
  background: transparent;
  color: var(--text-white);
  border: 2px solid rgba(255, 255, 255, 0.7);
  padding: var(--spacing-sm);
  border-radius: 50%;
  font-size: var(--font-size-lg);
  cursor: pointer;
  transition: all var(--transition-bounce);
  width: 50px;
  height: 50px;
  align-items: center;
  justify-content: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.mobile-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 1);
  transform: rotate(180deg) scale(1.1);
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9);
}

.main-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
  gap: 0;
  border: none;
}

.left-sidebar {
  width: 320px;
  flex-shrink: 0;
  background: transparent;
  overflow-y: auto;
  border: none;
}

.center-content {
  flex: 1;
  background: url('/images/backformap.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  filter: brightness(0.8) contrast(1.1);
  overflow: hidden;
  padding: 20px;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 150;
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }

  .left-sidebar {
    position: fixed;
    top: 60px;
    left: -320px;
    height: calc(100vh - 60px);
    z-index: 200;
    transition: left 0.3s ease;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .left-sidebar.mobile-open {
    left: 0;
  }

  .center-content {
    width: 100%;
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .center-content {
    padding: 5px;
  }

  .nav-content {
    padding: 0 10px;
  }
}
</style>
