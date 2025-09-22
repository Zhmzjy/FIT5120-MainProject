<template>
  <div class="seasonal-page" :style="pageBgStyle">
    <div class="hero-section">
      <div class="hero-overlay"></div>

      <TopNavigation
        @toggleMobileMenu="toggleMobileMenu"
        :theme="'seasonal'"
        :selectedSeason="selectedSeason"
      />

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
      <div class="section-overlay"></div>

      <div class="analysis-container">
        <div class="data-analysis-wrapper">
          <div class="analysis-header">
            <h2 class="analysis-title" :style="titleStyle">{{ selectedSeason }} Wildlife Analysis</h2>
            <p class="analysis-subtitle">Explore animal behaviors and patterns in {{ selectedSeason.toLowerCase() }}</p>
          </div>

          <div class="analysis-content">
          <div class="season-kpi-section">
            <div class="kpi-card main-kpi">
              <div class="kpi-icon">🐨</div>
              <div class="kpi-content">
                <div class="kpi-number" :style="titleStyle">{{ getCurrentSeasonKPI().active_species || 'Loading...' }}</div>
                <div class="kpi-label">Active Species This Season</div>
                <div class="kpi-detail">{{ getCurrentSeasonKPI().total_observations || 0 }} total observations</div>
              </div>
            </div>
          </div>

          <div class="activity-time-chart">
            <h3 class="chart-title">Activity Time Distribution</h3>
            <div class="time-chart-container">
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill morning" :style="{ height: getActivityHeight('Morning'), backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Morning</span>
                  <span class="time-range">6AM - 12PM</span>
                  <span class="observation-count">{{ getCurrentSeasonActivity().find(a => a.time_bin === 'Morning')?.count || 0 }} observations</span>
                </div>
              </div>
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill afternoon" :style="{ height: getActivityHeight('Afternoon'), backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Afternoon</span>
                  <span class="time-range">12PM - 6PM</span>
                  <span class="observation-count">{{ getCurrentSeasonActivity().find(a => a.time_bin === 'Afternoon')?.count || 0 }} observations</span>
                </div>
              </div>
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill evening" :style="{ height: getActivityHeight('Evening'), backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Evening</span>
                  <span class="time-range">6PM - 12AM</span>
                  <span class="observation-count">{{ getCurrentSeasonActivity().find(a => a.time_bin === 'Evening')?.count || 0 }} observations</span>
                </div>
              </div>
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill night" :style="{ height: getActivityHeight('Night'), backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Night</span>
                  <span class="time-range">12AM - 6AM</span>
                  <span class="observation-count">{{ getCurrentSeasonActivity().find(a => a.time_bin === 'Night')?.count || 0 }} observations</span>
                </div>
              </div>
            </div>
          </div>

          <div class="star-animals-section">
            <h3 class="section-title">{{ selectedSeason }} Star Animals</h3>
            <div class="star-animals-grid">
                              <div class="star-animal-card" v-for="animal in getTopAnimals()" :key="animal.common_name">
                  <div class="animal-rank">#{{ animal.rank }}</div>
                  <div class="animal-image-container">
                    <img :src="animal.image_url" :alt="animal.common_name" class="animal-image">
                    <div class="observation-badge">{{ animal.total_count }} sightings</div>
                  </div>
                <div class="animal-details">
                  <h4 class="animal-name">{{ animal.common_name }}</h4>
                  <p class="animal-scientific">{{ animal.scientific_name }}</p>
                  <div class="animal-stats">
                    <span class="stat-item">
                      <span class="stat-icon">📍</span>
                      <span class="stat-text">{{ animal.locations }} locations</span>
                    </span>
                    <span class="stat-item">
                      <span class="stat-icon">📸</span>
                      <span class="stat-text">{{ animal.photos }} photos</span>
                    </span>
                  </div>
                  <div class="recent-observation">
                    <span class="obs-label">Latest:</span>
                    <span class="obs-location">{{ animal.lastSeen }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="trend-comparison-section">
            <h3 class="section-title">Season vs Season Comparison</h3>
            <div class="season-comparison">
              <h4 class="trend-title">Species Activity Across Seasons</h4>
              <div class="comparison-bars">
                <div class="comparison-item" v-for="kpi in seasonKPI" :key="kpi.season">
                  <span class="season-name">{{ kpi.season }}</span>
                  <div class="comparison-bar">
                    <div class="comparison-fill" :class="`${kpi.season.toLowerCase()}-fill`" :style="{ width: getSeasonPercentage(kpi.active_species) + '%' }"></div>
                  </div>
                  <span class="season-value">{{ kpi.active_species }} species</span>
                </div>
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
import Button from '../components/common/Button.vue'
import apiService from '../services/api.js'
import TopNavigation from '../components/common/TopNavigation.vue'

export default {
  name: 'SeasonalPage',
  components: {
    SeasonButtonGroup,
    Button,
    TopNavigation
  },
  data() {
  return {
    selectedSeason: 'Spring',
    seasonKPI: [],
    seasonActivity: [],
    topSpecies: {},
    loading: false,
    error: null,
    mobileMenuOpen: false
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
    },
    pageBgStyle() {
      return {
        backgroundImage: `url('${this.currentBackgroundImage}')`
      }
    }
  },
  mounted() {
    this.loadSeasonData()
  },
  methods: {
    async loadSeasonData() {
      this.loading = true
      try {
        const [kpiData, activityData, topSpeciesData] = await Promise.all([
          apiService.getSeasonKPI(),
          apiService.getSeasonActivity(),
          apiService.getTopSpecies(this.selectedSeason)
        ])

        this.seasonKPI = kpiData
        this.seasonActivity = activityData
        this.topSpecies = topSpeciesData
      } catch (error) {
        this.error = error.message
        console.error('Failed to load season data:', error)
      } finally {
        this.loading = false
      }
    },

    async selectSeason(season) {
      this.selectedSeason = season
      await this.loadTopSpecies(season)
    },

    async loadTopSpecies(season) {
      try {
        this.topSpecies = await apiService.getTopSpecies(season)
      } catch (error) {
        console.error('Failed to load top species:', error)
      }
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

    getTopAnimals() {
      return this.topSpecies || []
    },

    getCurrentSeasonKPI() {
      return this.seasonKPI.find(kpi => kpi.season === this.selectedSeason) || {}
    },

    getCurrentSeasonActivity() {
      return this.seasonActivity.filter(activity => activity.season === this.selectedSeason) || []
    },

    getActivityHeight(timeBin) {
      const currentActivity = this.getCurrentSeasonActivity()
      if (!currentActivity.length) return '0%'

      const activity = currentActivity.find(a => a.time_bin === timeBin)
      const count = activity ? activity.count : 0

      if (count === 0) return '0%'

      const maxCount = Math.max(...currentActivity.map(a => a.count))
      if (maxCount === 0) return '0%'

      const percentage = (count / maxCount) * 100
      return percentage + '%'
    },

    getSeasonPercentage(activeSpecies) {
      if (!this.seasonKPI.length) return 0
      const maxSpecies = Math.max(...this.seasonKPI.map(kpi => kpi.active_species))
      return Math.round((activeSpecies / maxSpecies) * 100)
    },

    navigateToHome() {
      this.$router.push('/')
    },

    navigateToWildlife() {
      this.$router.push('/learn-wildlife')
    },

    navigateToSeasonal() {
      // Don't navigate if already on seasonal page
      if this.$route.path === '/seasonal' {
        return;
      }
      this.$router.push('/seasonal')
    },

    navigateToAIChallenge() {
      this.$router.push('/ai-challenge')
    },

    navigateToDailyWildle() {
      this.$router.push('/daily-wildle')
    },

    navigateToConservation() {
      this.$router.push('/conservation')
    },

    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    }
  }
}
</script>

<style scoped>
.seasonal-page {
  width: 100%;
  min-height: 300vh;
  position: relative;
  font-family: var(--font-cartoon);
  background-size: cover;
  background-position: center top;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.hero-section {
  width: 100%;
  height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.15);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.main-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  transition: color 0.3s ease;
  font-family: var(--font-cartoon);
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  transition: color 0.3s ease;
  font-family: var(--font-cartoon);
}

.wildlife-analysis-section {
  position: relative;
  min-height: 200vh;
  overflow: hidden;
}

.section-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.15);
  z-index: 1;
}

.side-background {
  position: absolute;
  top: 0;
  width: 300px;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}

.left-bg {
  left: 0;
}

.right-bg {
  right: 0;
}

.side-background img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.6) contrast(1.2);
}

.analysis-container {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.data-analysis-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  margin: 2rem 0;
}

.analysis-header {
  text-align: center;
  margin-bottom: 4rem;
}

.analysis-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
  font-family: var(--font-cartoon);
}

.analysis-subtitle {
  font-size: 1.1rem;
  color: #666;
  font-family: var(--font-cartoon);
}

.season-kpi-section {
  margin-bottom: 4rem;
}

.kpi-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 2rem;
  max-width: 600px;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.kpi-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

.kpi-icon {
  font-size: 3rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.kpi-number {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.kpi-label {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.kpi-detail {
  font-size: 0.9rem;
  color: #666;
}

.activity-time-chart {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(0, 0, 0, 0.1);
  margin-bottom: 4rem;
  transition: all 0.3s ease;
}

.activity-time-chart:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

.chart-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #333;
}

.time-chart-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.time-period {
  text-align: center;
}

.time-bar {
  height: 200px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  position: relative;
  margin-bottom: 1rem;
  display: flex;
  align-items: end;
}

.bar-fill {
  width: 100%;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.time-label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.time-name {
  font-weight: bold;
  color: #333;
}

.time-range {
  font-size: 0.8rem;
  color: #666;
}

.observation-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: #444;
}

.star-animals-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #333;
}

.star-animals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.star-animal-card {
  background: white;
  padding: 1.25rem;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
}

.star-animal-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.animal-rank {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
  z-index: 2;
}

.animal-image-container {
  position: relative;
  margin-bottom: 1rem;
}

.animal-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 0;
}

.observation-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
}

.animal-details {
  text-align: left;
}

.animal-name {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.animal-scientific {
  font-style: italic;
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.animal-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: #555;
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.recent-observation {
  padding: 0.75rem;
  background: #f0f9ff;
  border: 1px solid #e0f2fe;
  border-radius: 8px;
  font-size: 0.9rem;
  border-left: 4px solid #0ea5e9;
}

.trend-comparison-section {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.trend-comparison-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

.season-comparison {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.trend-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #333;
}

.comparison-bars {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comparison-item {
  display: grid;
  grid-template-columns: 80px 1fr 80px;
  align-items: center;
  gap: 1rem;
}

.season-name {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.comparison-bar {
  height: 24px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.comparison-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 0.3s ease;
}

.spring-fill { background: #22c55e; }
.summer-fill { background: #eab308; }
.autumn-fill { background: #f97316; }
.winter-fill { background: #3b82f6; }

.season-value {
  font-size: 0.85rem;
  color: #666;
  text-align: right;
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
  background: white;
  border-radius: 50%;
  border: 2px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.scroll-arrow:hover {
  background: #f8f9fa;
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
  .data-analysis-wrapper {
    padding: 2rem 1.5rem;
    border-radius: 16px;
    margin: 1rem 0;
  }

  .main-title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .analysis-title {
    font-size: 2rem;
  }

  .time-chart-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .star-animals-grid {
    grid-template-columns: 1fr;
  }

  .kpi-card {
    flex-direction: column;
    text-align: center;
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

  .side-background {
    display: none;
  }
}
</style>
