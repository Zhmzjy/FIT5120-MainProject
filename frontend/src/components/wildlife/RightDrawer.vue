<template>
  <div class="right-drawer" :class="{ 'drawer-open': isOpen }">
    <div class="drawer-header">
      <h3>🌏 Region Explorer</h3>
      <button @click="toggleDrawer" class="close-btn">✕</button>
    </div>
    <div class="drawer-content">
      <div v-if="selectedRegion" class="region-info">
        <div class="region-header">
          <h4>{{ selectedRegion.name }}</h4>
          <p class="region-type">{{ selectedRegion.state }}</p>
        </div>
        <div class="region-stats">
          <div class="stat-item">
            <span class="stat-number">{{ selectedRegion.totalSpecies }}</span>
            <span class="stat-label">Total Species</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ selectedRegion.totalObservations }}</span>
            <span class="stat-label">Observations</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ selectedRegion.endangeredSpecies }}</span>
            <span class="stat-label">Endangered</span>
          </div>
        </div>
        <div class="top-species">
          <h5>Top Species in Region</h5>
          <div v-for="species in selectedRegion.topSpecies" :key="species.id" class="species-item">
            <div class="species-info">
              <strong>{{ species.common_name }}</strong>
              <em>{{ species.scientific_name }}</em>
              <span class="observation-count">{{ species.count }} observations</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="placeholder-content">
        <div class="placeholder-icon">🗺️</div>
        <p>Click on a region to explore wildlife data!</p>
        <div class="region-tips">
          <h4>🌏 Explore Australia's Wildlife</h4>
          <ul>
            <li>� Browse by state and territory</li>
            <li>🦎 Filter by animal types</li>
            <li>🛡️ Check conservation status</li>
            <li>🌲 Discover bioregions</li>
          </ul>
        </div>
      </div>
    </div>
    <button v-if="!isOpen" @click="toggleDrawer" class="drawer-toggle">
      �️ Regions
    </button>
  </div>
  <div v-if="isOpen" class="drawer-overlay" @click="closeDrawer"></div>
</template>

<script>
export default {
  name: 'RightDrawer',
  props: {
    selectedRegion: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isOpen: false
    }
  },
  watch: {
    selectedRegion(newRegion) {
      if (newRegion) {
        this.isOpen = true
      }
    }
  },
  methods: {
    toggleDrawer() {
      this.isOpen = !this.isOpen
    },
    closeDrawer() {
      this.isOpen = false
      this.$emit('closeDrawer')
    }
  }
}
</script>

<style scoped>
.right-drawer {
  position: fixed;
  top: 0;
  right: -450px;
  width: 450px;
  height: 100vh;
  background: linear-gradient(135deg, var(--background-card) 0%, #fff0f8 100%);
  box-shadow: -4px 0 20px var(--shadow-colorful);
  transition: right var(--transition-bounce);
  z-index: 1000;
  padding: var(--spacing-lg);
  font-family: var(--font-family-primary);
  overflow-y: auto;
}

.drawer-open {
  right: 0;
}

.drawer-toggle {
  position: fixed;
  top: 50%;
  right: var(--spacing-md);
  transform: translateY(-50%);
  background: linear-gradient(135deg, var(--accent-blue), var(--primary-green));
  color: var(--text-white);
  border: none;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-pill);
  font-family: var(--font-family-primary);
  font-weight: bold;
  cursor: pointer;
  z-index: 1001;
  box-shadow: 0 4px 12px var(--shadow-colorful);
  transition: all var(--transition-bounce);
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

.drawer-toggle:hover {
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 8px 20px var(--shadow-colorful);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-md);
  border-bottom: 3px solid var(--accent-pink);
  background: linear-gradient(90deg, var(--accent-pink), var(--accent-yellow), var(--accent-blue));
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
  border-radius: var(--border-radius-lg);
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.drawer-header h3 {
  margin: 0;
  color: var(--text-white);
  font-size: var(--font-size-xl);
  font-weight: bold;
  text-shadow: 2px 2px 4px var(--shadow-dark);
}

.close-btn {
  background: var(--background-card);
  border: 2px solid var(--accent-pink);
  font-size: var(--font-size-lg);
  cursor: pointer;
  padding: var(--spacing-xs);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: var(--accent-pink);
  font-weight: bold;
  transition: all var(--transition-bounce);
}

.close-btn:hover {
  background: var(--accent-pink);
  color: var(--text-white);
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 4px 12px var(--shadow-colorful);
}

.animal-placeholder {
  text-align: center;
  padding: var(--spacing-2xl) var(--spacing-lg);
  color: var(--text-gray);
  background: var(--background-card);
  border-radius: var(--border-radius-xl);
  box-shadow: 0 8px 24px var(--shadow-light);
  border: 2px dashed var(--accent-blue);
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-lg);
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.animal-placeholder p {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xl);
  color: var(--text-dark);
  font-weight: bold;
}

.fun-facts {
  text-align: left;
  background: linear-gradient(135deg, var(--light-green), #e8f5e8);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 2px solid var(--primary-green);
}

.fun-facts h4 {
  color: var(--text-dark);
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-lg);
}

.fun-facts ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.fun-facts li {
  margin-bottom: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--background-card);
  border-radius: var(--border-radius-md);
  border-left: 4px solid var(--accent-yellow);
  font-size: var(--font-size-sm);
  color: var(--text-dark);
  transition: all var(--transition-normal);
}

.fun-facts li:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px var(--shadow-light);
}

.region-info {
  padding: var(--spacing-lg);
}

.region-header h4 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 1.4rem;
}

.region-type {
  color: var(--color-text-secondary);
  font-style: italic;
  margin-bottom: var(--spacing-lg);
}

.region-stats {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  backdrop-filter: blur(10px);
  flex: 1;
  min-width: 80px;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary-green);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-dark);
  text-align: center;
}

.top-species h5 {
  color: var(--primary-green);
  margin-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--primary-green);
  padding-bottom: var(--spacing-sm);
}

.species-item {
  background: rgba(255, 255, 255, 0.1);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  border-radius: var(--border-radius);
  backdrop-filter: blur(10px);
}

.species-info strong {
  display: block;
  color: var(--primary-green);
  margin-bottom: var(--spacing-xs);
}

.species-info em {
  display: block;
  color: var(--text-dark);
  margin-bottom: var(--spacing-xs);
  font-size: 0.9rem;
}

.observation-count {
  font-size: 0.8rem;
  color: var(--accent-yellow);
  font-weight: bold;
}

.placeholder-content {
  padding: var(--spacing-lg);
  text-align: center;
}

.region-tips {
  margin-top: var(--spacing-xl);
  text-align: left;
}

.region-tips h4 {
  color: var(--primary-green);
  margin-bottom: var(--spacing-md);
}

.region-tips ul {
  list-style: none;
  padding: 0;
}

.region-tips li {
  padding: var(--spacing-sm) 0;
  color: var(--text-dark);
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  z-index: 999;
  backdrop-filter: blur(2px);
}

@media (max-width: 768px) {
  .right-drawer {
    right: -100vw;
    width: 100vw;
    top: auto;
    bottom: 0;
    height: 70vh;
    border-radius: var(--border-radius-xl) var(--border-radius-xl) 0 0;
  }
  
  .drawer-open {
    right: 0;
  }
  
  .drawer-toggle {
    bottom: var(--spacing-lg);
    top: auto;
    transform: none;
    writing-mode: initial;
    text-orientation: initial;
  }
}
</style>
