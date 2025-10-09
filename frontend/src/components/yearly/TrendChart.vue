<template>
  <div class="trend-chart-container">
    <div class="chart-header">
      <h4 class="chart-title">{{ title }}</h4>
    </div>

    <div class="chart-content">
      <div v-if="loading" class="chart-loading">
        <div class="loading-spinner"></div>
        <p>Loading trend data...</p>
      </div>

      <div v-else-if="!chartData || chartData.length === 0" class="no-data">
        <p>No trend data available for this species</p>
      </div>

      <div v-else class="chart-wrapper">
        <div class="debug-info" style="margin-bottom: 10px; font-size: 12px; color: #666;">
          Data points: {{ chartData.length }} | Canvas ready: {{ canvasReady }}
        </div>
        <canvas ref="chartCanvas" :width="chartWidth" :height="chartHeight" style="border: 1px solid #ddd;"></canvas>

        <div class="trend-summary">
          <div class="summary-stats">
            <div class="stat-item">
              <span class="stat-label">Trend:</span>
              <span class="stat-value" :class="trendDirection">
                {{ trendText }}
              </span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Peak Year:</span>
              <span class="stat-value">{{ peakYear }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Peak Count:</span>
              <span class="stat-value">{{ peakCount }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="species" class="species-info">
      <div class="species-details">
        <img :src="species.imageUrl" :alt="species.commonName" class="species-image" />
        <div class="species-metadata">
          <h5 class="species-name">{{ species.commonName }}</h5>
          <p class="species-scientific">{{ species.scientificName }}</p>
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
      canvasReady: false
    }
  },
  computed: {
    chartWidth() {
      return 800
    },
    chartHeight() {
      return 400
    },
    trendDirection() {
      if (!this.chartData || this.chartData.length < 2) return 'neutral'

      const firstCount = this.chartData[0].count
      const lastCount = this.chartData[this.chartData.length - 1].count

      if (lastCount > firstCount) return 'positive'
      if (lastCount < firstCount) return 'negative'
      return 'neutral'
    },
    trendText() {
      const direction = this.trendDirection
      if (direction === 'positive') return 'Increasing'
      if (direction === 'negative') return 'Decreasing'
      return 'Stable'
    },
    peakYear() {
      if (!this.chartData || this.chartData.length === 0) return 'N/A'

      const peak = this.chartData.reduce((max, item) =>
        item.count > max.count ? item : max
      )
      return peak.year
    },
    peakCount() {
      if (!this.chartData || this.chartData.length === 0) return 'N/A'

      const peak = this.chartData.reduce((max, item) =>
        item.count > max.count ? item : max
      )
      return peak.count.toLocaleString()
    }
  },
  watch: {
    chartData: {
      handler() {
        this.$nextTick(() => {
          this.renderChart()
        })
      },
      immediate: true
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.canvasReady = !!this.$refs.chartCanvas
      this.renderChart()
    })
  },
  methods: {
    renderChart() {
      if (!this.chartData || this.chartData.length === 0) {
        console.log('No chart data available')
        return
      }

      if (!this.$refs.chartCanvas) {
        console.log('Canvas ref not available')
        return
      }

      const canvas = this.$refs.chartCanvas
      const ctx = canvas.getContext('2d')

      if (!ctx) {
        console.log('Could not get canvas context')
        return
      }

      const width = this.chartWidth
      const height = this.chartHeight
      const padding = 60

      ctx.clearRect(0, 0, width, height)

      const maxCount = Math.max(...this.chartData.map(d => d.count))
      const minCount = Math.min(...this.chartData.map(d => d.count))
      const countRange = maxCount - minCount || 1

      ctx.strokeStyle = '#4299e1'
      ctx.lineWidth = 3
      ctx.beginPath()

      this.chartData.forEach((point, index) => {
        const x = padding + (index / (this.chartData.length - 1)) * (width - 2 * padding)
        const y = height - padding - ((point.count - minCount) / countRange) * (height - 2 * padding)

        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })

      ctx.stroke()

      ctx.fillStyle = '#4299e1'
      this.chartData.forEach((point, index) => {
        const x = padding + (index / (this.chartData.length - 1)) * (width - 2 * padding)
        const y = height - padding - ((point.count - minCount) / countRange) * (height - 2 * padding)

        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
      })

      ctx.fillStyle = '#2d3748'
      ctx.font = '12px sans-serif'
      ctx.textAlign = 'center'

      this.chartData.forEach((point, index) => {
        const x = padding + (index / (this.chartData.length - 1)) * (width - 2 * padding)
        ctx.fillText(point.year.toString(), x, height - 20)
      })

      ctx.textAlign = 'right'
      const steps = 5
      for (let i = 0; i <= steps; i++) {
        const value = minCount + (countRange * i / steps)
        const y = height - padding - (i / steps) * (height - 2 * padding)
        ctx.fillText(Math.round(value).toLocaleString(), padding - 10, y + 4)
      }

      console.log('Chart rendered successfully with', this.chartData.length, 'data points')
    }
  }
}
</script>

<style scoped>
.trend-chart-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  margin: 0;
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
}

.chart-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #e2e8f0;
  border-top: 2px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 12px;
}

.no-data {
  text-align: center;
  padding: 60px;
  color: #718096;
}

.chart-wrapper {
  text-align: center;
}

.trend-summary {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.summary-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #718096;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
}

.stat-value.positive {
  color: #38a169;
}

.stat-value.negative {
  color: #e53e3e;
}

.stat-value.neutral {
  color: #718096;
}

.species-info {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.species-details {
  display: flex;
  align-items: center;
  gap: 16px;
}

.species-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
}

.species-name {
  margin: 0 0 4px 0;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
}

.species-scientific {
  margin: 0;
  color: #718096;
  font-size: 14px;
  font-style: italic;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
