<template>
  <div class="seasonal-page min-h-screen bg-gradient-to-b from-blue-50 to-green-50 p-4">
    <div class="max-w-6xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-green-800 mb-2">Seasonal Wildlife Activities</h1>
        <p class="text-lg text-gray-600">Discover what animals do in different seasons!</p>
      </div>

      <SeasonSelector @season-selected="handleSeasonChange" :selected-season="selectedSeason" />

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        <p class="mt-2 text-gray-600">Loading seasonal data...</p>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{ error }}
        </div>
        <button @click="fetchSeasonalData" class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          Try Again
        </button>
      </div>

      <div v-else-if="seasonalData" class="space-y-8">
        <KpiStrip :data="seasonalData.summary" />

        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Activity Levels</h2>
          <ActivityChart :activities="seasonalData.activities" />
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Featured Animals</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimalCard
              v-for="animal in seasonalData.animals"
              :key="animal.id"
              :animal="animal"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SeasonSelector from '../components/seasonal/SeasonSelector.vue'
import KpiStrip from '../components/seasonal/KpiStrip.vue'
import ActivityChart from '../components/seasonal/ActivityChart.vue'
import AnimalCard from '../components/seasonal/AnimalCard.vue'

export default {
  name: 'SeasonalPage',
  components: {
    SeasonSelector,
    KpiStrip,
    ActivityChart,
    AnimalCard
  },
  data() {
    return {
      selectedSeason: 'Spring',
      seasonalData: null,
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchSeasonalData()
  },
  methods: {
    handleSeasonChange(season) {
      this.selectedSeason = season
      this.fetchSeasonalData()
    },
    async fetchSeasonalData() {
      this.loading = true
      this.error = null

      try {
        const response = await fetch(`/api/animals/seasonal?season=${this.selectedSeason}`)

        if (!response.ok) {
          throw new Error(`Failed to fetch seasonal data: ${response.status}`)
        }

        this.seasonalData = await response.json()
      } catch (err) {
        this.error = err.message || 'Failed to load seasonal data'
        this.seasonalData = this.getMockData()
      } finally {
        this.loading = false
      }
    },
    getMockData() {
      return {
        summary: {
          totalAnimals: 45,
          activeSpecies: 32,
          migrationCount: 8
        },
        activities: [
          { name: 'Foraging', value: 85 },
          { name: 'Nesting', value: 70 },
          { name: 'Migration', value: 40 },
          { name: 'Hibernation', value: 15 }
        ],
        animals: [
          {
            id: 1,
            name: 'Kangaroo',
            image: '/images/kangaroo.jpg',
            score: 4,
            count: 12,
            activity: 'Active foraging'
          },
          {
            id: 2,
            name: 'Koala',
            image: '/images/koala.jpg',
            score: 5,
            count: 8,
            activity: 'Resting in trees'
          },
          {
            id: 3,
            name: 'Wombat',
            image: '/images/wombat.jpg',
            score: 3,
            count: 5,
            activity: 'Burrowing'
          }
        ]
      }
    }
  }
}
</script>
