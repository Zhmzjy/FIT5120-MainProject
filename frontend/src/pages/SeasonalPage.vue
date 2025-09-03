<template>
  <div class="seasonal-page" :style="pageBgStyle">
    <div class="hero-section">
      <div class="hero-overlay"></div>

      <div class="top-nav-bar">
        <div class="nav-content">
          <div class="nav-left">
            <h3 class="nav-title">Wildlife Academy</h3>
          </div>
          <div class="nav-right">
            <button class="nav-btn" @click="navigateToHome">Home</button>
            <button class="nav-btn" @click="navigateToWildlife">Learn Wildlife</button>
          </div>
        </div>
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
            <h3 class="section-title">Seasonal Trends & Comparison</h3>
            <div class="trend-container">
              <div class="monthly-trends-chart">
                <h4 class="trend-title">Monthly Species Activity Trends</h4>
                <div v-if="getTopTrendAnimals().length > 0" class="species-trends-chart">
                  <svg viewBox="0 0 900 400" class="trends-chart-svg">
                    <g class="grid-lines">
                      <line v-for="i in 5" :key="`grid-${i}`" x1="80" :x2="820" :y1="80 + (i - 1) * 60" :y2="80 + (i - 1) * 60" stroke="#e5e7eb" stroke-width="1"/>
                      <line v-for="i in 12" :key="`month-${i}`" :x1="80 + (i - 1) * 62" :x2="80 + (i - 1) * 62" y1="80" y2="320" stroke="#e5e7eb" stroke-width="1"/>
                    </g>

                    <g v-for="(animal, animalIndex) in getTopTrendAnimals()" :key="animal.taxon_id">
                      <polyline
                        :points="getMonthlyTrendPoints(animal.trends)"
                        :stroke="getTrendColor(animalIndex)"
                        stroke-width="3"
                        fill="none"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />

                      <g v-for="(point, pointIndex) in getMonthlyDataPoints(animal.trends)" :key="`${animal.taxon_id}-${pointIndex}`">
                        <circle
                          :cx="point.x"
                          :cy="point.y"
                          r="4"
                          :fill="getTrendColor(animalIndex)"
                          stroke="white"
                          stroke-width="2"
                        />
                      </g>
                    </g>

                    <g class="axis-labels">
                      <text v-for="(month, index) in monthLabels" :key="month" :x="80 + index * 62" y="350" text-anchor="middle" class="month-label" font-size="12" fill="#666">
                        {{ month }}
                      </text>
                    </g>

                    <g class="y-axis-labels">
                      <text v-for="i in 5" :key="`y-${i}`" x="70" :y="85 + (4 - i) * 60" text-anchor="end" class="count-label" font-size="11" fill="#666">
                        {{ getYAxisLabel(i - 1) }}
                      </text>
                    </g>
                  </svg>

                  <div class="trends-legend">
                    <div v-for="(animal, index) in getTopTrendAnimals()" :key="animal.taxon_id" class="legend-item">
                      <div class="legend-color" :style="{ backgroundColor: getTrendColor(index) }"></div>
                      <img :src="animal.image_url" :alt="animal.common_name" class="legend-icon">
                      <span class="legend-name">{{ animal.common_name }}</span>
                    </div>
                  </div>
                </div>
                <div v-else class="no-data-message">
                  <p>Loading trend data...</p>
                </div>
              </div>
              <div class="season-comparison">
                <h4 class="trend-title">Season vs Season</h4>
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
import apiService from '../services/api.js'

export default {
  name: 'SeasonalPage',
  components: {
    SeasonButtonGroup
  },
  data() {
  return {
    selectedSeason: 'Spring',
    seasonKPI: [],
    seasonActivity: [],
    topSpecies: {},
    monthlyTrends: [],
    loading: false,
    error: null
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
        await this.loadMonthlyTrends()
      } catch (error) {
        this.error = error.message
        console.error('Failed to load season data:', error)
      } finally {
        this.loading = false
      }
    },

    async loadMonthlyTrends() {
      try {
        const topAnimals = this.getTopAnimals().slice(0, 5)
        console.log('Top animals for trends:', topAnimals)

        if (!topAnimals || topAnimals.length === 0) {
          console.log('No top animals found')
          this.monthlyTrends = []
          return
        }

        const animalTaxonMapping = {
          'Australian Magpie': 8575,
          'Koala': 42983,
          'Laughing Kookaburra': 2413,
          'Waxlip Orchid': null,
          'Superb Fairywren': 12065,
          'Australian Wood Duck': null,
          'Rainbow Lorikeet': 980095,
          'Western Honey Bee': 47219,
          'Australian Water Dragon': null,
          'Australian Painted Lady': null
        }

        const animalsWithTaxonId = topAnimals.map(animal => ({
          ...animal,
          taxon_id: animalTaxonMapping[animal.common_name] || null
        })).filter(animal => animal.taxon_id !== null)

        console.log('Animals with taxon_id mapping:', animalsWithTaxonId)

        if (animalsWithTaxonId.length === 0) {
          console.log('No animals with valid taxon_id found')
          this.monthlyTrends = []
          return
        }

        const trendsPromises = animalsWithTaxonId.map(animal => {
          console.log(`Loading trends for ${animal.common_name} (taxon_id: ${animal.taxon_id})`)
          return apiService.getSpeciesTrend(animal.taxon_id)
        })

        const trendsResults = await Promise.all(trendsPromises)
        console.log('Trends results:', trendsResults)

        this.monthlyTrends = animalsWithTaxonId.map((animal, index) => ({
          ...animal,
          trends: trendsResults[index] || []
        }))

        console.log('Final monthly trends:', this.monthlyTrends)
      } catch (error) {
        console.error('Failed to load monthly trends:', error)
        this.monthlyTrends = []
      }
    },

    async selectSeason(season) {
      this.selectedSeason = season
      await this.loadTopSpecies(season)
      await this.loadMonthlyTrends()
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

    getSeasonAnimals() {
      return this.animalData[this.selectedSeason] || []
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

    getTopAnimalsChart() {
      const animals = this.getTopAnimals()
      return Array.isArray(animals) ? animals.slice(0, 10) : []
    },

    getSpeciesBarWidth(count) {
      const animals = this.getTopAnimalsChart()
      if (!animals.length) return 0
      const maxCount = Math.max(...animals.map(a => a.total_count))
      return maxCount > 0 ? Math.round((count / maxCount) * 100) : 0
    },

    getLineChartPoints() {
      const data = this.getTopAnimalsChart()
      const maxCount = Math.max(...data.map(animal => animal.total_count))
      const scaleX = 700 / (data.length - 1 || 1)
      const scaleY = 250 / maxCount

      return data.map((animal, index) => {
        const x = index * scaleX + 70
        const y = 250 - animal.total_count * scaleY
        return `${x},${y}`
      }).join(' ')
    },

    getAreaChartPoints() {
      const data = this.getTopAnimalsChart()
      const maxCount = Math.max(...data.map(animal => animal.total_count))
      const scaleX = 700 / (data.length - 1 || 1)
      const scaleY = 250 / maxCount

      const points = data.map((animal, index) => {
        const x = index * scaleX + 70
        const y = 250 - animal.total_count * scaleY
        return `${x},${y}`
      })

      return `${points[0]} ${points.join(' ')} ${points[points.length - 1]}`
    },

    getChartDataPoints() {
      const data = this.getTopAnimalsChart()
      const maxCount = Math.max(...data.map(animal => animal.total_count))
      const scaleX = 700 / (data.length - 1 || 1)
      const scaleY = 250 / maxCount

      return data.map((animal, index) => {
        const x = index * scaleX + 70
        const y = 250 - animal.total_count * scaleY
        return { x, y, count: animal.total_count }
      })
    },

    navigateToHome() {
      this.$router.push('/')
    },

    navigateToWildlife() {
      this.$router.push('/learn-wildlife')
    },

    getTopTrendAnimals() {
      return this.monthlyTrends || []
    },

    getTrendColor(index) {
      const colors = ['#22c55e', '#3b82f6', '#f97316', '#e11d48', '#8b5cf6']
      return colors[index % colors.length]
    },

    getMonthlyTrendPoints(trends) {
      if (!trends || !trends.length) return ''

      const months = Array.from({length: 12}, (_, i) => i + 1)
      const maxCount = this.getMaxTrendCount()

      return months.map((month, index) => {
        const trendData = trends.find(t => t.month === month)
        const count = trendData ? trendData.total_count : 0
        const x = 80 + index * 62
        const y = 320 - (count / maxCount) * 240
        return `${x},${y}`
      }).join(' ')
    },

    getMonthlyDataPoints(trends, animalIndex) {
      if (!trends || !trends.length) return []

      const months = Array.from({length: 12}, (_, i) => i + 1)
      const maxCount = this.getMaxTrendCount()

      return months.map((month, index) => {
        const trendData = trends.find(t => t.month === month)
        const count = trendData ? trendData.total_count : 0
        const x = 80 + index * 62
        const y = 320 - (count / maxCount) * 240
        return { x, y, count }
      })
    },

    getMaxTrendCount() {
      let maxCount = 0
      this.monthlyTrends.forEach(animal => {
        if (animal.trends) {
          animal.trends.forEach(trend => {
            if (trend.total_count > maxCount) {
              maxCount = trend.total_count
            }
          })
        }
      })
      return maxCount || 1
    },

    getYAxisLabel(index) {
      const maxCount = this.getMaxTrendCount()
      return Math.round((maxCount / 4) * index)
    },

    get monthLabels() {
      return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
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
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.30);
  z-index: 1;
}


.top-nav-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 10;
  background: transparent;
  padding: 1rem 0;
}

.nav-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
}

.nav-title {
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
  transition: all var(--transition-normal);
}

.nav-title:hover {
  background: transparent;
  transform: scale(1.02);
  text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.9), 2px 2px 4px rgba(0, 0, 0, 1);
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-3px); }
}

.nav-right {
  display: flex;
  align-items: center;
}

.nav-left {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: var(--font-cartoon);
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  padding: 6rem 2rem 2rem 2rem;
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
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  transition: color 0.3s ease;
  font-family: var(--font-cartoon);
}

.wildlife-analysis-section {
  position: relative;
  min-height: 200vh;
  overflow: hidden;
}

.wildlife-analysis-section::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.30);
  z-index: 1;
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
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin: 2rem 0;
}

@media (max-width: 768px) {
  .data-analysis-wrapper {
    padding: 2rem 1.5rem;
    border-radius: 16px;
    margin: 1rem 0;
  }
}

@media (max-width: 480px) {
  .data-analysis-wrapper {
    padding: 1.5rem 1rem;
    border-radius: 12px;
  }
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
  color: #64748b;
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
  display: flex;
  align-items: center;
  gap: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.kpi-icon {
  font-size: 3rem;
  padding: 1rem;
  background: #f1f5f9;
  border-radius: 12px;
}

.kpi-number {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.kpi-label {
  font-size: 1.2rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.kpi-detail {
  color: #22c55e;
  font-size: 0.9rem;
}

.activity-time-chart {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-bottom: 4rem;
}

.chart-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #1e293b;
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
  background: #f1f5f9;
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
  color: #1e293b;
}

.time-range {
  font-size: 0.8rem;
  color: #64748b;
}

.observation-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: #059669;
}

.star-animals-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
  color: #1e293b;
}

.star-animals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.star-animal-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.3s ease;
}

.star-animal-card:hover {
  transform: translateY(-5px);
}

.animal-rank {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #fbbf24;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.animal-image-container {
  position: relative;
  margin-bottom: 1rem;
}

.animal-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 0.5rem;
}

.observation-badge {
  background: #059669;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  display: inline-block;
}

.animal-name {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #1e293b;
}

.animal-scientific {
  font-style: italic;
  color: #64748b;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.animal-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  color: #64748b;
}

.recent-observation {
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  font-size: 0.9rem;
}

.obs-label {
  font-weight: 600;
  color: #374151;
}

.obs-location {
  color: #059669;
}

.trend-comparison-section {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.trend-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

.trend-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

.trend-chart {
  padding: 1rem;
}

.trend-line-chart {
  position: relative;
}

.chart-svg {
  width: 100%;
  height: 200px;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  font-size: 0.8rem;
  color: #64748b;
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
  color: #374151;
  font-size: 0.9rem;
}

.comparison-bar {
  height: 24px;
  background: #f1f5f9;
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
  color: #64748b;
  text-align: right;
}

.top-species-chart {
  padding: 1rem;
}

.species-chart-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.species-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.species-bar:hover {
  background: #f1f5f9;
  transform: translateX(5px);
}

.species-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 200px;
  flex-shrink: 0;
}

.species-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e2e8f0;
}

.species-name {
  font-weight: 500;
  color: #1e293b;
  font-size: 0.9rem;
}

.bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.species-bar-fill {
  height: 20px;
  border-radius: 10px;
  transition: all 0.3s ease;
  min-width: 20px;
}

.species-count {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
  min-width: 50px;
  text-align: right;
}

.species-line-chart {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  margin-top: 1rem;
}

.line-chart-svg {
  width: 100%;
  height: 300px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-label {
  font-family: var(--font-cartoon);
}

.axis-label {
  font-family: var(--font-cartoon);
}

.monthly-trends-chart {
  padding: 1rem;
}

.species-trends-chart {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 12px;
  margin-top: 1rem;
}

.trends-chart-svg {
  width: 100%;
  height: 400px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.grid-lines line {
  opacity: 0.3;
}

.month-label {
  font-family: var(--font-cartoon);
}

.count-label {
  font-family: var(--font-cartoon);
}

.trends-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #e5e7eb;
}

.legend-name {
  color: #374151;
  font-weight: 500;
}

.no-data-message {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-style: italic;
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

  .time-chart-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .star-animals-grid {
    grid-template-columns: 1fr;
  }

  .trend-container {
    grid-template-columns: 1fr;
    gap: 2rem;
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
}
</style>
