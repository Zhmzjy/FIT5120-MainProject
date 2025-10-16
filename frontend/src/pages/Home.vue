<template>
  <div class="home-page">
    <div class="background-wrapper">
      <img
        src="/images/v2osk-1Z2niiBPg5A-unsplash.jpg"
        style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1"
        alt="background"
      />
    </div>

    <TopNavigation @toggleMobileMenu="toggleMobileMenu" />

    <div class="hero-section">
      <div class="overlay"></div>
      <div class="hero-content">
        <h1 class="main-title">Welcome to Dondig's Wildlife Seminary</h1>
        <p class="subtitle">
          Explore Australia's wildlife through games, maps, and AI — fun learning
          for kids, and adventures for families.
        </p>
      </div>
    </div>

    <Footer />

    <div
      v-if="mobileMenuOpen"
      class="mobile-overlay"
      @click="closeMobileMenu"
    ></div>
  </div>
</template>

<script>
import TopNavigation from '../components/common/TopNavigation.vue'
import Footer from '../components/common/Footer.vue'

export default {
  name: 'Home',
  components: {
    TopNavigation,
    Footer
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
.home-page {
  width: 100%;
  min-height: 100vh;
  position: relative;
}

.background-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.hero-section {
  width: 100%;
  height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding-top: 70px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(0, 17, 34, 0.2) 0%,
    rgba(45, 80, 22, 0.15) 50%,
    rgba(0, 105, 148, 0.2) 100%
  );
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  padding: 2rem;
  color: #ffffff;
}

.main-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  margin-bottom: 5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  line-height: 1.1;
  transform: translateY(-155px);
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.2);
}

.subtitle {
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  line-height: 1.6;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  opacity: 0.95;
  max-width: 600px;
  margin: 0 auto;
  transform: translateY(-150px);
  -webkit-text-stroke: 1px rgba(255, 255, 255, 0.2);
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

@media (max-width: 768px) {
  .hero-section {
    padding-top: 60px;
  }

  .hero-content {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-content {
    padding: 1rem;
  }
}
</style>
