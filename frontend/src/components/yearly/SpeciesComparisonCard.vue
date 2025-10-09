<template>
  <div class="species-comparison-card">
    <div class="comparison-header">
      <h3>{{ year1 }} vs {{ year2 }} Comparison</h3>
      <div class="year-badges">
        <span class="year-badge year1">{{ year1 }}</span>
        <span class="vs-text">VS</span>
        <span class="year-badge year2">{{ year2 }}</span>
      </div>
    </div>

    <div class="comparison-stats">
      <div class="stat-comparison">
        <div class="stat-item">
          <span class="stat-label">Total Species</span>
          <div class="stat-values">
            <span class="value year1-value">{{ data.year1.totalSpecies }}</span>
            <span class="change-indicator" :class="getChangeClass(data.year1.totalSpecies, data.year2.totalSpecies)">
              {{ getChangeText(data.year1.totalSpecies, data.year2.totalSpecies) }}
            </span>
            <span class="value year2-value">{{ data.year2.totalSpecies }}</span>
          </div>
        </div>

        <div class="stat-item">
          <span class="stat-label">Total Observations</span>
          <div class="stat-values">
            <span class="value year1-value">{{ data.year1.totalObservations.toLocaleString() }}</span>
            <span class="change-indicator" :class="getChangeClass(data.year1.totalObservations, data.year2.totalObservations)">
              {{ getChangeText(data.year1.totalObservations, data.year2.totalObservations) }}
            </span>
            <span class="value year2-value">{{ data.year2.totalObservations.toLocaleString() }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="species-comparison-grid">
      <div class="comparison-section most-common">
        <h4>Most Common Species</h4>
        <div class="species-comparison-list">
          <div
            v-for="(comparison, index) in mostCommonComparisons"
            :key="index"
            class="species-comparison-item"
          >
            <div class="species-rank">#{{ index + 1 }}</div>
            <div class="species-comparison-content">
              <div class="year-species year1-species">
                <div class="species-info">
                  <img :src="comparison.year1.imageUrl" :alt="comparison.year1.commonName" class="species-image">
                  <div class="species-details">
                    <span class="species-name">{{ comparison.year1.commonName }}</span>
                    <span class="species-count">{{ comparison.year1.count.toLocaleString() }}</span>
                  </div>
                </div>
              </div>

              <div class="comparison-arrow">
                <span v-if="comparison.year1.commonName === comparison.year2.commonName">→</span>
                <span v-else class="different-species">≠</span>
              </div>

              <div class="year-species year2-species">
                <div class="species-info">
                  <img :src="comparison.year2.imageUrl" :alt="comparison.year2.commonName" class="species-image">
                  <div class="species-details">
                    <span class="species-name">{{ comparison.year2.commonName }}</span>
                    <span class="species-count">{{ comparison.year2.count.toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="comparison-section least-common">
        <h4>Least Common Species</h4>
        <div class="species-comparison-list">
          <div
            v-for="(comparison, index) in leastCommonComparisons"
            :key="index"
            class="species-comparison-item"
          >
            <div class="species-rank">#{{ index + 1 }}</div>
            <div class="species-comparison-content">
              <div class="year-species year1-species">
                <div class="species-info">
                  <img :src="comparison.year1.imageUrl" :alt="comparison.year1.commonName" class="species-image">
                  <div class="species-details">
                    <span class="species-name">{{ comparison.year1.commonName }}</span>
                    <span class="species-count">{{ comparison.year1.count.toLocaleString() }}</span>
                  </div>
                </div>
              </div>

              <div class="comparison-arrow">
                <span v-if="comparison.year1.commonName === comparison.year2.commonName">→</span>
                <span v-else class="different-species">≠</span>
              </div>

              <div class="year-species year2-species">
                <div class="species-info">
                  <img :src="comparison.year2.imageUrl" :alt="comparison.year2.commonName" class="species-image">
                  <div class="species-details">
                    <span class="species-name">{{ comparison.year2.commonName }}</span>
                    <span class="species-count">{{ comparison.year2.count.toLocaleString() }}</span>
                  </div>
                </div>
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
  name: 'SpeciesComparisonCard',
  props: {
    year1: {
      type: Number,
      required: true
    },
    year2: {
      type: Number,
      required: true
    },
    data: {
      type: Object,
      required: true
    }
  },
  computed: {
    mostCommonComparisons() {
      const maxLength = Math.max(
        this.data.year1.mostCommon?.length || 0,
        this.data.year2.mostCommon?.length || 0
      )

      const comparisons = []
      for (let i = 0; i < Math.min(maxLength, 5); i++) {
        comparisons.push({
          year1: this.data.year1.mostCommon?.[i] || { commonName: 'N/A', count: 0, imageUrl: '' },
          year2: this.data.year2.mostCommon?.[i] || { commonName: 'N/A', count: 0, imageUrl: '' }
        })
      }
      return comparisons
    },
    leastCommonComparisons() {
      const maxLength = Math.max(
        this.data.year1.leastCommon?.length || 0,
        this.data.year2.leastCommon?.length || 0
      )

      const comparisons = []
      for (let i = 0; i < Math.min(maxLength, 5); i++) {
        comparisons.push({
          year1: this.data.year1.leastCommon?.[i] || { commonName: 'N/A', count: 0, imageUrl: '' },
          year2: this.data.year2.leastCommon?.[i] || { commonName: 'N/A', count: 0, imageUrl: '' }
        })
      }
      return comparisons
    }
  },
  methods: {
    getChangeClass(val1, val2) {
      if (val1 > val2) return 'decrease'
      if (val1 < val2) return 'increase'
      return 'no-change'
    },
    getChangeText(val1, val2) {
      const diff = val2 - val1
      const percentage = Math.abs(Math.round((diff / val1) * 100))

      if (diff > 0) return `+${percentage}%`
      if (diff < 0) return `-${percentage}%`
      return '0%'
    }
  }
}
</script>

<style scoped>
.species-comparison-card {
  background: white;
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.comparison-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.comparison-header h3 {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 var(--spacing-md) 0;
}

.year-badges {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
}

.year-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-pill);
  font-size: 0.875rem;
  font-weight: bold;
}

.year-badge.year1 {
  background: #3b82f6;
  color: white;
}

.year-badge.year2 {
  background: #10b981;
  color: white;
}

.vs-text {
  font-size: 1.125rem;
  font-weight: bold;
  color: #64748b;
}

.comparison-stats {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: #f8fafc;
  border-radius: var(--border-radius-md);
}

.stat-comparison {
  display: flex;
  gap: var(--spacing-xl);
  justify-content: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.stat-values {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.value {
  font-size: 1.125rem;
  font-weight: bold;
}

.year1-value {
  color: #3b82f6;
}

.year2-value {
  color: #10b981;
}

.change-indicator {
  padding: 2px 6px;
  border-radius: var(--border-radius-sm);
  font-size: 0.75rem;
  font-weight: bold;
}

.change-indicator.increase {
  background: #dcfce7;
  color: #166534;
}

.change-indicator.decrease {
  background: #fef2f2;
  color: #dc2626;
}

.change-indicator.no-change {
  background: #f1f5f9;
  color: #64748b;
}

.species-comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
}

.comparison-section h4 {
  font-size: 1.125rem;
  font-weight: bold;
  color: #1e293b;
  margin: 0 0 var(--spacing-lg) 0;
  text-align: center;
}

.most-common h4 {
  color: #22c55e;
}

.least-common h4 {
  color: #f97316;
}

.species-comparison-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.species-comparison-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border: 1px solid #e2e8f0;
  border-radius: var(--border-radius-md);
}

.species-rank {
  font-size: 0.875rem;
  font-weight: bold;
  color: #64748b;
  min-width: 20px;
}

.species-comparison-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
}

.year-species {
  flex: 1;
}

.species-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.species-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.species-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.species-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1e293b;
}

.species-count {
  font-size: 0.75rem;
  color: #64748b;
}

.comparison-arrow {
  font-size: 1.25rem;
  color: #64748b;
  min-width: 20px;
  text-align: center;
}

.different-species {
  color: #f97316;
  font-weight: bold;
}

@media (max-width: 768px) {
  .species-comparison-grid {
    grid-template-columns: 1fr;
  }

  .stat-comparison {
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .species-comparison-content {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .comparison-arrow {
    transform: rotate(90deg);
  }
}
</style>
