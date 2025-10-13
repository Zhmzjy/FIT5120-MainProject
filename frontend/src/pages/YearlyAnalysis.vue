<template>
  <div class="yearly-analysis-page">
    <img src="/images/epic6.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

    <TopNavigation @toggleMobileMenu="toggleMobileMenu" />

    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Yearly Wildlife Analysis</h1>
        <p class="page-subtitle">Explore how Australian wildlife populations have changed over time</p>
      </div>

      <YearSelector
        :selectedYear="selectedYear"
        :compareYear="compareYear"
        :mode="analysisMode"
        :availableYears="availableYears"
        @year-changed="handleYearChange"
        @compare-year-changed="handleCompareYearChange"
        @mode-changed="handleModeChange"
      />

      <div class="analysis-content">
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading wildlife data...</p>
        </div>

        <div v-else class="data-display">
          <div v-if="analysisMode === 'single'" class="single-year-view">
            <div class="stats-grid">
              <YearlyStatsCard
                title="Most Common Species"
                :year="selectedYear"
                :speciesList="currentYearData.mostCommon"
                cardType="most-common"
                @species-selected="handleSpeciesSelected"
                @view-trend="handleViewTrend"
              />

              <YearlyStatsCard
                title="Least Common Species"
                :year="selectedYear"
                :speciesList="currentYearData.leastCommon"
                cardType="least-common"
                @species-selected="handleSpeciesSelected"
                @view-trend="handleViewTrend"
              />
            </div>
          </div>

          <div v-else class="compare-years-view">
            <SpeciesComparisonCard
              :year1="selectedYear"
              :year2="compareYear"
              :data="comparisonData"
            />
          </div>
        </div>
      </div>

      <SpeciesSearch
        @species-selected="handleSpeciesSearchSelected"
      />

      <div v-if="selectedSpeciesForTrend" class="trend-section">
        <TrendChart
          :title="`${selectedSpeciesForTrend.commonName} Population Trend`"
          :chartData="selectedSpeciesTrendData"
          :species="selectedSpeciesForTrend"
          :loading="trendLoading"
        />
      </div>
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import TopNavigation from '../components/common/TopNavigation.vue'
import YearSelector from '../components/yearly/YearSelector.vue'
import YearlyStatsCard from '../components/yearly/YearlyStatsCard.vue'
import SpeciesComparisonCard from '../components/yearly/SpeciesComparisonCard.vue'
import TrendChart from '../components/yearly/TrendChart.vue'
import SpeciesSearch from '../components/yearly/SpeciesSearch.vue'
import api from '../services/api'
import { getWikipediaImage } from '@/utils/wikipediaImage.js'

export default {
  name: 'YearlyAnalysis',
  components: {
    TopNavigation,
    YearSelector,
    YearlyStatsCard,
    SpeciesComparisonCard,
    TrendChart,
    SpeciesSearch
  },
  data() {
    return {
      mobileMenuOpen: false,
      selectedYear: 2022,
      compareYear: 2021,
      analysisMode: 'single',
      availableYears: [],
      loading: false,
      trendLoading: false,
      selectedSpeciesForTrend: null,
      currentYearData: {
        mostCommon: [],
        leastCommon: []
      },
      comparisonData: null,
      selectedSpeciesTrendData: []
    }
  },
  async mounted() {
    await this.loadAvailableYears()
    await this.loadYearData()
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    async loadAvailableYears() {
      try {
        const years = await api.getAvailableYears()
        this.availableYears = years
        if (years.length > 0) {
          this.selectedYear = years[0]
          this.compareYear = years[1] || years[0]
        }
      } catch (error) {
        console.error('Error loading available years:', error)
      }
    },
    async handleYearChange(year) {
      this.selectedYear = year
      await this.loadYearData()
    },
    async handleCompareYearChange(year) {
      this.compareYear = year
      await this.loadComparisonData()
    },
    async handleModeChange(mode) {
      this.analysisMode = mode
      if (mode === 'compare') {
        await this.loadComparisonData()
      } else {
        await this.loadYearData()
      }
    },
    handleSpeciesSelected(species) {
      console.log('Species selected:', species)
    },
    async handleViewTrend(species) {
      this.selectedSpeciesForTrend = species
      await this.loadSpeciesTrend(species.commonName)
    },
    async handleSpeciesSearchSelected(species) {
      this.selectedSpeciesForTrend = species
      await this.loadSpeciesTrend(species.commonName)
    },
    async loadYearData() {
      this.loading = true
      try {
        const [mostCommon, leastCommon] = await Promise.all([
          api.getYearlyMostCommon(this.selectedYear),
          api.getYearlyLeastCommon(this.selectedYear)
        ])

        this.currentYearData.mostCommon = await this.enrichSpeciesWithImages(mostCommon)
        this.currentYearData.leastCommon = await this.enrichSpeciesWithImages(leastCommon)
      } catch (error) {
        console.error('Error loading year data:', error)
      } finally {
        this.loading = false
      }
    },
    async loadComparisonData() {
      this.loading = true
      try {
        const data = await api.compareYears(this.selectedYear, this.compareYear)

        data.year1.mostCommon = await this.enrichSpeciesWithImages(data.year1.mostCommon)
        data.year1.leastCommon = await this.enrichSpeciesWithImages(data.year1.leastCommon)
        data.year2.mostCommon = await this.enrichSpeciesWithImages(data.year2.mostCommon)
        data.year2.leastCommon = await this.enrichSpeciesWithImages(data.year2.leastCommon)

        this.comparisonData = data
      } catch (error) {
        console.error('Error loading comparison data:', error)
      } finally {
        this.loading = false
      }
    },
    async loadSpeciesTrend(commonName) {
      this.trendLoading = true
      try {
        const startYear = Math.min(...this.availableYears)
        const endYear = Math.max(...this.availableYears)

        const trendData = await api.getSpeciesTrendData(commonName, startYear, endYear)
        this.selectedSpeciesTrendData = trendData
      } catch (error) {
        console.error('Error loading species trend:', error)
        this.selectedSpeciesTrendData = []
      } finally {
        this.trendLoading = false
      }
    },
    async enrichSpeciesWithImages(speciesList) {
      return await Promise.all(speciesList.map(async (species) => {
        const imageUrl = await getWikipediaImage(species.commonName)
        return {
          ...species,
          imageUrl: imageUrl || '/images/koala.png'
        }
      }))
    }
  }
}
</script>

<style scoped>
.yearly-analysis-page {
  min-height: 100vh;
  position: relative;
}

.main-content {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  padding-top: 100px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 12px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}

.page-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.analysis-content {
  margin-bottom: 32px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-state p {
  color: #718096;
  font-size: 18px;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.trend-section {
  margin-top: 32px;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .main-content {
    padding: 20px 16px;
    padding-top: 80px;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
