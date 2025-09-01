<template>
  <Layout>
    <div class="home-page">
      <div class="hero-section">
        <div class="background-image">
          <img src="/images/v2osk-1Z2niiBPg5A-unsplash.jpg" alt="Australian Wildlife Background" />
          <div class="overlay"></div>
        </div>

        <div class="hero-content">
          <h1 class="main-title">Welcome to Wildlife Academy</h1>
          <p class="subtitle">
            Explore Australia's wildlife through games, maps, and AI — fun learning for kids, and adventures for families.
          </p>

          <div class="action-buttons">
            <Button
              type="primary"
              size="large"
              @click="navigateToLearnWildlife"
            >
              Learn Wildlife
            </Button>

            <Button
              type="primary"
              size="large"
              @click="navigateToSeasonal"
            >
              Seasonal Activities
            </Button>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import Layout from '../components/common/Layout.vue'
import Button from '../components/common/Button.vue'

export default {
  name: 'Home',
  components: {
    Layout,
    Button
  },
  methods: {
    navigateToLearnWildlife() {
      this.$router.push('/learn-wildlife')
    },
    navigateToSeasonal() {
      this.$router.push('/seasonal')
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

.hero-section {
  width: 100%;
  height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.background-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(0, 17, 34, 0.4) 0%,
    rgba(45, 80, 22, 0.3) 50%,
    rgba(0, 105, 148, 0.4) 100%
  );
  z-index: 2;
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  max-width: 800px;
  padding: var(--spacing-xl);
  color: var(--text-white);
}

.main-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  margin-bottom: var(--spacing-lg);
  text-shadow: 2px 2px 4px var(--shadow-dark);
  line-height: 1.1;
}

.subtitle {
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  line-height: 1.6;
  margin-bottom: var(--spacing-2xl);
  text-shadow: 1px 1px 2px var(--shadow-dark);
  opacity: 0.95;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-lg);
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .hero-content {
    padding: var(--spacing-lg);
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-md);
  }

  .main-title {
    margin-bottom: var(--spacing-md);
  }

  .subtitle {
    margin-bottom: var(--spacing-xl);
  }
}

@media (max-width: 480px) {
  .hero-content {
    padding: var(--spacing-md);
  }
}
</style>
