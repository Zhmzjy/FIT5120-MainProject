<template>
  <div class="trend-chart-container">
    <div class="chart-header">
      <h4 class="chart-title">{{ species?.commonName || 'Animal' }} Story Over Time</h4>
    </div>

    <div class="chart-content">
      <div v-if="loading" class="chart-loading">
        <div class="loading-spinner"></div>
        <p>Loading the story...</p>
      </div>

      <div v-else-if="!chartData || chartData.length === 0" class="no-data">
        <p>No story available for this animal yet</p>
      </div>

      <div v-else class="accordion-timeline">
        <div class="story-intro">
          <h3>{{ getStoryIntro() }}</h3>
        </div>

        <div class="accordion-container">
          <div
            v-for="(point, index) in chartData"
            :key="point.year"
            class="accordion-item"
            :class="{ 'is-expanded': expandedYear === point.year, 'is-first': index === 0, 'is-last': index === chartData.length - 1 }"
          >
            <div
              class="accordion-header"
              @click="toggleYear(point.year)"
            >
              <div class="header-left">
                <img
                  :src="getAnimalImage()"
                  :alt="species?.commonName"
                  class="header-animal-icon"
                />
                <div class="header-info">
                  <span class="header-year">{{ point.year }}</span>
                  <span class="header-count">{{ point.count }} {{ species?.commonName || 'animals' }}</span>
                </div>
              </div>
              <div class="header-right">
                <div v-if="index > 0" class="quick-change" :class="getChangeClass(point, chartData[index - 1])">
                  {{ getChangeText(point, chartData[index - 1]) }}
                </div>
                <div class="expand-icon" :class="{ 'is-open': expandedYear === point.year }">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </div>
              </div>
            </div>

            <transition name="accordion">
              <div v-if="expandedYear === point.year" class="accordion-content">
                <div class="content-grid">
                  <div class="content-main">
                    <div class="story-section">
                      <h4 class="section-title">The Story</h4>
                      <div class="story-text">
                        {{ getStoryText(point, index) }}
                      </div>
                    </div>

                    <div class="visual-section">
                      <div class="count-display">
                        <div class="count-number">{{ point.count }}</div>
                        <div class="count-label">{{ species?.commonName || 'animals' }}</div>
                      </div>

                      <div class="animal-images">
                        <img
                          v-for="n in Math.min(point.count, 8)"
                          :key="n"
                          :src="getAnimalImage()"
                          :alt="species?.commonName"
                          class="small-animal-image"
                          :style="{ animationDelay: (n * 0.05) + 's' }"
                        />
                        <div v-if="point.count > 8" class="more-animals">
                          +{{ point.count - 8 }} more
                        </div>
                      </div>
                    </div>

                    <div v-if="index > 0" class="change-section">
                      <div class="change-card" :class="getChangeClass(point, chartData[index - 1])">
                        <div class="change-header">
                          <span class="change-label">Change from {{ chartData[index - 1].year }}</span>
                        </div>
                        <div class="change-detail">
                          <span class="change-number">{{ getChangeText(point, chartData[index - 1]) }}</span>
                          <span class="change-description">{{ getChangeDescription(point, chartData[index - 1]) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="content-sidebar">
                    <div class="edu-card status-card">
                      <div class="card-icon">
                        <img src="https://img.icons8.com/doodle/30/help.png" alt="help icon" class="icon-image" />
                      </div>
                      <h5 class="card-title">Why This Matters</h5>
                      <p class="card-text">{{ getWhyMatters(point, index) }}</p>
                    </div>

                    <div class="edu-card fact-card">
                      <div class="card-icon">
                        <img src="https://img.icons8.com/dusk/30/goal.png" alt="goal icon" class="icon-image" />
                      </div>
                      <h5 class="card-title">Fun Fact</h5>
                      <p class="card-text">{{ getFunFact(index) }}</p>
                    </div>

                    <div class="edu-card environment-card">
                      <div class="card-icon">
                        <img src="https://img.icons8.com/plasticine/30/hand-planting.png" alt="environment icon" class="icon-image" />
                      </div>
                      <h5 class="card-title">Environment Update</h5>
                      <p class="card-text">{{ getEnvironmentUpdate(point, index) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>

        <div class="story-summary">
          <div class="summary-card">
            <h3>{{ getStoryEnding() }}</h3>
            <div class="summary-stats">
              <div class="summary-stat">
                <span class="stat-label">Years of History</span>
                <span class="stat-value">{{ chartData.length }}</span>
              </div>
              <div class="summary-stat">
                <span class="stat-label">Overall Trend</span>
                <span class="stat-value" :class="'trend-' + trendDirection">{{ getTrendText() }}</span>
              </div>
              <div class="summary-stat">
                <span class="stat-label">Best Year</span>
                <span class="stat-value">{{ peakYear }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrendChart',
  props: {
    title: {
      type: String,
      required: true
    },
    chartData: {
      type: Array,
      default: () => []
    },
    species: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      expandedYear: null
    }
  },
  computed: {
    trendDirection() {
      if (!this.chartData || this.chartData.length < 2) return 'neutral'
      const firstCount = this.chartData[0].count
      const lastCount = this.chartData[this.chartData.length - 1].count
      if (lastCount > firstCount) return 'positive'
      if (lastCount < firstCount) return 'negative'
      return 'neutral'
    },
    peakYear() {
      if (!this.chartData || this.chartData.length === 0) return 'N/A'
      const peak = this.chartData.reduce((max, item) => item.count > max.count ? item : max)
      return peak.year
    }
  },
  methods: {
    toggleYear(year) {
      this.expandedYear = this.expandedYear === year ? null : year
    },
    getAnimalImage() {
      return this.species?.imageUrl || '/images/kangaroo.png'
    },
    getStoryIntro() {
      const animalName = this.species?.commonName || 'our animal friends'
      return `Click on any year to learn more about ${animalName}!`
    },
    getStoryText(point, index) {
      const animalName = this.species?.commonName || 'animals'
      const count = point.count

      if (index === 0) {
        return `In the year ${point.year}, there were ${count} ${animalName} living in their natural habitat. This was the beginning of their recorded story.`
      }

      const prevCount = this.chartData[index - 1].count
      const change = count - prevCount

      if (change > 0) {
        return `Then in ${point.year}, the population grew! ${count} ${animalName} were recorded. This increase shows positive signs for the species, possibly due to conservation efforts or improved habitats.`
      } else if (change < 0) {
        return `In ${point.year}, the population decreased to ${count} ${animalName}. This change reminds us how important it is to protect these animals and their homes.`
      } else {
        return `In ${point.year}, the population remained stable with ${count} ${animalName}. Stability can be a good sign, showing the species is maintaining its numbers.`
      }
    },
    getChangeText(current, previous) {
      const change = current.count - previous.count
      if (change > 0) return `+${change}`
      if (change < 0) return `${change}`
      return 'No change'
    },
    getChangeDescription(current, previous) {
      const change = current.count - previous.count
      const animalName = this.species?.commonName || 'animals'
      if (change > 0) return `More ${animalName} were recorded this year!`
      if (change < 0) return `Fewer ${animalName} were seen this year.`
      return `Population stayed the same.`
    },
    getChangeClass(current, previous) {
      const change = current.count - previous.count
      if (change > 0) return 'positive'
      if (change < 0) return 'negative'
      return 'neutral'
    },
    getWhyMatters(point, index) {
      const animalName = this.species?.commonName || 'animals'
      const reasons = [
        `${animalName} play a vital role in their ecosystem. Their population health indicates the overall environmental health.`,
        `Every ${animalName.toLowerCase()} counts! They help maintain balance in nature by contributing to their food chain.`,
        `${animalName} are indicators of climate health. Changes in their numbers tell us about environmental conditions.`,
        `Protecting ${animalName} means protecting entire ecosystems. They share their habitat with many other species.`,
        `${animalName} populations affect biodiversity. A healthy population means a thriving ecosystem.`
      ]
      return reasons[index % reasons.length]
    },
    getFunFact(index) {
      const animalName = this.species?.commonName?.toLowerCase() || 'animal'

      if (animalName.includes('koala')) {
        const facts = [
          'Koalas sleep 18-22 hours a day! They need lots of rest because eucalyptus leaves are hard to digest.',
          'Koalas have fingerprints just like humans! Even scientists can have trouble telling them apart.',
          'Baby koalas are called joeys and are only 2cm long when born!',
          'Koalas rarely drink water. They get most of their moisture from eucalyptus leaves.'
        ]
        return facts[index % facts.length]
      } else if (animalName.includes('kangaroo')) {
        const facts = [
          'Kangaroos can jump 3 times their own height! That is like you jumping over a house!',
          'Kangaroos cannot walk backwards. They can only move forward!',
          'A group of kangaroos is called a mob. They live together for safety.',
          'Kangaroos can swim! They use their tail to help them move through water.'
        ]
        return facts[index % facts.length]
      } else {
        const facts = [
          `${this.species?.commonName || 'These animals'} are unique to Australia and found nowhere else in the world!`,
          'Australian wildlife has evolved over millions of years in isolation.',
          'Many Australian animals are nocturnal, which means they are active at night.',
          'Australia is home to some of the most unique animals on Earth!'
        ]
        return facts[index % facts.length]
      }
    },
    getEnvironmentUpdate(point, index) {
      const prevPoint = index > 0 ? this.chartData[index - 1] : null
      const change = prevPoint ? point.count - prevPoint.count : 0

      if (change > 0) {
        const updates = [
          'Protected areas are helping wildlife thrive!',
          'Conservation efforts are making a positive difference.',
          'Habitat restoration projects are showing success.',
          'Community support is helping animals recover.'
        ]
        return updates[index % updates.length]
      } else if (change < 0) {
        const updates = [
          'Climate change affects food and water availability for animals.',
          'We need more wildlife reserves and protected areas.',
          'Habitat loss continues to be a challenge for wildlife.',
          'Your actions can help reverse this trend!'
        ]
        return updates[index % updates.length]
      } else {
        return 'Stable populations show that current conservation efforts are working.'
      }
    },
    getStoryEnding() {
      const direction = this.trendDirection
      const animalName = this.species?.commonName || 'these animals'

      if (direction === 'positive') {
        return `Great news! ${animalName} populations are growing over time!`
      } else if (direction === 'negative') {
        return `We need to help protect ${animalName}! Every action counts.`
      } else {
        return `${animalName} populations are staying steady. Let's keep it that way!`
      }
    },
    getTrendText() {
      const direction = this.trendDirection
      if (direction === 'positive') return 'Growing'
      if (direction === 'negative') return 'Declining'
      return 'Stable'
    }
  }
}
</script>

<style scoped>
.trend-chart-container {
  background: linear-gradient(135deg, #fef5e7 0%, #fff9e6 100%);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chart-header {
  text-align: center;
  margin-bottom: 32px;
}

.chart-title {
  margin: 0;
  color: #2d3748;
  font-size: 28px;
  font-weight: 700;
  font-family: 'Comic Sans MS', 'Chalkboard SE', 'Arial Rounded MT Bold', cursive;
}

.chart-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  flex-direction: column;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #ffd700;
  border-top: 4px solid #ff6b6b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.no-data {
  text-align: center;
  padding: 60px;
  color: #718096;
  font-size: 18px;
}

.accordion-timeline {
  position: relative;
}

.story-intro {
  text-align: center;
  margin-bottom: 32px;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.story-intro h3 {
  margin: 0;
  color: #2d3748;
  font-size: 22px;
  font-weight: 600;
  font-family: 'Comic Sans MS', 'Chalkboard SE', cursive;
}

.accordion-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.accordion-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.accordion-item.is-first {
  border: 2px solid #4ecdc4;
}

.accordion-item.is-last {
  border: 2px solid #ff6b6b;
}

.accordion-item.is-expanded {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.accordion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  transition: all 0.2s ease;
}

.accordion-header:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #f8f9fa 100%);
}

.accordion-item.is-expanded .accordion-header {
  background: white;
  color: #2d3748;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-animal-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #ffd700;
  background: white;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.header-year {
  font-size: 20px;
  font-weight: 700;
}

.header-count {
  font-size: 14px;
  opacity: 0.8;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quick-change {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
}

.quick-change.positive {
  background: #d1fae5;
  color: #065f46;
}

.quick-change.negative {
  background: #fee2e2;
  color: #991b1b;
}

.quick-change.neutral {
  background: #e0e7ff;
  color: #1e40af;
}

.expand-icon {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease;
}

.expand-icon.is-open {
  transform: rotate(180deg);
}

.accordion-content {
  padding: 24px;
  background: #fafbfc;
  border-top: 2px solid #e9ecef;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 24px;
}

.content-main {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.story-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #ffd700;
}

.section-title {
  margin: 0 0 12px 0;
  color: #2d3748;
  font-size: 18px;
  font-weight: 700;
}

.story-text {
  font-size: 16px;
  line-height: 1.6;
  color: #4a5568;
  font-family: 'Comic Sans MS', 'Chalkboard SE', cursive;
}

.visual-section {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 20px;
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.count-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: white;
  padding: 20px;
  border-radius: 12px;
  color: #2d3748;
  min-width: 120px;
  border: 2px solid #e2e8f0;
}

.count-number {
  font-size: 48px;
  font-weight: 900;
  line-height: 1;
  color: #2d3748;
}

.count-label {
  font-size: 14px;
  font-weight: 600;
  margin-top: 8px;
  text-align: center;
  color: #2d3748;
}

.animal-images {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  padding: 12px;
  background: #f7fafc;
  border-radius: 8px;
}

.small-animal-image {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid #e2e8f0;
  animation: fadeInScale 0.4s ease backwards;
}

.more-animals {
  padding: 8px 16px;
  background: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
  color: #667eea;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.change-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.change-card {
  padding: 16px;
  border-radius: 8px;
  border: 2px solid;
}

.change-card.positive {
  background: #d1fae5;
  border-color: #10b981;
  color: #065f46;
}

.change-card.negative {
  background: #fee2e2;
  border-color: #ef4444;
  color: #991b1b;
}

.change-card.neutral {
  background: #e0e7ff;
  border-color: #6366f1;
  color: #1e40af;
}

.change-header {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
  opacity: 0.8;
  text-transform: uppercase;
}

.change-detail {
  display: flex;
  align-items: center;
  gap: 12px;
}

.change-number {
  font-size: 28px;
  font-weight: 900;
}

.change-description {
  font-size: 14px;
  font-weight: 600;
  flex: 1;
}

.content-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.edu-card {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.card-title {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 700;
  color: #2d3748;
}

.card-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  color: #4a5568;
}

.status-card {
  border-left: 4px solid #fbbf24;
}

.fact-card {
  border-left: 4px solid #3b82f6;
}

.environment-card {
  border-left: 4px solid #8b5cf6;
}

.story-summary {
  margin-top: 32px;
}

.summary-card {
  background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 50%, #FFECB3 100%);
  color: #2E7D32;
  padding: 32px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(46, 125, 50, 0.15);
  border: 2px solid rgba(129, 199, 132, 0.3);
}

.summary-card h3 {
  margin: 0 0 24px 0;
  font-size: 24px;
  font-weight: 700;
  font-family: 'Comic Sans MS', 'Chalkboard SE', cursive;
  background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 50%, #FFB74D 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.summary-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
  flex-wrap: wrap;
}

.summary-stat {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
  color: #558B2F;
  font-weight: 600;
}

.stat-value {
  font-size: 32px;
  font-weight: 900;
  background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 50%, #FDD835 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-value.trend-positive {
  background: linear-gradient(135deg, #2E7D32 0%, #66BB6A 50%, #81C784 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-value.trend-negative {
  background: linear-gradient(135deg, #D84315 0%, #FF6F00 50%, #FFB74D 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.accordion-enter-active,
.accordion-leave-active {
  transition: all 0.3s ease;
  max-height: 2000px;
  overflow: hidden;
}

.accordion-enter-from,
.accordion-leave-to {
  max-height: 0;
  opacity: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .content-sidebar {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .trend-chart-container {
    padding: 20px;
  }

  .chart-title {
    font-size: 22px;
  }

  .header-animal-icon {
    width: 40px;
    height: 40px;
  }

  .header-year {
    font-size: 18px;
  }

  .header-count {
    font-size: 12px;
  }

  .content-sidebar {
    grid-template-columns: 1fr;
  }

  .summary-stats {
    gap: 24px;
  }

  .stat-value {
    font-size: 24px;
  }
}
</style>
