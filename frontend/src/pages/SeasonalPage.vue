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
          <div class="season-kpi-section">
            <div class="kpi-card main-kpi">
              <div class="kpi-icon">🐨</div>
              <div class="kpi-content">
                <div class="kpi-number" :style="titleStyle">245</div>
                <div class="kpi-label">Active Species This Season</div>
                <div class="kpi-detail">+12% from last season</div>
              </div>
            </div>
          </div>

          <div class="activity-time-chart">
            <h3 class="chart-title">Activity Time Distribution</h3>
            <div class="time-chart-container">
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill morning" :style="{ height: '65%', backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Morning</span>
                  <span class="time-range">6AM - 12PM</span>
                  <span class="observation-count">1,234 observations</span>
                </div>
              </div>
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill afternoon" :style="{ height: '85%', backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Afternoon</span>
                  <span class="time-range">12PM - 6PM</span>
                  <span class="observation-count">1,678 observations</span>
                </div>
              </div>
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill evening" :style="{ height: '70%', backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Evening</span>
                  <span class="time-range">6PM - 12AM</span>
                  <span class="observation-count">1,456 observations</span>
                </div>
              </div>
              <div class="time-period">
                <div class="time-bar">
                  <div class="bar-fill night" :style="{ height: '45%', backgroundColor: getSeasonColor() }"></div>
                </div>
                <div class="time-label">
                  <span class="time-name">Night</span>
                  <span class="time-range">12AM - 6AM</span>
                  <span class="observation-count">892 observations</span>
                </div>
              </div>
            </div>
          </div>

          <div class="star-animals-section">
            <h3 class="section-title">{{ selectedSeason }} Star Animals</h3>
            <div class="star-animals-grid">
              <div class="star-animal-card" v-for="animal in getTopAnimals()" :key="animal.name">
                <div class="animal-rank">#{{ animal.rank }}</div>
                <div class="animal-image-container">
                  <img :src="animal.image" :alt="animal.name" class="animal-image">
                  <div class="observation-badge">{{ animal.observations }} sightings</div>
                </div>
                <div class="animal-details">
                  <h4 class="animal-name">{{ animal.name }}</h4>
                  <p class="animal-scientific">{{ animal.scientific }}</p>
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
              <div class="monthly-trend">
                <h4 class="trend-title">Monthly Species Activity</h4>
                <div class="trend-chart">
                  <div class="trend-line-chart">
                    <svg viewBox="0 0 400 200" class="chart-svg">
                      <polyline
                        points="50,150 100,120 150,100 200,80 250,90 300,110 350,130"
                        :stroke="getSeasonColor()"
                        stroke-width="3"
                        fill="none"
                      />
                      <circle cx="50" cy="150" r="4" :fill="getSeasonColor()"/>
                      <circle cx="100" cy="120" r="4" :fill="getSeasonColor()"/>
                      <circle cx="150" cy="100" r="4" :fill="getSeasonColor()"/>
                      <circle cx="200" cy="80" r="4" :fill="getSeasonColor()"/>
                      <circle cx="250" cy="90" r="4" :fill="getSeasonColor()"/>
                      <circle cx="300" cy="110" r="4" :fill="getSeasonColor()"/>
                      <circle cx="350" cy="130" r="4" :fill="getSeasonColor()"/>
                    </svg>
                    <div class="chart-labels">
                      <span>Sep</span>
                      <span>Oct</span>
                      <span>Nov</span>
                      <span>Dec</span>
                      <span>Jan</span>
                      <span>Feb</span>
                      <span>Mar</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="season-comparison">
                <h4 class="trend-title">Season vs Season</h4>
                <div class="comparison-bars">
                  <div class="comparison-item">
                    <span class="season-name">Spring</span>
                    <div class="comparison-bar">
                      <div class="comparison-fill spring-fill" style="width: 85%"></div>
                    </div>
                    <span class="season-value">245 species</span>
                  </div>
                  <div class="comparison-item">
                    <span class="season-name">Summer</span>
                    <div class="comparison-bar">
                      <div class="comparison-fill summer-fill" style="width: 70%"></div>
                    </div>
                    <span class="season-value">198 species</span>
                  </div>
                  <div class="comparison-item">
                    <span class="season-name">Autumn</span>
                    <div class="comparison-bar">
                      <div class="comparison-fill autumn-fill" style="width: 95%"></div>
                    </div>
                    <span class="season-value">287 species</span>
                  </div>
                  <div class="comparison-item">
                    <span class="season-name">Winter</span>
                    <div class="comparison-bar">
                      <div class="comparison-fill winter-fill" style="width: 55%"></div>
                    </div>
                    <span class="season-value">156 species</span>
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

export default {
  name: 'SeasonalPage',
  components: {
    SeasonButtonGroup
  },
  data() {
    return {
      selectedSeason: 'Spring',
      mockData: {
        Spring: [
          { rank: 1, name: 'Kangaroo', scientific: 'Osphranter rufus', observations: 1256, locations: 45, photos: 234, lastSeen: 'Blue Mountains', image: '/images/kangaroo.png' },
          { rank: 2, name: 'Koala', scientific: 'Phascolarctos cinereus', observations: 892, locations: 32, photos: 156, lastSeen: 'Grampians NP', image: '/images/koala.png' },
          { rank: 3, name: 'Echidna', scientific: 'Tachyglossus aculeatus', observations: 567, locations: 28, photos: 89, lastSeen: 'Royal NP', image: '/images/kangaroo.png' }
        ],
        Summer: [
          { rank: 1, name: 'Platypus', scientific: 'Ornithorhynchus anatinus', observations: 1456, locations: 22, photos: 178, lastSeen: 'Yarra River', image: '/images/koala.png' },
          { rank: 2, name: 'Kookaburra', scientific: 'Dacelo novaeguineae', observations: 1123, locations: 67, photos: 289, lastSeen: 'Kakadu NP', image: '/images/kangaroo.png' },
          { rank: 3, name: 'Dingo', scientific: 'Canis dingo', observations: 678, locations: 34, photos: 123, lastSeen: 'Fraser Island', image: '/images/koala.png' }
        ],
        Autumn: [
          { rank: 1, name: 'Possum', scientific: 'Trichosurus vulpecula', observations: 1567, locations: 89, photos: 345, lastSeen: 'Sydney Harbour', image: '/images/kangaroo.png' },
          { rank: 2, name: 'Wallaby', scientific: 'Macropus rufogriseus', observations: 1234, locations: 56, photos: 234, lastSeen: 'Kangaroo Island', image: '/images/koala.png' },
          { rank: 3, name: 'Bandicoot', scientific: 'Perameles nasuta', observations: 890, locations: 43, photos: 167, lastSeen: 'Daintree', image: '/images/kangaroo.png' }
        ],
        Winter: [
          { rank: 1, name: 'Tasmanian Devil', scientific: 'Sarcophilus harrisii', observations: 678, locations: 12, photos: 89, lastSeen: 'Tasmania', image: '/images/koala.png' },
          { rank: 2, name: 'Sugar Glider', scientific: 'Petaurus breviceps', observations: 567, locations: 34, photos: 123, lastSeen: 'Lamington NP', image: '/images/kangaroo.png' },
          { rank: 3, name: 'Numbat', scientific: 'Myrmecobius fasciatus', observations: 234, locations: 8, photos: 45, lastSeen: 'WA Wheatbelt', image: '/images/koala.png' }
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
    },
    getTopAnimals() {
      return this.mockData[this.selectedSeason] || []
    }
  }
}
</script>

<style scoped>
.seasonal-page {
  width: 100%;
  min-height: 300vh;
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
  min-height: 200vh;
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
  margin-bottom: 4rem;
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
