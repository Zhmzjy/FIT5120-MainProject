<template>
  <div class="season-selector mb-8">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="season in seasons"
        :key="season.name"
        @click="selectSeason(season.name)"
        :class="[
          'transform transition-all duration-300',
          selectedSeason === season.name ? 'scale-105' : 'hover:scale-102'
        ]"
      >
        <SeasonTile
          :emoji="season.icon"
          :title="season.name"
          :subtitle="season.description"
          :class="[
            selectedSeason === season.name
              ? 'ring-4 ring-green-400 ring-opacity-50'
              : ''
          ]"
        />
      </div>
    </div>
  </div>
</template>

<script>
import SeasonTile from './SeasonTile.vue'

export default {
  name: 'SeasonSelector',
  components: {
    SeasonTile
  },
  props: {
    selectedSeason: {
      type: String,
      default: 'Spring'
    }
  },
  emits: ['season-selected'],
  data() {
    return {
      seasons: [
        {
          name: 'Spring',
          icon: '🌸',
          description: 'New life blooms'
        },
        {
          name: 'Summer',
          icon: '☀️',
          description: 'Hot and active'
        },
        {
          name: 'Autumn',
          icon: '🍂',
          description: 'Preparing for rest'
        },
        {
          name: 'Winter',
          icon: '❄️',
          description: 'Cold and quiet'
        }
      ]
    }
  },
  methods: {
    selectSeason(season) {
      this.$emit('season-selected', season)
    }
  }
}
</script>

<style scoped>
.season-button {
  min-height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
</style>
