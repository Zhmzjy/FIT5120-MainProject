<template>
  <div class="action-buttons">
    <SeasonButton
      v-for="season in seasons"
      :key="season"
      :season="season"
      :is-selected="selectedSeason === season"
      @select="handleSeasonSelect"
      size="small"
    />
  </div>
</template>

<script>
import SeasonButton from './SeasonButton.vue'

export default {
  name: 'SeasonButtonGroup',
  components: {
    SeasonButton
  },
  props: {
    selectedSeason: {
      type: String,
      default: 'Spring'
    }
  },
  emits: ['update:selectedSeason'],
  data() {
    return {
      seasons: ['Spring', 'Summer', 'Autumn', 'Winter']
    }
  },
  methods: {
    handleSeasonSelect(season) {
      this.$emit('update:selectedSeason', season)
    }
  }
}
</script>

<style scoped>
.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
  align-items: center;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
  }
}
</style>
