<template>
  <div class="wildlife-app">
    <header class="top-nav">
      <div class="nav-content">
        <div class="logo">
          <h2>Wildlife Academy</h2>
        </div>
        <nav class="nav-links">
          <button @click="goHome" class="nav-link">Home</button>
          <button @click="goToFindZoo" class="nav-link">Find Zoo</button>
        </nav>
        <button @click="toggleMobileSidebar" class="mobile-toggle">☰</button>
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

    <footer class="bottom-bar">
      <LegendBar />
    </footer>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileSidebar"></div>
  </div>
</template>

<script>
import LeftFilters from '../components/wildlife/LeftFilters.vue'
import MapView from '../components/wildlife/MapView.vue'
import RightDrawer from '../components/wildlife/RightDrawer.vue'
import LegendBar from '../components/wildlife/LegendBar.vue'

export default {
  name: 'LearnWildlife',
  components: {
    LeftFilters,
    MapView,
    RightDrawer,
    LegendBar
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
    goToFindZoo() {
      this.$router.push('/find-zoo')
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
}

.top-nav {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 0 20px;
  flex-shrink: 0;
  z-index: 100;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  max-width: 100%;
}

.logo h2 {
  margin: 0;
  color: #2d5a27;
  font-size: 20px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  background: none;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}

.nav-link:hover {
  background: #f5f5f5;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
}

.main-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.left-sidebar {
  width: 320px;
  flex-shrink: 0;
  background: white;
  overflow-y: auto;
}

.center-content {
  flex: 1;
  background: #f5f5f5;
  overflow: hidden;
  padding: 20px;
}

.bottom-bar {
  flex-shrink: 0;
  background: white;
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
