<template>
  <div class="seasonal-page">
    <div class="hero-section">
      <div class="background-image">
        <img :src="currentBackgroundImage" :alt="`${selectedSeason} background`" />
        <div class="overlay"></div>
      </div>

      <div class="hero-content">
        <h1 class="main-title" :style="titleStyle">Seasonal Wildlife Activities</h1>
        <p class="subtitle" :style="subtitleStyle">Discover what animals do in different seasons!</p>

        <SeasonButtonGroup
          :selected-season="selectedSeason"
          @update:selected-season="selectSeason"
        />
      </div>
    </div>

    <div class="wildlife-analysis-section">
      <div class="side-background left-bg">
        <img :src="currentBackgroundImage" :alt="`${selectedSeason} background`" />
      </div>
      <div class="side-background right-bg">
        <img :src="currentBackgroundImage" :alt="`${selectedSeason} background`" />
      </div>

      <div class="analysis-container">
        <div class="analysis-header">
          <h2 class="analysis-title" :style="titleStyle">{{ selectedSeason }} Wildlife Analysis</h2>
          <p class="analysis-subtitle">Explore animal behaviors and patterns in {{ selectedSeason.toLowerCase() }}</p>
        </div>

        <div class="analysis-content">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-number" :style="titleStyle">245</div>
              <div class="stat-label">Active Species</div>
            </div>
            <div class="stat-card">
              <div class="stat-number" :style="titleStyle">87%</div>
              <div class="stat-label">Migration Rate</div>
            </div>
            <div class="stat-card">
              <div class="stat-number" :style="titleStyle">156</div>
              <div class="stat-label">Breeding Pairs</div>
            </div>
            <div class="stat-card">
              <div class="stat-number" :style="titleStyle">32°C</div>
              <div class="stat-label">Avg Temperature</div>
            </div>
          </div>

          <div class="activity-chart">
            <h3 class="chart-title">Animal Activity Levels</h3>
            <div class="chart-bars">
              <div class="chart-bar">
                <div class="bar-fill" :style="{ height: '80%', backgroundColor: getSeasonColor() }"></div>
                <span class="bar-label">Morning</span>
              </div>
              <div class="chart-bar">
                <div class="bar-fill" :style="{ height: '95%', backgroundColor: getSeasonColor() }"></div>
                <span class="bar-label">Afternoon</span>
              </div>
              <div class="chart-bar">
                <div class="bar-fill" :style="{ height: '65%', backgroundColor: getSeasonColor() }"></div>
                <span class="bar-label">Evening</span>
              </div>
              <div class="chart-bar">
                <div class="bar-fill" :style="{ height: '40%', backgroundColor: getSeasonColor() }"></div>
                <span class="bar-label">Night</span>
              </div>
            </div>
          </div>

          <div class="featured-animals">
            <h3 class="animals-title">Featured {{ selectedSeason }} Animals</h3>
            <div class="animals-grid">
              <div class="animal-card" v-for="animal in getSeasonAnimals()" :key="animal.name">
                <img :src="animal.image" :alt="animal.name" class="animal-image">
                <div class="animal-info">
                  <h4 class="animal-name">{{ animal.name }}</h4>
                  <p class="animal-activity">{{ animal.activity }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="scroll-arrow" @click="scrollDown">
      <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="6,9 12,15 18,9"></polyline>
      </svg>
    </div>
  </div>
</template>

<script>
import SeasonButtonGroup from '../components/seasonal/SeasonButtonGroup.vue'

export default {
  name: 'SeasonalPage',
  components: {
    SeasonButtonGroup
  },
  data() {
    return {
      selectedSeason: 'Spring',
      animalData: {
        Spring: [
          { name: 'Kangaroo', activity: 'Active breeding season', image: '/images/kangaroo.png' },
          { name: 'Koala', activity: 'Feeding on new eucalyptus leaves', image: '/images/koala.png' },
          { name: 'Echidna', activity: 'Foraging for insects', image: '/images/kangaroo.png' },
          { name: 'Wombat', activity: 'Building new burrows', image: '/images/koala.png' }
        ],
        Summer: [
          { name: 'Platypus', activity: 'Swimming in cool waters', image: '/images/kangaroo.png' },
          { name: 'Kookaburra', activity: 'Hunting in early morning', image: '/images/koala.png' },
          { name: 'Dingo', activity: 'Seeking shade during day', image: '/images/kangaroo.png' },
          { name: 'Bilby', activity: 'Nocturnal foraging', image: '/images/koala.png' }
        ],
        Autumn: [
          { name: 'Possum', activity: 'Storing food for winter', image: '/images/kangaroo.png' },
          { name: 'Wallaby', activity: 'Preparing winter coat', image: '/images/koala.png' },
          { name: 'Bandicoot', activity: 'Building winter shelter', image: '/images/kangaroo.png' },
          { name: 'Quoll', activity: 'Hunting before winter', image: '/images/koala.png' }
        ],
        Winter: [
          { name: 'Tasmanian Devil', activity: 'Conserving energy', image: '/images/kangaroo.png' },
          { name: 'Sugar Glider', activity: 'Huddling for warmth', image: '/images/koala.png' },
          { name: 'Numbat', activity: 'Limited daytime activity', image: '/images/kangaroo.png' },
          { name: 'Quokka', activity: 'Reduced movement', image: '/images/koala.png' }
        ]
      }
    }
  },
  computed: {
    currentBackgroundImage() {
      const images = {
        Spring: '/images/Spring.jpg',
        Summer: '/images/Summer.jpg',
        Autumn: '/images/Autumn.jpg',
        Winter: '/images/Winter.jpg'
      }
      return images[this.selectedSeason]
    },
    titleStyle() {
      const colors = {
        Spring: '#22c55e',
        Summer: '#eab308',
        Autumn: '#f97316',
        Winter: '#3b82f6'
      }
      return {
        color: colors[this.selectedSeason]
      }
    },
    subtitleStyle() {
      const colors = {
        Spring: '#86efac',
        Summer: '#fde047',
        Autumn: '#fdba74',
        Winter: '#93c5fd'
      }
      return {
        color: colors[this.selectedSeason]
      }
    }
  },
  methods: {
    selectSeason(season) {
      this.selectedSeason = season
    },
    scrollDown() {
      window.scrollBy({
        top: window.innerHeight,
        behavior: 'smooth'
      })
    },
    getSeasonColor() {
      const colors = {
        Spring: '#22c55e',
        Summer: '#eab308',
        Autumn: '#f97316',
        Winter: '#3b82f6'
      }
      return colors[this.selectedSeason]
    },
    getSeasonAnimals() {
      return this.animalData[this.selectedSeason] || []
    }
  }
}
</script>

<style scoped>
.seasonal-page {
  width: 100%;
  min-height: 200vh;
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
  transition: opacity 0.5s ease;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  z-index: 2;
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  padding: 2rem;
}

.main-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  transition: color 0.3s ease;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  transition: color 0.3s ease;
}

.wildlife-analysis-section {
  position: relative;
  min-height: 100vh;
  background: #f8fafc;
  overflow: hidden;
}

.side-background {
  position: absolute;
  top: 0;
  width: 200px;
  height: 100%;
  z-index: 1;
}

.left-bg {
  left: 0;
  clip-path: polygon(0 0, 100% 0, 80% 100%, 0% 100%);
}

.right-bg {
  right: 0;
  clip-path: polygon(20% 0, 100% 0, 100% 100%, 0% 100%);
}

.side-background img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.7);
}

.analysis-container {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.analysis-header {
  text-align: center;
  margin-bottom: 3rem;
}

.analysis-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.analysis-subtitle {
  font-size: 1.1rem;
  color: #64748b;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #64748b;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.activity-chart {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 3rem;
}

.chart-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #1e293b;
}

.chart-bars {
  display: flex;
  justify-content: space-between;
  align-items: end;
  height: 200px;
  gap: 1rem;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.bar-fill {
  width: 100%;
  background: #22c55e;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
}

.bar-label {
  font-size: 0.9rem;
  color: #64748b;
  text-align: center;
}

.featured-animals {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.animals-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #1e293b;
}

.animals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.animal-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 8px;
  background: #f8fafc;
  transition: transform 0.3s ease;
}

.animal-card:hover {
  transform: scale(1.02);
}

.animal-image {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.animal-name {
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #1e293b;
}

.animal-activity {
  font-size: 0.9rem;
  color: #64748b;
}

.scroll-arrow {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  cursor: pointer;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.scroll-arrow:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateX(-50%) translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.arrow-icon {
  width: 24px;
  height: 24px;
  color: #666;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-5px);
  }
  60% {
    transform: translateY(-3px);
  }
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .side-background {
    width: 100px;
  }

  .analysis-title {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .animals-grid {
    grid-template-columns: 1fr;
  }

  .scroll-arrow {
    width: 40px;
    height: 40px;
    bottom: 1.5rem;
  }

  .arrow-icon {
    width: 20px;
    height: 20px;
  }
}
</style>
