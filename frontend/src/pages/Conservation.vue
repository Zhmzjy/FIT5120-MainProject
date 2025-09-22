<template>
  <div class="conservation-page">
    <img src="/images/epic3-background.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

    <TopNavigation @toggleMobileMenu="toggleMobileMenu" />

    <div class="main-content">
      <ConservationContainer />
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import ConservationContainer from '../components/conservation/ConservationContainer.vue'
import TopNavigation from '../components/common/TopNavigation.vue'

export default {
  name: 'Conservation',
  components: {
    ConservationContainer,
    TopNavigation
  },
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  methods: {
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
  font-family: var(--font-cartoon);
}

.main-content {
  flex: 1;
  padding: var(--spacing-xl);
  display: flex;
  justify-content: center;
  align-items: flex-start;
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
