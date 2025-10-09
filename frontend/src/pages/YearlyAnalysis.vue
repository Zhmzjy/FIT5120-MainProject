<template>
  <div class="yearly-analysis-page">
    <img src="/images/v2osk-1Z2niiBPg5A-unsplash.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

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
      selectedYear: 2024,
      compareYear: 2023,
      analysisMode: 'single',
      availableYears: [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015],
      loading: false,
      trendLoading: false,
      selectedSpeciesForTrend: null,
      mockData: {
        2024: {
          mostCommon: [
            {
              taxonId: 1,
              commonName: 'Rainbow Lorikeet',
              scientificName: 'Trichoglossus moluccanus',
              count: 15420,
              imageUrl: '/images/koala.png',
              trend: { direction: 'up', percentage: 12 }
            },
            {
              taxonId: 2,
              commonName: 'Australian Magpie',
              scientificName: 'Gymnorhina tibicen',
              count: 12350,
              imageUrl: '/images/kangaroo.png',
              trend: { direction: 'up', percentage: 8 }
            },
            {
              taxonId: 3,
              commonName: 'Koala',
              scientificName: 'Phascolarctos cinereus',
              count: 8920,
              imageUrl: '/images/koala.png',
              trend: { direction: 'down', percentage: 5 }
            }
          ],
          leastCommon: [
            {
              taxonId: 101,
              commonName: 'Bilby',
              scientificName: 'Macrotis lagotis',
              count: 42,
              imageUrl: '/images/kangaroo.png',
              trend: { direction: 'down', percentage: 18 }
            },
            {
              taxonId: 102,
              commonName: 'Tasmanian Devil',
              scientificName: 'Sarcophilus harrisii',
              count: 67,
              imageUrl: '/images/koala.png',
              trend: { direction: 'down', percentage: 12 }
            }
          ],
          totalSpecies: 1250,
          totalObservations: 125340
        },
        2023: {
          mostCommon: [
            {
              taxonId: 2,
              commonName: 'Australian Magpie',
              scientificName: 'Gymnorhina tibicen',
              count: 14200,
              imageUrl: '/images/kangaroo.png'
            },
            {
              taxonId: 1,
              commonName: 'Rainbow Lorikeet',
              scientificName: 'Trichoglossus moluccanus',
              count: 13750,
              imageUrl: '/images/koala.png'
            }
          ],
          leastCommon: [
            {
              taxonId: 101,
              commonName: 'Bilby',
              scientificName: 'Macrotis lagotis',
              count: 51,
              imageUrl: '/images/kangaroo.png'
            }
          ],
          totalSpecies: 1180,
          totalObservations: 118650
        },
        trendData: {
          1: [
            { year: 2015, count: 8420 },
            { year: 2016, count: 9150 },
            { year: 2017, count: 10200 },
            { year: 2018, count: 11800 },
            { year: 2019, count: 12950 },
            { year: 2020, count: 11200 },
            { year: 2021, count: 12800 },
            { year: 2022, count: 13200 },
            { year: 2023, count: 13750 },
            { year: 2024, count: 15420 }
          ],
          2: [
            { year: 2015, count: 11200 },
            { year: 2016, count: 11800 },
            { year: 2017, count: 12400 },
            { year: 2018, count: 13100 },
            { year: 2019, count: 13800 },
            { year: 2020, count: 12900 },
            { year: 2021, count: 13400 },
            { year: 2022, count: 13900 },
            { year: 2023, count: 14200 },
            { year: 2024, count: 12350 }
          ],
          3: [
            { year: 2015, count: 12400 },
            { year: 2016, count: 11800 },
            { year: 2017, count: 11200 },
            { year: 2018, count: 10800 },
            { year: 2019, count: 10200 },
            { year: 2020, count: 9800 },
            { year: 2021, count: 9600 },
            { year: 2022, count: 9400 },
            { year: 2023, count: 9380 },
            { year: 2024, count: 8920 }
          ],
          4: [
            { year: 2015, count: 5200 },
            { year: 2016, count: 5800 },
            { year: 2017, count: 6200 },
            { year: 2018, count: 6800 },
            { year: 2019, count: 7200 },
            { year: 2020, count: 6900 },
            { year: 2021, count: 7400 },
            { year: 2022, count: 7800 },
            { year: 2023, count: 8100 },
            { year: 2024, count: 8500 }
          ],
          5: [
            { year: 2015, count: 890 },
            { year: 2016, count: 820 },
            { year: 2017, count: 750 },
            { year: 2018, count: 680 },
            { year: 2019, count: 620 },
            { year: 2020, count: 580 },
            { year: 2021, count: 540 },
            { year: 2022, count: 490 },
            { year: 2023, count: 450 },
            { year: 2024, count: 420 }
          ],
          6: [
            { year: 2015, count: 120 },
            { year: 2016, count: 108 },
            { year: 2017, count: 95 },
            { year: 2018, count: 87 },
            { year: 2019, count: 78 },
            { year: 2020, count: 72 },
            { year: 2021, count: 69 },
            { year: 2022, count: 65 },
            { year: 2023, count: 62 },
            { year: 2024, count: 67 }
          ]
        }
      }
    }
  },
  computed: {
    currentYearData() {
      const data = this.mockData[this.selectedYear]
      return data || {
        mostCommon: [],
        leastCommon: [],
        totalSpecies: 0,
        totalObservations: 0
      }
    },
    comparisonData() {
      if (this.analysisMode === 'compare') {
        const year1Data = this.mockData[this.selectedYear] || {
          mostCommon: [],
          leastCommon: [],
          totalSpecies: 0,
          totalObservations: 0
        }
        const year2Data = this.mockData[this.compareYear] || {
          mostCommon: [],
          leastCommon: [],
          totalSpecies: 0,
          totalObservations: 0
        }
        return {
          year1: year1Data,
          year2: year2Data
        }
      }
      return null
    },
    selectedSpeciesTrendData() {
      if (this.selectedSpeciesForTrend) {
        return this.mockData.trendData[this.selectedSpeciesForTrend.taxonId] || []
      }
      return []
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    handleYearChange(year) {
      this.selectedYear = year
      this.loadYearData()
    },
    handleCompareYearChange(year) {
      this.compareYear = year
      this.loadComparisonData()
    },
    handleModeChange(mode) {
      this.analysisMode = mode
      if (mode === 'compare') {
        this.loadComparisonData()
      } else {
        this.loadYearData()
      }
    },
    handleSpeciesSelected(species) {
      console.log('Species selected:', species)
    },
    handleViewTrend(species) {
      this.selectedSpeciesForTrend = species
      this.loadSpeciesTrend(species.taxonId)
    },
    handleSpeciesSearchSelected(species) {
      console.log('Species search selected:', species, 'taxonId:', species.taxonId)
      this.selectedSpeciesForTrend = species
      this.loadSpeciesTrend(species.taxonId)
    },
    loadYearData() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 800)
    },
    loadComparisonData() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 1000)
    },
    loadSpeciesTrend(taxonId) {
      console.log('Loading trend for taxonId:', taxonId)
      console.log('Available trend data:', Object.keys(this.mockData.trendData))
      this.trendLoading = true
      setTimeout(() => {
        this.trendLoading = false
        console.log('Trend loaded for taxonId:', taxonId, 'data:', this.mockData.trendData[taxonId])
      }, 600)
    }
  },
  mounted() {
    this.loadYearData()
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
