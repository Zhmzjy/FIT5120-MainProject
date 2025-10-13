<template>
  <div class="yearly-stats-card">
    <div class="card-header">
      <h3 class="card-title">{{ title }}</h3>
      <div class="year-badge">{{ year }}</div>
    </div>

    <div class="stats-summary">
      <div class="summary-item">
        <span class="summary-label">Total Species:</span>
        <span class="summary-value">{{ totalSpecies }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Total Observations:</span>
        <span class="summary-value">{{ totalObservations.toLocaleString() }}</span>
      </div>
    </div>

    <div class="species-list">
      <div
        v-for="(species, index) in speciesList"
        :key="species.taxonId"
        class="species-item"
        @click="$emit('species-selected', species)"
      >
        <div class="species-rank">#{{ index + 1 }}</div>
        <div class="species-image">
          <img
            :src="species.imageUrl"
            :alt="species.commonName"
            @error="handleImageError"
            @load="handleImageLoad"
          />
        </div>
        <div class="species-info">
          <h4 class="species-name">{{ species.commonName }}</h4>
          <p class="species-scientific">{{ species.scientificName }}</p>
          <div class="species-stats">
            <span class="observation-count">{{ species.count.toLocaleString() }} observations</span>
            <div v-if="species.trend" class="trend-indicator" :class="species.trend.direction">
              <span class="trend-arrow">{{ species.trend.direction === 'up' ? '↗' : '↘' }}</span>
              <span class="trend-percent">{{ species.trend.percentage }}%</span>
            </div>
          </div>
        </div>
        <div class="view-trend-btn">
          <Button type="secondary" size="small" @click.stop="$emit('view-trend', species)">
            View Trend
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'YearlyStatsCard',
  components: {
    Button
  },
  props: {
    title: {
      type: String,
      required: true
    },
    year: {
      type: Number,
      required: true
    },
    speciesList: {
      type: Array,
      default: () => []
    },
    cardType: {
      type: String,
      default: 'most-common',
      validator: value => ['most-common', 'least-common'].includes(value)
    }
  },
  emits: ['species-selected', 'view-trend'],
  computed: {
    totalSpecies() {
      return this.speciesList.length
    },
    totalObservations() {
      return this.speciesList.reduce((sum, species) => sum + species.count, 0)
    }
  },
  methods: {
    handleImageError(event) {
      const animalName = event.target.alt.toLowerCase()
      if (animalName.includes('koala')) {
        event.target.style.display = 'none'
        event.target.parentElement.innerHTML = '<div class="animal-emoji">🐨</div>'
      } else if (animalName.includes('magpie')) {
        event.target.style.display = 'none'
        event.target.parentElement.innerHTML = '<div class="animal-emoji">🐦‍⬛</div>'
      } else if (animalName.includes('lorikeet')) {
        event.target.style.display = 'none'
        event.target.parentElement.innerHTML = '<div class="animal-emoji">🦜</div>'
      } else if (animalName.includes('bilby')) {
        event.target.style.display = 'none'
        event.target.parentElement.innerHTML = '<div class="animal-emoji">🐭</div>'
      } else if (animalName.includes('tasmanian devil')) {
        event.target.style.display = 'none'
        event.target.parentElement.innerHTML = '<div class="animal-emoji">😈</div>'
      } else {
        event.target.style.display = 'none'
        event.target.parentElement.innerHTML = '<div class="animal-emoji">🐾</div>'
      }
    },
    handleImageLoad(event) {
      console.log('Image loaded successfully:', event.target.alt)
    }
  }
}
</script>

<style scoped>
.yearly-stats-card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  height: fit-content;
  border: 2px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #A2E2A2, #DFF8DF);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid #EAF6EA;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1e293b;
  margin: 0;
}

.year-badge {
  background: white;
  color: #1e293b;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-pill);
  font-size: 0.875rem;
  font-weight: bold;
  border: 2px solid #77BFA3;
}

.stats-summary {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: white;
  border-radius: var(--border-radius-md);
  border: 1px solid #A2E2A2;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.summary-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.summary-value {
  font-size: 1.125rem;
  font-weight: bold;
  color: #1e293b;
}

.species-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  max-height: 500px;
  overflow-y: auto;
}

.species-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border: 1px solid #A2E2A2;
  border-radius: var(--border-radius-md);
  background: white;
}


.species-rank {
  font-size: 1.25rem;
  font-weight: bold;
  color: #77BFA3;
  min-width: 30px;
}

.species-image {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  border: 2px solid #A2E2A2;
}

.species-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.species-info {
  flex: 1;
  min-width: 0;
}

.species-name {
  font-size: 1rem;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 var(--spacing-xs) 0;
}

.species-scientific {
  font-size: 0.875rem;
  color: #64748b;
  font-style: italic;
  margin: 0 0 var(--spacing-sm) 0;
}

.species-stats {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.observation-count {
  font-size: 0.875rem;
  color: #475569;
  font-weight: 500;
}

.trend-indicator {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 0.75rem;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: var(--border-radius-sm);
}

.trend-indicator.up {
  background: #EAF6EA;
  color: #77BFA3;
}

.trend-indicator.down {
  background: #FFE8CC;
  color: #CC8800;
}

.trend-arrow {
  font-size: 0.875rem;
}

.view-trend-btn {
  flex-shrink: 0;
}

.animal-emoji {
  font-size: 2rem;
  line-height: 1;
  display: inline-block;
  width: 80px;
  height: 80px;
  text-align: center;
  border-radius: 50%;
  background: #EAF6EA;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .species-item {
    flex-wrap: wrap;
  }

  .view-trend-btn {
    width: 100%;
    margin-top: var(--spacing-sm);
  }
}
</style>
